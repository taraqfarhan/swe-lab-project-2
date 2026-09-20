// FoodFlow Application Client-side Scripts

document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss alert banners after 5 seconds
    const alerts = document.querySelectorAll('.auto-dismiss-alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s ease';
            setTimeout(() => alert.remove(), 500);
        }, 4500);
    });
});

// Quick-fill login demo accounts
function fillDemoAccount(username, password) {
    const userInput = document.getElementById('username');
    const passInput = document.getElementById('password');
    if (userInput && passInput) {
        userInput.value = username;
        passInput.value = password;
        userInput.classList.add('bg-amber-50');
        passInput.classList.add('bg-amber-50');
        setTimeout(() => {
            userInput.classList.remove('bg-amber-50');
            passInput.classList.remove('bg-amber-50');
        }, 800);
    }
}

// Modal open/close helpers
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}
