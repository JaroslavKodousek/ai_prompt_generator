from typing import List
from ..core.base_strategy import BaseExtractionStrategy
from ..core.llm_provider import BaseLLMClient

# Import all strategies
from .strategy_01_basic import BasicExtractionStrategy
from .strategy_02_structured import StructuredExtractionStrategy
from .strategy_03_cot import ChainOfThoughtStrategy
from .strategy_04_role_expert import RoleExpertStrategy
from .strategy_05_few_shot import FewShotStrategy
from .strategy_06_step_by_step import StepByStepStrategy
from .strategy_07_table_focused import TableFocusedStrategy
from .strategy_08_entity_focused import EntityFocusedStrategy
from .strategy_09_minimal import MinimalStrategy
from .strategy_10_verbose import VerboseStrategy
from .strategy_11_context_aware import ContextAwareStrategy
from .strategy_12_xml_format import XMLFormatStrategy
from .strategy_13_confidence_scoring import ConfidenceScoringStrategy
from .strategy_14_multi_pass import MultiPassStrategy
from .strategy_15_template_matching import TemplateMatchingStrategy
from .strategy_16_key_value_pairs import KeyValuePairStrategy
from .strategy_17_semantic_extraction import SemanticExtractionStrategy
from .strategy_18_prioritized import PrioritizedExtractionStrategy
from .strategy_19_comparative import ComparativeStrategy
from .strategy_20_hybrid import HybridStrategy


def get_all_strategies(client: BaseLLMClient, model: str = "") -> List[BaseExtractionStrategy]:
    """Get all available extraction strategies."""
    return [
        BasicExtractionStrategy(client, model),
        StructuredExtractionStrategy(client, model),
        ChainOfThoughtStrategy(client, model),
        RoleExpertStrategy(client, model),
        FewShotStrategy(client, model),
        StepByStepStrategy(client, model),
        TableFocusedStrategy(client, model),
        EntityFocusedStrategy(client, model),
        MinimalStrategy(client, model),
        VerboseStrategy(client, model),
        ContextAwareStrategy(client, model),
        XMLFormatStrategy(client, model),
        ConfidenceScoringStrategy(client, model),
        MultiPassStrategy(client, model),
        TemplateMatchingStrategy(client, model),
        KeyValuePairStrategy(client, model),
        SemanticExtractionStrategy(client, model),
        PrioritizedExtractionStrategy(client, model),
        ComparativeStrategy(client, model),
        HybridStrategy(client, model),
    ]


def get_strategy_by_id(strategy_id: str, client: BaseLLMClient, model: str = "") -> BaseExtractionStrategy:
    """Get a specific strategy by ID."""
    strategies = get_all_strategies(client, model)
    for strategy in strategies:
        if strategy.metadata.id == strategy_id:
            return strategy
    raise ValueError(f"Strategy not found: {strategy_id}")


def list_strategies() -> None:
    """Print all available strategies."""
    from ..core.llm_provider import create_llm_client, LLMProvider
    import os
    from dotenv import load_dotenv

    load_dotenv()

    # Try to create client with available API key
    try:
        client = create_llm_client(LLMProvider.GEMINI)
    except:
        try:
            client = create_llm_client(LLMProvider.ANTHROPIC)
        except:
            # Dummy client for listing only
            from ..core.llm_provider import GeminiClient
            client = GeminiClient(api_key="dummy")

    strategies = get_all_strategies(client)

    print("\nAvailable Extraction Strategies:")
    print("=" * 80)
    for strategy in strategies:
        meta = strategy.metadata
        print(f"\n{meta.id}: {meta.name}")
        print(f"  Category: {meta.category}")
        print(f"  Description: {meta.description}")
        print(f"  Est. Cost: ${meta.expected_cost_per_call:.4f}")
        print(f"  Use Cases: {', '.join(meta.use_cases)}")
    print("\n" + "=" * 80)
