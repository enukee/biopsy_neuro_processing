import os
from flask import Flask, request, jsonify, send_file

from pdf_report import create_pdf
from report import Report
from transliterate import transliterate_file
from test import test_processing
from image_processing import process_image, report_manager

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

app = Flask(__name__)

# Директория для сохранения загруженных файлов
UPLOAD_FOLDER = 'C://Users//vi//Desktop//dilpom//app//img_processing//'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}


@app.route('/process-image', methods=['POST'])
def proceed_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    files = request.files.getlist('file')

    if len(files) != 1:
        return jsonify({'error': 'Too many source files'}), 400

    file = files[0]

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    # Сохранение файла
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Замена русских букв в имени файла
    file_path = transliterate_file(file_path)

    # Обработка изображения
    processed_image_path, error = process_image(UPLOAD_FOLDER, file_path)

    if error is not None:
        return jsonify({'error': error}), 400

    # Отправка обработанного изображения обратно клиенту
    return send_file(
        processed_image_path,
        as_attachment=True,
        download_name=os.path.basename(processed_image_path)  # Указываем имя файла
    )


@app.route('/report/<filename>', methods=['GET'])
def get_report(filename):
    try:
        if not filename:
            return jsonify({'error': 'The filename parameter was not passed'}), 400

        rep = report_manager.get_report(filename)
        rep = rep.get_report()
        report_manager.remove_report(filename)
        return jsonify(rep)

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/report/pdf', methods=['POST'])
def create_pdf_report():
    try:
        # Получение JSON данные из тела запроса
        data = request.get_json()

        # Проверка, что данные не пустые
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        # Проверка наличия обязательных параметров
        if 'ObjectsCenter' not in data or 'ObjectsArea' not in data:
            return jsonify({'error': 'Missing required parameters: ObjectsCenter or ObjectsArea'}), 400

        # Создание объекта Report из JSON данных
        report = Report.from_json(data)

        # Создание PDF отчета
        pdf = create_pdf(report)

        # Отправка PDF файл в ответе
        return send_file(pdf, as_attachment=True, download_name='report.pdf')

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
