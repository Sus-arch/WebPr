document.addEventListener('DOMContentLoaded', function() {
    function hideMessages() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        });
    }

    document.querySelectorAll('.alert .btn-close').forEach(button => {
        button.addEventListener('click', hideMessages);
    });

    setTimeout(hideMessages, 5000);

    const currentPath = window.location.pathname;

    if (currentPath.includes('/accounts/login/')) {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            const alertText = alert.textContent;
            if (!alertText.includes('Вход') && !alertText.includes('Login') &&
                !alertText.includes('ошибк') && !alertText.includes('error')) {
                alert.remove();
            }
        });
    }
});