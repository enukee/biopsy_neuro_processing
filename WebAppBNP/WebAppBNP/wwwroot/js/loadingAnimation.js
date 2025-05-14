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

function clearCanvas(canvasId) {
    const canvas = document.getElementById(canvasId);
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
};

function drawSquare(canvasId, x, y, size, color, text) {
    const canvas = document.getElementById(canvasId);
    const ctx = canvas.getContext('2d');

    // Рисование квадрата
    ctx.fillStyle = color;
    ctx.fillRect(x, y, size, size);

    // Настройка стиля текста
    ctx.fillStyle = 'white'; // Цвет текста
    ctx.font = '10px Arial'; // Размер и шрифт текста
    ctx.textAlign = 'center'; // Выравнивание текста по центру
    ctx.textBaseline = 'middle'; // Выравнивание текста по вертикали

    // Вычисление координат для текста
    const textX = x + size / 2;
    const textY = y + size / 2;

    // Рисование текста
    ctx.fillText(text, textX, textY);
};
