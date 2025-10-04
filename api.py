#!/usr/bin/env python3
"""
FastAPI web service for document extraction.
Can be deployed to Cloudflare Workers with Python Workers.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import tempfile
import os
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.extraction_engine import ExtractionEngine
from src.core.llm_provider import create_llm_client, LLMProvider
from src.strategies.strategy_registry import get_all_strategies
from src.core.validator import ResultValidator
from src.utils.document_loader import DocumentLoader

app = FastAPI(
    title="AI Prompt Generator API",
    description="Document data extraction using 20 different AI strategies",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExtractionRequest(BaseModel):
    provider: str = "gemini"  # "gemini" or "anthropic"
    max_concurrent: int = 5
    ground_truth: Optional[Dict[str, Any]] = None


class StrategyInfo(BaseModel):
    id: str
    name: str
    description: str
    category: str
    expected_cost: float


@app.get("/")
async def root():
    """Serve the main web interface."""
    return FileResponse("static/index.html")


@app.get("/api")
async def api_info():
    return {
        "message": "AI Prompt Generator API",
        "version": "1.0.0",
        "endpoints": {
            "/extract": "POST - Extract data from document",
            "/strategies": "GET - List all strategies",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/strategies", response_model=List[StrategyInfo])
async def list_strategies():
    """List all available extraction strategies."""
    try:
        # Create dummy client for metadata
        client = create_llm_client(LLMProvider.GEMINI)
        strategies = get_all_strategies(client)

        return [
            StrategyInfo(
                id=s.metadata.id,
                name=s.metadata.name,
                description=s.metadata.description,
                category=s.metadata.category,
                expected_cost=s.metadata.expected_cost_per_call
            )
            for s in strategies
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/extract")
async def extract_document(
    file: UploadFile = File(...),
    provider: str = Form("openrouter"),
    model: str = Form("google/gemini-2.5-flash"),
    max_concurrent: int = Form(5),
    api_key: Optional[str] = Form(None)
):
    """
    Extract data from document using all strategies.

    Args:
        file: Document file (PDF, DOCX, or text)
        provider: LLM provider (default: "openrouter")
        model: Model name (required for OpenRouter)
        max_concurrent: Max concurrent requests
        api_key: Optional API key (otherwise from env)

    Returns:
        Extraction results from all strategies
    """
    temp_file = None
    try:
        # Validate provider
        if provider not in ["openrouter"]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid provider: {provider}. Currently only 'openrouter' is supported"
            )

        # Save uploaded file temporarily
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            content = await file.read()
            temp.write(content)
            temp_file = temp.name

        # Create LLM client
        llm_provider = LLMProvider(provider)
        client = create_llm_client(llm_provider, api_key=api_key, model=model)

        # Get strategies
        strategies = get_all_strategies(client)

        # Create engine
        engine = ExtractionEngine(
            strategies=strategies,
            llm_client=client,
            max_concurrent=max_concurrent,
            request_delay=0.5
        )

        # Run extraction
        results = await engine.extract_with_all_strategies(temp_file)

        # Validate results
        validation_metrics = ResultValidator.compare_results(results, None)

        # Create report
        report = engine.create_comparison_report(
            document_name=file.filename,
            results=results,
            ground_truth=None
        )
        report.validation_metrics = validation_metrics

        # Find best strategy
        best_strategy_id = ResultValidator.find_best_strategy(
            results,
            validation_metrics,
            optimize_for="cost"
        )

        if best_strategy_id:
            best = next(r for r in results if r.strategy_id == best_strategy_id)
            report.best_strategy = best.strategy_name

        return JSONResponse(content=report.model_dump(mode='json'))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Cleanup temp file
        if temp_file and os.path.exists(temp_file):
            os.unlink(temp_file)


@app.post("/extract-single")
async def extract_single_strategy(
    file: UploadFile = File(...),
    strategy_id: str = Form("strategy_01"),
    provider: str = Form("openrouter"),
    model: Optional[str] = Form(None),
    api_key: Optional[str] = Form(None)
):
    """
    Extract data using a single strategy.

    Args:
        file: Document file
        strategy_id: Strategy ID to use
        provider: LLM provider
        model: Optional model name
        api_key: Optional API key

    Returns:
        Extraction result
    """
    temp_file = None
    try:
        # Save uploaded file
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            content = await file.read()
            temp.write(content)
            temp_file = temp.name

        # Load document
        text, doc_type = DocumentLoader.load(temp_file)
        text = DocumentLoader.preprocess_text(text)

        # Create client and strategy
        llm_provider = LLMProvider(provider)
        client = create_llm_client(llm_provider, api_key=api_key, model=model)

        from src.strategies.strategy_registry import get_strategy_by_id
        strategy = get_strategy_by_id(strategy_id, client)

        # Run extraction
        result = await strategy.extract(text)

        return JSONResponse(content=result.model_dump(mode='json'))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if temp_file and os.path.exists(temp_file):
            os.unlink(temp_file)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
