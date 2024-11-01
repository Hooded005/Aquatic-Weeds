// Color Schemes Configuration
const colorSchemes = {
    default: {
        '--primary-bg-color': '#475fdd',
        '--secondary-bg-color': '#5a90e2',
        '--hover-bg-color': '#6d82f2',
        '--text-color': '#ffffff',
        '--body-bg-color': '#f0f0f5',
        '--panel-bg-color': '#f2f7ff',
    },
    dark: {
        '--primary-bg-color': '#1f1f1f',
        '--secondary-bg-color': '#2b2b2b',
        '--hover-bg-color': '#373737',
        '--text-color': '#e0e0e0',
        '--body-bg-color': '#121212',
        '--panel-bg-color': '#1e1e1e',
    },
    light: {
        '--primary-bg-color': '#ffffff',
        '--secondary-bg-color': '#f5f5f5',
        '--hover-bg-color': '#e0e0e0',
        '--text-color': '#333333',
        '--body-bg-color': '#ffffff',
        '--panel-bg-color': '#f9f9f9',
    },
    blue: {
        '--primary-bg-color': '#1e90ff',
        '--secondary-bg-color': '#00bfff',
        '--hover-bg-color': '#87cefa',
        '--text-color': '#ffffff',
        '--body-bg-color': '#e6f2ff',
        '--panel-bg-color': '#cce6ff',
    },
    green: {
        '--primary-bg-color': '#2e8b57',
        '--secondary-bg-color': '#3cb371',
        '--hover-bg-color': '#66cdaa',
        '--text-color': '#ffffff',
        '--body-bg-color': '#e8f5e9',
        '--panel-bg-color': '#c8e6c9',
    },
    colorblind: {
        '--primary-bg-color': '#000000',
        '--secondary-bg-color': '#ffffff',
        '--hover-bg-color': '#7f7f7f',
        '--text-color': '#ffffff',
        '--body-bg-color': '#ffffff',
        '--panel-bg-color': '#000000',
    },
};

// Function to Apply Color Scheme
function applyColorScheme(scheme) {
    const root = document.documentElement;
    const colors = colorSchemes[scheme];

    if (colors) {
        for (const [variable, value] of Object.entries(colors)) {
            root.style.setProperty(variable, value);
        }
        // Announce the change to screen readers
        const announcement = document.getElementById('color-scheme-announcement');
        announcement.textContent = `Color scheme changed to ${scheme}.`;
    } else {
        // Fallback to default scheme and notify the user
        applyColorScheme('default');
        const announcement = document.getElementById('color-scheme-announcement');
        announcement.textContent = `Selected color scheme not found. Reverting to default scheme.`;
    }
}

// Event Listener for Color Scheme Selector
document.getElementById('color-scheme').addEventListener('change', function () {
    const selectedScheme = this.value;
    applyColorScheme(selectedScheme);
    localStorage.setItem('selectedColorScheme', selectedScheme);
    this.focus(); // Maintain focus on the select element
});

// Apply Saved Scheme on Page Load
document.addEventListener('DOMContentLoaded', () => {
    const savedScheme = localStorage.getItem('selectedColorScheme') || 'default';
    applyColorScheme(savedScheme);
    document.getElementById('color-scheme').value = savedScheme;
});
