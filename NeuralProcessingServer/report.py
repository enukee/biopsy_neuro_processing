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
