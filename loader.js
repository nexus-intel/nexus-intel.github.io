async function loadSharedComponents() {
    try {
        // Load Header
        const headerRes = await fetch('/header.html');
        const headerHtml = await headerRes.text();
        document.querySelector('header').innerHTML = headerHtml;

        // Load Footer
        const footerRes = await fetch('/footer.html');
        const footerHtml = await footerRes.text();
        const footerPlaceholder = document.querySelector('footer');
        if (footerPlaceholder) {
            footerPlaceholder.innerHTML = footerHtml;
        } else {
            const footerEl = document.createElement('footer');
            footerEl.innerHTML = footerHtml;
            document.body.appendChild(footerEl);
        }
    } catch (err) {
        console.error('Failed to load shared components:', err);
    }
}

document.addEventListener('DOMContentLoaded', loadSharedComponents);
