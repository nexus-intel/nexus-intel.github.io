async function loadSharedComponents() {
    // Detect root path based on script location or window global
    const ROOT_PATH = window.ROOT_PATH || '';
    
    const components = [
        { selector: 'header', file: 'header.html' },
        { selector: 'footer', file: 'footer.html' }
    ];

    for (const comp of components) {
        let el = document.querySelector(comp.selector);
        if (!el) el = document.getElementById(comp.selector + '-placeholder');
        if (el) {
            try {
                const response = await fetch(`${ROOT_PATH}${comp.file}`);
                const text = await response.text();
                
                // Adjust links in the loaded HTML to be relative to the current page
                let adjustedText = text;
                if (ROOT_PATH) {
                    adjustedText = text.replace(/href="(?!http|#)([^"]+)"/g, `href="${ROOT_PATH}$1"`);
                    adjustedText = adjustedText.replace(/src="(?!http)([^"]+)"/g, `src="${ROOT_PATH}$1"`);
                }
                
                el.innerHTML = adjustedText;
                
                // Dispatch event so other scripts know header is loaded
                window.dispatchEvent(new CustomEvent('componentLoaded', { detail: comp.id }));
            } catch (err) {
                console.warn(`Failed to load ${comp.file}:`, err);
            }
        }
    }
}

document.addEventListener('DOMContentLoaded', loadSharedComponents);
