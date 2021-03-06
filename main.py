import os
import json
import operator
import xml.etree.ElementTree as ET


# функция опредялющая в качестве ключа сортировки длинну значения списка
def length(list_item):
    return len(list_item)


# функция заполняет слова в словарь из переданной строки
def count_words(result, description):
    # получаем все слова новости, разделяя их по пробелу
    words = description.split(' ')

    # сортируем список с функцией-ключом по длине слова
    words.sort(key=length, reverse=True)

    # формируем результат, добавляя слова и подсчитывая вхождения
    for word in words:
        if len(word) >= 6:
            if result.get(word) is None:
                result[word] = 0
            result[word] += 1
        else:
            break

    return result


# функция получающая все слова с количеством упоминаний
def get_all_words(path):
    # определяем переменную - результат выполнения функции
    result = {}

    if '.xml' in path:
        # xml, дополнительное задание
        tree = ET.parse(path)

        descriptions = tree.findall('channel/item/description')
        for description in descriptions:
            result = count_words(result, description.text)
    else:
        # json
        with open(path, 'rb') as fp:
            file_data = json.load(fp)

            for news in file_data['rss']['channel']['items']:
                result = count_words(result, news['description'])

    return result


# функция получающая первых 10 слов с максимальным числом упоминаний
def get_words(path):
    # получаем словарь всех слов с частотой использования
    words = get_all_words(path)

    # сортируем словарь в обратном порядке, преобразуя результат в список кортежей
    words_sorted = sorted(words.items(), key=operator.itemgetter(1), reverse=True)

    result = list()
    for word in words_sorted:
        result.append(word)

        if len(result) == 10:
            break

    return result


def main():
    # получаем текущую директорию
    current_dir = os.path.dirname(os.path.abspath(__file__))

    if __name__ == '__main__':
        # определяем список файлов в директории
        file_list = os.listdir(current_dir)

        print('Всего файлов:', len(file_list))
        print()

        for path in file_list:
            # пропускаем возможные вложенные директории
            if os.path.isdir(path):
                continue

            # разделяем имя файла и расширение
            file_name, file_extension = os.path.splitext(path)

            # обрабатываем только файлы json
            if file_extension.lower() == '.json' or file_extension.lower() == '.xml':
                # получаем список самых длинных слов (не более 10 слов, длиной от 6 символов)
                words = get_words(os.path.join(current_dir, path))

                # выводим имя обработанного файла
                print('Файл:', path, 'самые частые', len(words), 'слов:')

                # выводим слова
                for word in words:
                    print('    слово "' + str(word[0]) + '", встречается ' + str(word[1]) + ' раз')

                print()


main()
