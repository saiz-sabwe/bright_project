// Mobile menu toggle
const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const navMenu = document.querySelector('.nav-menu');
const hamburger = document.querySelector('.hamburger');

mobileMenuToggle.addEventListener('click', function () {
    navMenu.classList.toggle('active');
    hamburger.classList.toggle('active');
});

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    });
});

// Close mobile menu when clicking outside
document.addEventListener('click', function (e) {
    if (!e.target.closest('header')) {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    }
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Fade in animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

document.querySelectorAll('.fade-in').forEach(el => {
    observer.observe(el);
});

// Header scroll effect
window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    if (window.scrollY > 100) {
        header.style.background = 'rgba(255, 255, 255, 0.95)';
        header.style.backdropFilter = 'blur(10px)';
    } else {
        header.style.background = 'var(--white)';
        header.style.backdropFilter = 'none';
    }
});

// Counter animation for stats
const animateCounters = () => {
    const counters = document.querySelectorAll('.stat-number');
    counters.forEach(counter => {
        const target = parseInt(counter.textContent.replace(/[^\d]/g, ''));
        const suffix = counter.textContent.replace(/[\d]/g, '');
        let current = 0;
        const increment = target / 100;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            counter.textContent = Math.floor(current) + suffix;
        }, 20);
    });
};

// Trigger counter animation when parallax section is visible
const parallaxObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            animateCounters();
            parallaxObserver.unobserve(entry.target);
        }
    });
});

const parallaxSection = document.querySelector('.parallax-section');
if (parallaxSection) {
    parallaxObserver.observe(parallaxSection);
}

// Form submission
document.querySelector('.contact-form').addEventListener('submit', function (e) {
    e.preventDefault();
    alert('Merci pour votre message ! Nous vous recontacterons rapidement.');
    this.reset();
});

// Additional enhancements
document.addEventListener('DOMContentLoaded', function () {
    // Performance optimization: throttle scroll events
    function throttle(func, limit) {
        let inThrottle;
        return function () {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    }

    // Enhanced form validation
    function validateForm(form) {
        const name = form.querySelector('#name');
        const email = form.querySelector('#email');
        let isValid = true;

        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (email && !emailRegex.test(email.value)) {
            email.style.borderColor = '#e74c3c';
            isValid = false;
        } else if (email) {
            email.style.borderColor = '';
        }

        // Name validation
        if (name && name.value.trim().length < 2) {
            name.style.borderColor = '#e74c3c';
            isValid = false;
        } else if (name) {
            name.style.borderColor = '';
        }

        return isValid;
    }

    // Enhanced form submission
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();

            if (validateForm(this)) {
                const submitButton = this.querySelector('button[type="submit"]');
                const originalText = submitButton.innerHTML;

                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Envoi en cours...';
                submitButton.disabled = true;

                setTimeout(() => {
                    submitButton.innerHTML = '<i class="fas fa-check"></i> Message envoyé !';
                    submitButton.style.background = '#27ae60';

                    setTimeout(() => {
                        submitButton.innerHTML = originalText;
                        submitButton.style.background = '';
                        submitButton.disabled = false;
                        this.reset();
                    }, 2000);
                }, 1500);
            } else {
                alert('Veuillez corriger les erreurs dans le formulaire.');
            }
        });
    }

    // Keyboard navigation for accessibility
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            navMenu.classList.remove('active');
            hamburger.classList.remove('active');
        }
    });

    // Service cards hover effect
    document.querySelectorAll('.service-card').forEach(card => {
        card.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });

        card.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
});