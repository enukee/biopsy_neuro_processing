import os
from flask import Flask, request, jsonify, send_file
import cv2  # OpenCV для обработки изображений
import numpy as np
from model import build
from transliterate import transliterate_file
from test import test_processing

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

PATH_TO_MODEL = r'C:\Users\vi\Desktop\dilpom\trained_models\model_7_1.weights.h5'
# Загрузка модели
model = build(PATH_TO_MODEL)

app = Flask(__name__)

# Директория для сохранения загруженных файлов
UPLOAD_FOLDER = 'C://Users//vi//Desktop//dilpom//app//img_processing//'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/proceed', methods=['POST'])
def proceed_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Сохранение файла
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Замена русских букв в имени файла
    file_path = transliterate_file(file_path)

    # Обработка изображения
    processed_image_path = process_image(file_path)

    # Отправка обработанного изображения обратно клиенту
    return send_file(processed_image_path, as_attachment=True)


def process_image(file_path):
    try:
        if os.path.exists(file_path):
            print("File exists.")
        else:
            print("File does not exist.")

        # Read the image using OpenCV
        image = cv2.imread(file_path, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Unable to read the image file.")

        # Изменение размера
        image = cv2.resize(image, (256, 256))

        raw = np.expand_dims(image, axis=0)  # Изменяем размерность до (1, 256, 256, 3)

        pred = model.predict(raw)  # Получаем predict

        pred = pred.squeeze().reshape(256, 256) * 255  # predic t приводим к адекватной размерости в (256, 256)

        # Схранение обработанного файла
        processed_image_path = os.path.join(UPLOAD_FOLDER, 'processed_' + os.path.basename(file_path))
        cv2.imwrite(processed_image_path, pred)

        return processed_image_path

    except Exception as e:
        # Log the error and return None or handle it as needed
        print(f"Error processing image: {e}")
        return None


if __name__ == '__main__':
    app.run(debug=True)
