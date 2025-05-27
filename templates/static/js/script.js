// Back to Top Button
const backToTopButton = document.getElementById('backToTop');

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        backToTopButton.classList.remove('opacity-0', 'invisible');
        backToTopButton.classList.add('opacity-100', 'visible');
    } else {
        backToTopButton.classList.remove('opacity-100', 'visible');
        backToTopButton.classList.add('opacity-0', 'invisible');
    }
});

backToTopButton.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});


document.getElementById('mobileMenuButton').addEventListener('click', function() {
    document.getElementById('mobileMenu').classList.toggle('hidden');
});

// Accordion functionality for FAQ
document.querySelectorAll('.accordion-button').forEach(button => {
    button.addEventListener('click', function() {
        const content = this.nextElementSibling;
        const icon = this.querySelector('i');
        
        content.classList.toggle('hidden');
        icon.classList.toggle('fa-chevron-down');
        icon.classList.toggle('fa-chevron-up');
    });
});

// Star rating interaction
document.querySelectorAll('.rating-input label').forEach(star => {
    star.addEventListener('mouseover', function() {
        const stars = this.parentElement.querySelectorAll('label');
        const index = Array.from(stars).indexOf(this);
        
        stars.forEach((s, i) => {
            if (i <= index) {
                s.classList.add('text-yellow-400');
                s.classList.remove('text-gray-300');
            }
        });
    });
    
    star.addEventListener('mouseout', function() {
        const stars = this.parentElement.querySelectorAll('label');
        const checked = this.parentElement.querySelector('input:checked');
        
        if (!checked) {
            stars.forEach(s => {
                s.classList.remove('text-yellow-400');
                s.classList.add('text-gray-300');
            });
        } else {
            const checkedIndex = parseInt(checked.value) - 1;
            stars.forEach((s, i) => {
                if (i <= checkedIndex) {
                    s.classList.add('text-yellow-400');
                    s.classList.remove('text-gray-300');
                } else {
                    s.classList.remove('text-yellow-400');
                    s.classList.add('text-gray-300');
                }
            });
        }
    });
    
    star.addEventListener('click', function() {
        const input = this.previousElementSibling;
        const stars = this.parentElement.querySelectorAll('label');
        const index = Array.from(stars).indexOf(this);
        
        stars.forEach((s, i) => {
            if (i <= index) {
                s.classList.add('text-yellow-400');
                s.classList.remove('text-gray-300');
            } else {
                s.classList.remove('text-yellow-400');
                s.classList.add('text-gray-300');
            }
        });
    });
});