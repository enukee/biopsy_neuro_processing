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
