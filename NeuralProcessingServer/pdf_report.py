from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.colors import Color
from reportlab.platypus import Table, TableStyle
import matplotlib.pyplot as plt
import io


# Регистрируем шрифт, поддерживающий кириллицу
pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))


def create_boxplot_image(objects_area):
    """
    Создает график коробки с усами на основе данных и возвращает изображение в виде ImageReader.

    :param objects_area: Список значений площадей
    :return: Изображение графика коробки с усами в виде ImageReader
    """
    # Создаем график коробки с усами с использованием matplotlib
    plt.figure(figsize=(8, 6))
    plt.boxplot(objects_area, vert=True, patch_artist=True)

    # Настройка внешнего вида графика
    plt.title('Box Plot of Areas')
    plt.ylabel('Area')
    plt.grid(True)

    # Сохраняем график в буфер
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close()
    img_buffer.seek(0)

    # Возвращаем изображение в виде ImageReader
    return ImageReader(img_buffer)


def create_histogram_image(objects_area):
    """
    Создает гистограмму на основе данных и возвращает изображение в виде ImageReader.

    :param objects_area: Список значений площадей
    :return: Изображение гистограммы в виде ImageReader
    """
    # Создание гистограмму с использованием matplotlib
    plt.hist(objects_area, bins=20, color='skyblue', edgecolor='black')
    plt.title('Распределение площади')
    plt.xlabel('Площадь')
    plt.ylabel('Частота')

    # Сохранение гистограмму в буфер
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close()
    img_buffer.seek(0)

    return ImageReader(img_buffer)


def create_table(c, table_data, x_position, y_position):
    """
    Создает и рисует таблицу на PDF странице.

    :param c: Объект Canvas для рисования
    :param table_data: Данные для таблицы
    :param x_position: Начальная позиция по оси X для таблицы
    :param y_position: Начальная позиция по оси Y для таблицы
    """
    table_data.insert(0, ["Index", "X", "Y", "Area"])
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), Color(0.27, 0.41, 0.93)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Arial'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), Color(0.66, 0.72, 0.94)),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    table.wrapOn(c, 0, 0)
    table.drawOn(c, x_position, y_position)


def create_pdf(report):
    """
    Создает PDF отчет на основе данных из объекта Report.

    :param report: Объект Report
    :return: PDF файл в виде байтового объекта
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Заголовок
    c.setFont("Arial", 16)
    c.drawString(100, 750, "Список обнаруженных клубочков почек")

    # Получаем данные из отчета
    objects_center = report.get_report()['ObjectsCenter']
    objects_area = report.get_report()['ObjectsArea']

    count = len(objects_area)

    # Создаем данные для таблицы
    column = 0
    table_data = []
    for i, (center, area) in enumerate(zip(objects_center, objects_area), start=1):
        table_data.append([i, center[0], center[1], area])
        if i % 35 == 0 or i >= count:
            # Создание таблицы
            create_table(c, table_data, 50 + column * 170, 720 - len(table_data) * 20)
            table_data.clear()
            column += 1
            if column == 2:
                column = 0
                c.showPage()  # Создаем новую страницу
                c.setFont("Arial", 16)

    c.showPage()
    # Заголовок
    c.setFont("Arial", 16)
    c.drawString(100, 750, "Диаграммы")

    # Создание гистограммы
    histogram_img = create_histogram_image(objects_area)
    c.drawImage(histogram_img, 50, 500, width=400, height=300)

    # Создание boxplot
    histogram_img = create_boxplot_image(objects_area)
    c.drawImage(histogram_img, 50, 100, width=400, height=300)

    c.save()
    buffer.seek(0)
    return buffer
