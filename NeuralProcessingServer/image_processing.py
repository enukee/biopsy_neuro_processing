import os
import cv2  # OpenCV для обработки изображений
import numpy as np

from model import build, DIVIDER
from report import Report, ReportManager

PATH_TO_MODEL = r'C:\Users\vi\Desktop\dilpom\trained_models\model_8_4.weights.h5'
# Загрузка модели
model = build(PATH_TO_MODEL)

# Менеджерр отчётов
report_manager = ReportManager()


def applying_mask(img, pred):
    # Найдем контуры на бинарном изображении
    contours, _ = cv2.findContours(pred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Создадим копию исходного изображения для наложения контуров
    output_image = img.copy()

    # Создадим маску для прозрачной заливки
    mask = np.zeros_like(output_image, dtype=np.uint8)

    # Заливаем контуры на маске
    cv2.drawContours(mask, contours, -1, (0, 255, 0, 128), thickness=cv2.FILLED)  # Зеленый цвет с прозрачностью 128

    # Наложим маску на исходное изображение
    alpha = 0.2  # Коэффициент прозрачности
    output_image = cv2.addWeighted(output_image, 1, mask, alpha, 0)
    output_image = cv2.drawContours(output_image, contours, -1, (0, 255, 0), 2)
    return output_image


def filter_image(img):
    # бинаризация изображения
    _, thresholded = cv2.threshold(img.astype(np.uint8), 127, 255, cv2.THRESH_BINARY)

    # определение ядра
    kernel = np.ones((3, 3), np.uint8)
    # закрытие пробелов изображения
    closing = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Зададим порог для площади контуров
    area_threshold = 3000
    for contour in contours:
      # Вычислим площадь контура
      area = cv2.contourArea(contour)
      # Если площадь контура меньше порога, закрасим его черным
      if area < area_threshold:
          cv2.drawContours(closing, [contour], -1, (0), thickness=cv2.FILLED)

      else:
          # Найдем выпуклую оболочку для контура
          hull = cv2.convexHull(contour)
          # Заливаем выпуклую оболочку на маске
          cv2.drawContours(closing, [hull], -1, (255), thickness=cv2.FILLED)

    return closing


def create_report(pred):
    contours, _ = cv2.findContours(pred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Создание отчёта
    img_report = Report()

    for contour in contours:
        # Вычислим площадь контура
        area = cv2.contourArea(contour)

        # Вычислим моменты контура
        M = cv2.moments(contour)

        if M["m00"] != 0:
            # Вычислим центр масс контура
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            center = (cX, cY)
        else:
            center = (0, 0)  # или любое другое значение по умолчанию, если контур пустой

        img_report.add_contour(center, area)

    return img_report


def resize(img):
    def find_next_multiple_of_divider(n):
        if n % DIVIDER == 0:
            return n
        else:
            return (n // DIVIDER + 1) * DIVIDER

    # вычисление новых рахмеров
    height, width = img.shape[:2]
    new_width = find_next_multiple_of_divider(width)
    new_height = find_next_multiple_of_divider(height)

    if height == new_height and width == new_width:
        return img

    # создание нового изображения белого цвета
    white_image = np.ones((new_height, new_width, 3), dtype=np.uint8) * 255
    white_image[0:height, 0:width] = img
    return white_image


def process_image(upload_folder, file_path):
    try:
        if not os.path.exists(file_path):
            return None, "File does not exist."

        # Read the image using OpenCV
        image = cv2.imread(file_path, cv2.IMREAD_COLOR)
        if image is None:
            return None, "Unable to read the image file."

        # сохранение размера
        height, width = image.shape[:2]

        # Изменение размера
        image = resize(image)

        raw = np.expand_dims(image, axis=0)  # Изменяем размерность до (1, 256, 256, 3)

        pred = model.predict(raw)  # Получаем predict

        output_image = pred.squeeze().reshape(image.shape[0], image.shape[1]) * 255  # predic t приводим к адекватной размерости в (256, 256)

        output_image = output_image[0:height, 0:width]

        # фильтрация предсказанной маски
        output_image = filter_image(output_image)

        # имя обработанного файла
        processed_file_name = 'processed_' + os.path.basename(file_path)

        # формирование отчёта
        report = create_report(output_image)
        # кеширование отчёта
        report_manager.add_report(processed_file_name, report)

        # наложение макси на исходное изображение
        output_image = applying_mask(image, output_image)

        # Схранение обработанного файла
        processed_image_path = os.path.join(upload_folder, processed_file_name)
        cv2.imwrite(processed_image_path, output_image)

        return processed_image_path, None

    except Exception as e:
        return None, f"Error processing image: {e}"
