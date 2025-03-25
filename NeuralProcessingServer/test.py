import cv2
import numpy as np


def test_processing(model, file_path):
    window_name = 'Predicted Image'

    CLR = cv2.IMREAD_COLOR
    img = cv2.imread(file_path, CLR)
    cv2.imshow(window_name, img)
    img = cv2.resize(img, (256, 256))  # По её окончанию читаем картинку
    raw = np.expand_dims(img, axis=0)  # Изменяем размерность до (1, 256, 256, 3)
    pred = model.predict(raw)  # Получаем predict
    pred = pred.squeeze().reshape(256, 256) * 255  # predic t приводим к адекватной размерости в (256, 256)
    cv2.imwrite("SomeResults.png", pred)  # сохраняем результат
    cv2.imshow(window_name, pred)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
