/**
 * JavaScript enhancements for AE Copilot
 * Adds Superhuman-style keyboard shortcuts and interactions
 */

// Keyboard shortcuts (Superhuman style)
document.addEventListener('keydown', function(e) {
    // Cmd/Ctrl + K for command palette
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        showCommandPalette();
    }
    
    // Cmd/Ctrl + S to save (when in ROI calculator)
    if ((e.metaKey || e.ctrlKey) && e.key === 's') {
        e.preventDefault();
        // Trigger save button if available
        const saveButton = document.querySelector('[data-testid="baseButton-secondary"]');
        if (saveButton && saveButton.textContent.includes('Save')) {
            saveButton.click();
        }
    }
    
    // Escape to close modals/expanders
    if (e.key === 'Escape') {
        closeModals();
    }
});

// Command palette (Superhuman style)
function showCommandPalette() {
    // Create command palette overlay
    const palette = document.createElement('div');
    palette.id = 'command-palette';
    palette.innerHTML = `
        <div style="
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 600px;
            max-width: 90vw;
            z-index: 10000;
            padding: 8px;
        ">
            <input type="text" id="command-input" placeholder="Type a command..." style="
                width: 100%;
                border: none;
                outline: none;
                padding: 12px 16px;
                font-size: 16px;
                border-radius: 8px;
            " autofocus>
            <div id="command-results" style="max-height: 400px; overflow-y: auto; margin-top: 8px;">
                <div class="command-item" data-action="roi">💰 Calculate ROI</div>
                <div class="command-item" data-action="gong">📞 Fetch Gong Transcript</div>
                <div class="command-item" data-action="crm">🏢 Load CRM Data</div>
                <div class="command-item" data-action="export">📤 Export Narrative Pack</div>
            </div>
        </div>
    `;
    
    document.body.appendChild(palette);
    
    // Style command items
    const style = document.createElement('style');
    style.textContent = `
        .command-item {
            padding: 12px 16px;
            cursor: pointer;
            border-radius: 8px;
            margin: 2px 0;
        }
        .command-item:hover {
            background: #f3f4f6;
        }
    `;
    document.head.appendChild(style);
    
    // Handle input
    const input = document.getElementById('command-input');
    input.addEventListener('input', filterCommands);
    input.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            palette.remove();
        }
    });
    
    // Handle clicks
    document.querySelectorAll('.command-item').forEach(item => {
        item.addEventListener('click', function() {
            const action = this.dataset.action;
            executeCommand(action);
            palette.remove();
        });
    });
}

function filterCommands(e) {
    const query = e.target.value.toLowerCase();
    document.querySelectorAll('.command-item').forEach(item => {
        if (item.textContent.toLowerCase().includes(query)) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
}

function executeCommand(action) {
    // Navigate to appropriate tab
    const tabs = document.querySelectorAll('[data-baseweb="tab"]');
    const actionMap = {
        'roi': 0,
        'gong': 1,
        'crm': 2,
        'export': 3
    };
    if (tabs[actionMap[action]]) {
        tabs[actionMap[action]].click();
    }
}

function closeModals() {
    document.querySelectorAll('#command-palette').forEach(el => el.remove());
}

// Smooth scroll to sections
function smoothScrollTo(element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Add loading states
function showLoading(element) {
    element.style.opacity = '0.6';
    element.style.pointerEvents = 'none';
}

function hideLoading(element) {
    element.style.opacity = '1';
    element.style.pointerEvents = 'auto';
}
