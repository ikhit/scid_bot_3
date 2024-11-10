document.addEventListener("DOMContentLoaded", function() {

    const dataBotToggle = document.getElementById('data-bot-toggle');
    const requestsToggle = document.getElementById('requests-toggle');

    if (localStorage.getItem('dataBotOpen') === 'true') {
        dataBotToggle.checked = true;
    }
    if (localStorage.getItem('requestsOpen') === 'true') {
        requestsToggle.checked = true;
    }

    dataBotToggle.addEventListener('change', function() {
        localStorage.setItem('dataBotOpen', dataBotToggle.checked);
    });

    requestsToggle.addEventListener('change', function() {
        localStorage.setItem('requestsOpen', requestsToggle.checked);
    });
});
