function startProgress(progress) {
    const progressBar = document.getElementById('progressBar');
    if (progress < 0) {
        progress = 0;
    } else if (progress > 100) {
        progress = 100;
    }
    progressBar.style.width = progress + '%';
    progressBar.textContent = progress + '%';
}