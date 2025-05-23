import os
from flask import Flask, request, jsonify, send_file
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


@app.route('/proceed', methods=['POST'])
def proceed_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    files = request.files.getlist('file')

    if len(files) != 1:
        return jsonify({'error': 'Please upload exactly one file'}), 400

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


@app.route('/report', methods=['GET'])
def get_report():
    try:
        file_name = request.args.get('requestID')
        if not file_name:
            return jsonify({'error': 'The requestID parameter was not passed'}), 400

        rep = report_manager.get_report(file_name)
        rep = rep.get_report()
        report_manager.remove_report(file_name)
        print(rep)
        return jsonify(rep)

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
