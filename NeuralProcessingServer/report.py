class Report:
    def __init__(self):
        # Отчёт об объектах изображения
        self.__centers = []
        self.__areas = []

    def add_contour(self, center, area):
        self.__centers.append(center)
        self.__areas.append(area)

    def get_report(self):
        data = {
            "ObjectsCenter": self.__centers,
            "ObjectsArea": self.__areas
        }
        return data

    def clear(self):
        self.__centers.clear()
        self.__areas.clear()

    @classmethod
    def from_json(cls, json_data):
        """
        Создает объект Report из JSON данных.

        :param json_data: JSON данные, содержащие ObjectsCenter и ObjectsArea
        :return: Объект Report
        """
        report = cls()

        # Проверяем наличие необходимых ключей в JSON данных
        if 'ObjectsCenter' not in json_data or 'ObjectsArea' not in json_data:
            raise ValueError("The JSON data must contain both 'ObjectsCenter' and 'ObjectsArea'.")

        objects_center = json_data['ObjectsCenter']
        objects_area = json_data['ObjectsArea']

        # Проверка, что количество элементов в ObjectsCenter и ObjectsArea совпадает
        if len(objects_center) != len(objects_area):
            raise ValueError("The data is incorrect. "
                             "Different number of ObjectsArea and ObjectCenter parameters.")

        for center, area in zip(objects_center, objects_area):
            report.add_contour(center, area)

        return report


class ReportManager:
    def __init__(self):
        # Инициализация словаря для хранения отчетов
        self.reports = {}

    def add_report(self, filename, report):
        """
        Добавление отчета в словарь.

        :param filename: Имя обработанного файла (уникальный ключ)
        :param report: Отчет об обработке
        """
        if filename in self.reports:
            raise ValueError("The report for this file already exists.")
        self.reports[filename] = report

    def get_report(self, filename):
        """
        Получение отчета по имени файла.

        :param filename: Имя обработанного файла
        :return: Отчет об обработке
        """
        if filename not in self.reports:
            raise ValueError("There is no report for this file.")
        return self.reports[filename]

    def remove_report(self, filename):
        """
        Удаление отчета по имени файла.

        :param filename: Имя обработанного файла
        """
        if filename not in self.reports:
            raise ValueError("There is no report for this file.")
        del self.reports[filename]
