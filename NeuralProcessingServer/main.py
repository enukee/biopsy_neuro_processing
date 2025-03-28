import os
from flask import Flask, request, jsonify, send_file
import cv2  # OpenCV для обработки изображений
import numpy as np
from model import build

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Load the model once at the start
model = build()

app = Flask(__name__)

# Укажите директорию для сохранения загруженных файлов
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

        # Resize the image to the model's expected input size
        image = cv2.resize(image, (256, 256))

        # Preprocess the image for the model
        raw = np.expand_dims(image, axis=0) / 255.0  # Normalize pixel values to [0, 1]

        # Make a prediction using the model
        pred = model.predict(raw)

        # Post-process the prediction
        pred = pred.squeeze()  # Remove the batch dimension
        pred = (pred * 255).astype(np.uint8)  # Scale to [0, 255] and convert to uint8

        # Save the processed image
        processed_image_path = os.path.join(UPLOAD_FOLDER, 'processed_' + os.path.basename(file_path))
        cv2.imwrite(processed_image_path, pred)

        return processed_image_path

    except Exception as e:
        # Log the error and return None or handle it as needed
        print(f"Error processing image: {e}")
        return None


if __name__ == '__main__':
    app.run(debug=True)
