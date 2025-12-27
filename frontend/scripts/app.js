/**
 * Conference Registration Website - Main JavaScript
 * Handles slideshow functionality, form validation, and form submission
 */

// Configuration
// Automatically uses correct API URL based on environment
const CONFIG = {
    // Use localhost for development, Render backend URL for production
    apiUrl: window.location.hostname === 'localhost'
        ? 'http://localhost:8000/api'
        : 'https://iyc-registration-form.onrender.com/api',  // Render backend URL
    slideInterval: 5000, // 5 seconds
};

// ============================================
// SLIDESHOW FUNCTIONALITY
// ============================================

class Slideshow {
    constructor() {
        this.currentSlide = 0;
        this.slides = document.querySelectorAll('.slide');
        this.totalSlides = this.slides.length;
        this.autoPlayInterval = null;
        this.init();
    }

    init() {
        // Create dot indicators
        this.createDots();

        // Set up event listeners
        document.getElementById('prevBtn').addEventListener('click', () => this.prevSlide());
        document.getElementById('nextBtn').addEventListener('click', () => this.nextSlide());

        // Start autoplay
        this.startAutoPlay();

        // Pause on hover
        const slideshow = document.getElementById('slideshow');
        slideshow.addEventListener('mouseenter', () => this.stopAutoPlay());
        slideshow.addEventListener('mouseleave', () => this.startAutoPlay());
    }

    createDots() {
        const dotsContainer = document.getElementById('slideDots');
        for (let i = 0; i < this.totalSlides; i++) {
            const dot = document.createElement('span');
            dot.className = 'dot' + (i === 0 ? ' active' : '');
            dot.addEventListener('click', () => this.goToSlide(i));
            dotsContainer.appendChild(dot);
        }
    }

    showSlide(index) {
        // Remove active class from all slides and dots
        this.slides.forEach(slide => slide.classList.remove('active'));
        document.querySelectorAll('.dot').forEach(dot => dot.classList.remove('active'));

        // Add active class to current slide and dot
        this.slides[index].classList.add('active');
        document.querySelectorAll('.dot')[index].classList.add('active');

        this.currentSlide = index;
    }

    nextSlide() {
        const next = (this.currentSlide + 1) % this.totalSlides;
        this.showSlide(next);
    }

    prevSlide() {
        const prev = (this.currentSlide - 1 + this.totalSlides) % this.totalSlides;
        this.showSlide(prev);
    }

    goToSlide(index) {
        this.showSlide(index);
        this.stopAutoPlay();
        this.startAutoPlay();
    }

    startAutoPlay() {
        this.autoPlayInterval = setInterval(() => this.nextSlide(), CONFIG.slideInterval);
    }

    stopAutoPlay() {
        if (this.autoPlayInterval) {
            clearInterval(this.autoPlayInterval);
            this.autoPlayInterval = null;
        }
    }
}

// ============================================
// FORM VALIDATION
// ============================================

class FormValidator {
    constructor(formId) {
        this.form = document.getElementById(formId);
        this.errors = {};
    }

    validateField(fieldId, validationFn, errorMessage) {
        const field = document.getElementById(fieldId);
        const value = field.value.trim();
        const errorElement = document.getElementById(`${fieldId}Error`);
        const formGroup = field.closest('.form-group');

        if (!validationFn(value)) {
            this.errors[fieldId] = errorMessage;
            errorElement.textContent = errorMessage;
            errorElement.classList.add('show');
            formGroup.classList.add('error');
            return false;
        } else {
            delete this.errors[fieldId];
            errorElement.textContent = '';
            errorElement.classList.remove('show');
            formGroup.classList.remove('error');
            return true;
        }
    }

    validateRequired(fieldId, fieldName) {
        return this.validateField(
            fieldId,
            value => value.length > 0,
            `${fieldName} is required`
        );
    }

    validateEmail(fieldId) {
        const email = document.getElementById(fieldId).value.trim();
        if (!email) return true; // Email is optional

        return this.validateField(
            fieldId,
            value => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
            'Please enter a valid email address'
        );
    }

    validatePhone(fieldId) {
        const phone = document.getElementById(fieldId).value.trim();
        if (!phone) return true; // Phone is optional

        return this.validateField(
            fieldId,
            value => {
                // Remove spaces and dashes
                const cleaned = value.replace(/[\s\-]/g, '');
                // Check Ghana phone formats
                return /^(0\d{9}|\+233\d{9}|233\d{9})$/.test(cleaned);
            },
            'Please enter a valid Ghana phone number (e.g., 0241234567 or +233241234567)'
        );
    }

    validateConsent() {
        const checkbox = document.getElementById('privacyConsent');
        const errorElement = document.getElementById('consentError');
        const formGroup = checkbox.closest('.form-group');

        if (!checkbox.checked) {
            this.errors.consent = 'You must agree to the privacy terms to register';
            errorElement.textContent = this.errors.consent;
            errorElement.classList.add('show');
            formGroup.classList.add('error');
            return false;
        } else {
            delete this.errors.consent;
            errorElement.textContent = '';
            errorElement.classList.remove('show');
            formGroup.classList.remove('error');
            return true;
        }
    }

    validateAll() {
        let isValid = true;

        // Validate required fields only
        isValid = this.validateRequired('fullName', 'Full name') && isValid;
        isValid = this.validateRequired('church', 'Church') && isValid;
        isValid = this.validateRequired('city', 'City/Location') && isValid;

        // Validate optional fields if provided
        isValid = this.validatePhone('phone') && isValid;
        isValid = this.validateEmail('email') && isValid;

        // Validate privacy consent
        isValid = this.validateConsent() && isValid;

        return isValid;
    }

    clearErrors() {
        this.errors = {};
        document.querySelectorAll('.error-message').forEach(el => {
            el.textContent = '';
            el.classList.remove('show');
        });
        document.querySelectorAll('.form-group').forEach(el => {
            el.classList.remove('error');
        });
    }
}

// ============================================
// FORM SUBMISSION
// ============================================

class RegistrationForm {
    constructor() {
        this.form = document.getElementById('registrationForm');
        this.validator = new FormValidator('registrationForm');
        this.submitBtn = document.getElementById('submitBtn');
        this.init();
    }

    init() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));

        // Add real-time validation
        this.addRealtimeValidation();
    }

    addRealtimeValidation() {
        // Validate required fields on blur
        document.getElementById('fullName').addEventListener('blur', () =>
            this.validator.validateRequired('fullName', 'Full name'));

        document.getElementById('church').addEventListener('blur', () =>
            this.validator.validateRequired('church', 'Church'));

        document.getElementById('city').addEventListener('blur', () =>
            this.validator.validateRequired('city', 'City/Location'));

        // Validate optional fields on blur (only if they have a value)
        document.getElementById('phone').addEventListener('blur', () =>
            this.validator.validatePhone('phone'));

        document.getElementById('email').addEventListener('blur', () =>
            this.validator.validateEmail('email'));

        document.getElementById('privacyConsent').addEventListener('change', () =>
            this.validator.validateConsent());
    }

    async handleSubmit(e) {
        e.preventDefault();

        // Clear previous alerts
        document.getElementById('alertContainer').innerHTML = '';

        // Validate form
        if (!this.validator.validateAll()) {
            this.showAlert('Please fix the errors in the form', 'error');
            return;
        }

        // Prepare form data
        const formData = this.getFormData();

        // Show loading state
        this.setLoadingState(true);

        try {
            // Submit to API
            const response = await this.submitRegistration(formData);

            if (response.success) {
                // Store configuration for thank you page
                this.storeConfig();

                // Redirect to thank you page
                const encodedName = encodeURIComponent(formData.full_name);
                window.location.href = `thank-you.html?name=${encodedName}`;
            } else {
                this.showAlert(response.message || 'Registration failed. Please try again.', 'error');
                this.setLoadingState(false);
            }
        } catch (error) {
            console.error('Registration error:', error);
            this.showAlert(
                'Unable to connect to the server. Please check your internet connection and try again.',
                'error'
            );
            this.setLoadingState(false);
        }
    }

    getFormData() {
        const formData = {
            full_name: document.getElementById('fullName').value.trim(),
            phone: document.getElementById('phone').value.trim(),
            church: document.getElementById('church').value.trim(),
            institution: document.getElementById('institution').value.trim(),
            city: document.getElementById('city').value.trim(),
            leader: document.getElementById('leader').value.trim(),
            email: document.getElementById('email').value.trim() || null,
            contact_method: document.getElementById('contactMethod').value || null,
            first_time_attendee: document.querySelector('input[name="first_time_attendee"]:checked')?.value || null,
            prayer_request: document.getElementById('prayerRequest').value.trim() || null,
            privacy_consent: document.getElementById('privacyConsent').checked,
        };

        return formData;
    }

    async submitRegistration(formData) {
        const response = await fetch(`${CONFIG.apiUrl}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });

        if (!response.ok) {
            if (response.status === 429) {
                throw new Error('Too many requests. Please wait a moment and try again.');
            }
            const errorData = await response.json();
            throw new Error(errorData.detail?.message || 'Registration failed');
        }

        return await response.json();
    }

    setLoadingState(isLoading) {
        if (isLoading) {
            this.submitBtn.disabled = true;
            this.submitBtn.classList.add('loading');
            this.submitBtn.textContent = '';
        } else {
            this.submitBtn.disabled = false;
            this.submitBtn.classList.remove('loading');
            this.submitBtn.textContent = 'Register Now';
        }
    }

    showAlert(message, type = 'error') {
        const alertContainer = document.getElementById('alertContainer');
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.textContent = message;
        alertContainer.appendChild(alert);

        // Scroll to alert
        alert.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        // Auto-remove after 5 seconds
        setTimeout(() => {
            alert.remove();
        }, 5000);
    }

    storeConfig() {
        // Store config in localStorage for thank you page
        // In production, these would come from your backend
        // For now, we'll use placeholder values
        localStorage.setItem('whatsappLink', 'https://chat.whatsapp.com/your_invite_link');
        localStorage.setItem('facebookUrl', 'https://facebook.com/your_page');
        localStorage.setItem('youtubeUrl', 'https://youtube.com/@your_channel');
    }
}

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize slideshow
    new Slideshow();

    // Initialize registration form
    new RegistrationForm();

    // Handle logo fallback
    const logo = document.getElementById('logo');
    if (logo) {
        logo.addEventListener('error', function () {
            // Hide logo if image fails to load
            this.style.display = 'none';
        });
    }

    // Set social media links
    const facebookLink = document.getElementById('facebookLink');
    const youtubeLink = document.getElementById('youtubeLink');

    if (facebookLink) {
        facebookLink.href = 'https://www.facebook.com/int.youthforchrist';
    }
    if (youtubeLink) {
        youtubeLink.href = 'https://www.youtube.com/@Int.YouthForChrist';
    }

    console.log('IYC Conference Registration - Ready');
});
