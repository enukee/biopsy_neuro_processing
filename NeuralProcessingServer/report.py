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
