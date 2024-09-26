document.getElementById('customSelect').addEventListener('click', function() {
    this.classList.toggle('active');
});

document.addEventListener('click', function(event) {
    const select = document.getElementById('customSelect');
    if (!select.contains(event.target)) {
        select.classList.remove('active');
    }
});


