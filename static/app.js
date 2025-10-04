// API Base URL
const API_BASE = window.location.origin;

// State
let currentResults = null;
let strategies = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initFileUpload();
    initForm();
    loadStrategies();
});

// Tab Navigation
function initTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;

            // Update buttons
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Update content
            tabContents.forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(`${tabName}-tab`).classList.add('active');
        });
    });
}

// File Upload
function initFileUpload() {
    const fileInput = document.getElementById('file-input');
    const fileLabel = document.querySelector('.file-label');
    const fileName = document.getElementById('file-name');

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            const file = e.target.files[0];
            fileName.textContent = `Selected: ${file.name} (${formatFileSize(file.size)})`;
        } else {
            fileName.textContent = '';
        }
    });

    // Drag and drop
    fileLabel.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileLabel.style.borderColor = 'var(--primary)';
    });

    fileLabel.addEventListener('dragleave', () => {
        fileLabel.style.borderColor = 'var(--border)';
    });

    fileLabel.addEventListener('drop', (e) => {
        e.preventDefault();
        fileLabel.style.borderColor = 'var(--border)';

        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            const file = e.dataTransfer.files[0];
            fileName.textContent = `Selected: ${file.name} (${formatFileSize(file.size)})`;
        }
    });
}

// Form Submission
function initForm() {
    const form = document.getElementById('upload-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleSubmit();
    });
}

async function handleSubmit() {
    const fileInput = document.getElementById('file-input');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.getElementById('btn-text');
    const btnSpinner = document.getElementById('btn-spinner');
    const progressSection = document.getElementById('progress-section');

    if (!fileInput.files.length) {
        alert('Please select a file');
        return;
    }

    // Prepare form data
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('provider', document.getElementById('provider').value);
    formData.append('max_concurrent', document.getElementById('max-concurrent').value);

    const model = document.getElementById('model').value;
    if (model) formData.append('model', model);

    const apiKey = document.getElementById('api-key').value;
    if (apiKey) formData.append('api_key', apiKey);

    // Show loading state
    submitBtn.disabled = true;
    btnText.textContent = 'Processing...';
    btnSpinner.classList.remove('hidden');
    progressSection.classList.remove('hidden');

    try {
        // Start progress animation
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress = Math.min(progress + 1, 95);
            updateProgress(progress, 'Extracting data with multiple strategies...');
        }, 500);

        // Make API request
        const response = await fetch(`${API_BASE}/extract`, {
            method: 'POST',
            body: formData
        });

        clearInterval(progressInterval);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Extraction failed');
        }

        const results = await response.json();
        currentResults = results;

        // Complete progress
        updateProgress(100, 'Complete!');

        // Show results
        setTimeout(() => {
            displayResults(results);
            switchToResultsTab();
        }, 500);

    } catch (error) {
        console.error('Error:', error);
        alert(`Error: ${error.message}`);
        progressSection.classList.add('hidden');
    } finally {
        submitBtn.disabled = false;
        btnText.textContent = 'Analyze with All 20 Strategies';
        btnSpinner.classList.add('hidden');
    }
}

function updateProgress(percent, text) {
    document.getElementById('progress-fill').style.width = `${percent}%`;
    document.getElementById('progress-text').textContent = text;
}

// Load Strategies
async function loadStrategies() {
    try {
        const response = await fetch(`${API_BASE}/strategies`);
        strategies = await response.json();
        displayStrategies(strategies);
    } catch (error) {
        console.error('Error loading strategies:', error);
    }
}

function displayStrategies(strategies) {
    const container = document.getElementById('strategies-list');

    container.innerHTML = strategies.map(strategy => `
        <div class="strategy-card">
            <div class="strategy-header">
                <span class="strategy-id">${strategy.id}</span>
            </div>
            <h3>${strategy.name}</h3>
            <div class="strategy-category">${strategy.category}</div>
            <p class="strategy-description">${strategy.description}</p>
            <div class="strategy-meta">
                <span>Est. Cost</span>
                <span class="cost">$${strategy.expected_cost.toFixed(4)}</span>
            </div>
        </div>
    `).join('');
}

// Display Results
function displayResults(report) {
    const container = document.getElementById('results-container');

    if (!report.results || report.results.length === 0) {
        container.innerHTML = '<div class="empty-state"><h2>No results found</h2></div>';
        return;
    }

    // Sort by success and cost
    const sortedResults = [...report.results].sort((a, b) => {
        if (a.success !== b.success) return b.success - a.success;
        return a.execution_time - b.execution_time;
    });

    const html = `
        <div class="results-section">
            <div class="results-header">
                <div>
                    <h2>Extraction Results</h2>
                    <p style="color: var(--text-muted)">Document: ${report.document_name}</p>
                    <p style="color: var(--text-muted); font-size: 0.9rem;">Tested at: ${new Date(report.timestamp).toLocaleString()}</p>
                </div>
                ${report.best_strategy ? `<div class="best-badge">🏆 Best: ${report.best_strategy}</div>` : ''}
            </div>

            <div class="summary-stats" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
                <div class="stat">
                    <div class="stat-label">Total Strategies</div>
                    <div class="stat-value">${report.total_strategies}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Successful</div>
                    <div class="stat-value" style="color: var(--success)">${report.successful_extractions}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Failed</div>
                    <div class="stat-value" style="color: var(--danger)">${report.failed_extractions}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Avg Time</div>
                    <div class="stat-value">${report.average_execution_time.toFixed(2)}s</div>
                </div>
            </div>

            <h3 style="margin-bottom: 1rem;">Individual Strategy Results</h3>
            <div class="results-grid">
                ${sortedResults.map(result => renderResultCard(result, report.best_strategy)).join('')}
            </div>
        </div>
    `;

    container.innerHTML = html;
}

function renderResultCard(result, bestStrategy) {
    const isBest = result.strategy_name === bestStrategy;

    return `
        <div class="result-card ${isBest ? 'best' : ''}">
            <div class="result-header">
                <div>
                    <h3>${result.strategy_name} ${isBest ? '🏆' : ''}</h3>
                    <span style="color: var(--text-muted); font-size: 0.85rem;">${result.strategy_id}</span>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.5rem;">${result.success ? '✅' : '❌'}</div>
                    <div style="font-size: 0.85rem; color: var(--text-muted);">${result.success ? 'Success' : 'Failed'}</div>
                </div>
            </div>

            <div class="result-stats">
                <div class="stat">
                    <div class="stat-label">Execution Time</div>
                    <div class="stat-value" style="font-size: 1.2rem;">${result.execution_time.toFixed(2)}s</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Tokens Used</div>
                    <div class="stat-value" style="font-size: 1.2rem;">${result.tokens_used || 'N/A'}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Cost</div>
                    <div class="stat-value" style="font-size: 1.2rem; color: var(--success);">$${(result.cost || 0).toFixed(4)}</div>
                </div>
            </div>

            ${result.success ? `
                <div class="extracted-data">
                    <h4>Extracted Data</h4>
                    <div class="data-preview">${formatJSON(result.extracted_data)}</div>
                </div>
            ` : `
                <div style="margin-top: 1rem; padding: 1rem; background: var(--bg-card); border-radius: 0.5rem; color: var(--danger);">
                    <strong>Error:</strong> ${result.error || 'Unknown error'}
                </div>
            `}
        </div>
    `;
}

// Utilities
function switchToResultsTab() {
    document.querySelector('[data-tab="results"]').click();
}

function formatJSON(data) {
    if (typeof data === 'string') {
        try {
            data = JSON.parse(data);
        } catch {
            return data;
        }
    }
    return JSON.stringify(data, null, 2);
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}
