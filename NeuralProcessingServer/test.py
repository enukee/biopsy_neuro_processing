import cv2
import numpy as np


def test_processing(model, file_path):
    window_name = 'Predicted Image'

    CLR = cv2.IMREAD_COLOR
    SIZE = 512
    img = cv2.imread(file_path, CLR)  # По её окончанию читаем картинку
    img = cv2.resize(img, (SIZE, SIZE))
    raw = np.expand_dims(img, 0)  # Изменяем размерность до (1, 256, 256, 3)
    pred = model.predict(raw)  # Получаем predict
    pred = pred.squeeze().reshape(img.shape[0],
                                  img.shape[1]) * 255  # predic t приводим к адекватной размерости в (256, 256)
    pred = cv2.resize(pred, (SIZE, SIZE))
    cv2.imwrite("SomeResults.png", pred)  # сохраняем результат
    cv2.imshow(window_name, pred)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
