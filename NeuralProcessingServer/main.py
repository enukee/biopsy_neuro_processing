import os
from flask import Flask, request, jsonify, send_file
from transliterate import transliterate_file
from test import test_processing
from image_processing import process_image, img_report

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

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
    processed_image_path = process_image(UPLOAD_FOLDER, file_path)

    # Отправка обработанного изображения обратно клиенту
    return send_file(processed_image_path, as_attachment=True)


@app.route('/report', methods=['GET'])
def get_report():
    if img_report is not None:
        rep = img_report.get_report()
        print(rep)
        return jsonify(rep)

    else:
        return jsonify({'error': 'Report is none'}), 400


if __name__ == '__main__':
    app.run(debug=True)
