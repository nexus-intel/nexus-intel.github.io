document.addEventListener('DOMContentLoaded', () => {
    // Chatbot Toggle
    const trigger = document.getElementById('chatbot-trigger');
    const widget = document.getElementById('chatbot-widget');
    const closeBtn = document.getElementById('close-chat');

    trigger.addEventListener('click', () => {
        widget.classList.toggle('chatbot-closed');
    });

    closeBtn.addEventListener('click', () => {
        widget.classList.add('chatbot-closed');
    });

    // Chat Logic
    const sendBtn = document.getElementById('send-msg');
    const input = document.querySelector('.chat-input input');
    const messages = document.getElementById('chat-messages');

    const addMessage = (text, isBot = false) => {
        const msg = document.createElement('div');
        msg.className = `message ${isBot ? 'bot-message' : 'user-message'}`;
        msg.textContent = text;
        messages.appendChild(msg);
        messages.scrollTop = messages.scrollHeight;
    };

    const handleSend = () => {
        const text = input.value.trim();
        if (text) {
            addMessage(text);
            input.value = '';
            
            // Simulate bot response
            setTimeout(() => {
                const responses = [
                    "I'd be happy to help you with your AI project!",
                    "Our expertise in OCR can definitely scale your operations.",
                    "We specialize in LangGraph for complex agentic workflows.",
                    "Nexus delivers premium solutions in Python and Go.",
                    "Let's book a discovery call to discuss your RAG implementation."
                ];
                const rand = Math.floor(Math.random() * responses.length);
                addMessage(responses[rand], true);
            }, 1000);
        }
    };

    sendBtn.addEventListener('click', handleSend);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
    });

    // Scroll Animations
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.service-card, .tech-group, .blog-card, .contact-container').forEach(el => {
        observer.observe(el);
    });

    // Form Submissions
    const contactForm = document.getElementById('contact-form');
    const newsletterForm = document.getElementById('newsletter-form');

    const handleFormSubmit = (e, msg) => {
        e.preventDefault();
        const btn = e.target.querySelector('button');
        const originalText = btn.textContent;
        
        btn.textContent = 'Sending...';
        btn.disabled = true;

        setTimeout(() => {
            btn.textContent = 'Success!';
            btn.style.background = '#10b981';
            alert(msg);
            e.target.reset();

            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.background = '';
                btn.disabled = false;
            }, 3000);
        }, 1500);
    };

    if (contactForm) {
        contactForm.addEventListener('submit', (e) => handleFormSubmit(e, 'Message sent successfully! We will get back to you soon.'));
    }

    if (newsletterForm) {
        newsletterForm.addEventListener('submit', (e) => handleFormSubmit(e, 'Thanks for subscribing to our newsletter!'));
    }
});
