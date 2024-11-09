document.addEventListener("DOMContentLoaded", function() {
    const toggleButtons = document.querySelectorAll('.btn-toggle');

    toggleButtons.forEach(button => {
        const targetCollapse = document.querySelector(button.getAttribute('data-bs-target'));
        const collapseId = targetCollapse.id; 

        if (sessionStorage.getItem(collapseId) === 'open') {
            targetCollapse.classList.add('show');
            button.classList.add('active');
        }
    });

    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetCollapse = document.querySelector(button.getAttribute('data-bs-target'));
            const collapseId = targetCollapse.id;  

            const isOpen = targetCollapse.classList.contains('show');

            toggleButtons.forEach(btn => {
                const otherCollapse = document.querySelector(btn.getAttribute('data-bs-target'));
                if (btn !== button) {
                    otherCollapse.classList.remove('show');
                    btn.classList.remove('active');
                    sessionStorage.setItem(otherCollapse.id, 'closed');
                }
            });

            if (isOpen) {
                targetCollapse.classList.remove('show');
                button.classList.remove('active');
                sessionStorage.setItem(collapseId, 'closed');
            } else {
                targetCollapse.classList.add('show');
                button.classList.add('active');
                sessionStorage.setItem(collapseId, 'open');
            }
        });
    });
});
