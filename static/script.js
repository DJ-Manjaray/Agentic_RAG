// DOM Elements
const queryInput = document.getElementById('queryInput');
const submitBtn = document.getElementById('submitBtn');
const loadingIndicator = document.getElementById('loadingIndicator');
const responseSection = document.getElementById('responseSection');
const errorSection = document.getElementById('errorSection');
const workflowSteps = document.getElementById('workflowSteps');
const exampleChips = document.querySelectorAll('.example-chip');

// Response elements
const routeValue = document.getElementById('routeValue');
const sourceValue = document.getElementById('sourceValue');
const relevanceValue = document.getElementById('relevanceValue');
const responseContent = document.getElementById('responseContent');
const workflowVisualization = document.getElementById('workflowVisualization');
const errorMessage = document.getElementById('errorMessage');

// Event Listeners
submitBtn.addEventListener('click', handleSubmit);
queryInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
        handleSubmit();
    }
});

// Example chip click handlers
exampleChips.forEach(chip => {
    chip.addEventListener('click', () => {
        const query = chip.getAttribute('data-query');
        queryInput.value = query;
        handleSubmit();
    });
});

// Main submit handler
async function handleSubmit() {
    const query = queryInput.value.trim();
    
    if (!query) {
        showError('Please enter a query');
        return;
    }

    // Reset UI
    hideAll();
    showLoading();
    submitBtn.disabled = true;

    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'An error occurred');
        }

        if (data.success) {
            displayResponse(data);
        } else {
            throw new Error(data.error || 'Failed to get response');
        }

    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'An unexpected error occurred');
    } finally {
        submitBtn.disabled = false;
        hideLoading();
    }
}

// Display the response
function displayResponse(data) {
    // Update metadata
    routeValue.textContent = formatRoute(data.route) || '-';
    sourceValue.textContent = data.source || '-';
    relevanceValue.textContent = data.is_relevant || '-';
    
    // Update response content
    responseContent.textContent = data.response || 'No response generated';
    
    // Update workflow visualization
    updateWorkflowVisualization(data.workflow_steps);
    
    // Show response section
    responseSection.style.display = 'block';
    
    // Scroll to response
    responseSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Update workflow visualization
function updateWorkflowVisualization(steps) {
    workflowVisualization.innerHTML = '';
    
    if (!steps || steps.length === 0) {
        workflowVisualization.innerHTML = '<p style="color: var(--text-tertiary);">No workflow steps recorded</p>';
        return;
    }
    
    steps.forEach((step, index) => {
        const node = document.createElement('div');
        node.className = 'workflow-node';
        node.textContent = step;
        node.style.animationDelay = `${index * 0.1}s`;
        workflowVisualization.appendChild(node);
    });
}

// Format route name
function formatRoute(route) {
    if (!route) return '';
    
    const routeMap = {
        'Retrieve_QnA': 'Medical Q&A Database',
        'Retrieve_Device': 'Medical Device Manuals',
        'Web_Search': 'Web Search'
    };
    
    return routeMap[route] || route;
}

// Show loading state
function showLoading() {
    loadingIndicator.style.display = 'block';
    workflowSteps.innerHTML = '<div class="workflow-step">Initializing...</div>';
}

// Hide loading state
function hideLoading() {
    loadingIndicator.style.display = 'none';
}

// Show error
function showError(message) {
    hideAll();
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    
    // Auto-hide error after 5 seconds
    setTimeout(() => {
        errorSection.style.display = 'none';
    }, 5000);
}

// Hide all sections
function hideAll() {
    loadingIndicator.style.display = 'none';
    responseSection.style.display = 'none';
    errorSection.style.display = 'none';
}

// Auto-resize textarea
queryInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

// Add keyboard shortcut hint
document.addEventListener('DOMContentLoaded', () => {
    const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
    const shortcutKey = isMac ? 'Cmd' : 'Ctrl';
    
    queryInput.placeholder = `Example: What are the treatments for Kawasaki disease?\n\nPress ${shortcutKey}+Enter to submit`;
});

// Add visual feedback for button clicks
submitBtn.addEventListener('mousedown', function() {
    this.style.transform = 'scale(0.98)';
});

submitBtn.addEventListener('mouseup', function() {
    this.style.transform = '';
});

