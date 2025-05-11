window.downloadFileFromBase64 = (fileName, base64Data) => {
    const linkSource = base64Data;
    const downloadLink = document.createElement("a");
    downloadLink.href = linkSource;
    downloadLink.download = fileName;
    downloadLink.click();
};

window.loadingAnimation = {
    start: function (elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            let dots = '';
            const interval = setInterval(function () {
                dots = dots.length >= 3 ? '' : dots + '.';
                element.innerText = `Загрузка${dots}`;
            }, 500);

            // Возвращаем интервал, чтобы его можно было остановить позже
            return interval;
        }
    },
    stop: function (intervalId) {
        clearInterval(intervalId);
    }
};
