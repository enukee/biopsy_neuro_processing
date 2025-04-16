import os


def transliterate(text):
    # Словарь для транслитерации русских букв в английские
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'x', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
        'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch',
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya', ' ': '_'
    }

    # Применяем транслитерацию ко всем символам в строке
    return ''.join(translit_dict.get(char, char) for char in text)


def transliterate_file(path_file):
    # извлечение расширения из пути
    path, extension = os.path.splitext(path_file)

    # извлечение имени файла
    directory, filename = os.path.split(path)

    # замена русских символов
    new_filename = transliterate(filename)

    # формирование нового пути файла
    new_path_file = '\\'.join([directory, new_filename])

    count = 1
    copy_path_file = new_path_file
    while os.path.exists(copy_path_file + extension):
        copy_path_file = ''.join([new_path_file, '_copy', str(count)])
        count += 1

    new_path_file = ''.join([copy_path_file, extension])

    os.rename(path_file, new_path_file)
    return new_path_file


# transliterate_file(r'C:\Users\vi\Desktop\dilpom\datasets_komochki\почки х 10 0007.jpg')
