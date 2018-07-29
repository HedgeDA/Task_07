import os
import json
import operator


# функция опредялющая в качестве ключа сортировки длинну значения списка
def length(list_item):
    return len(list_item)


def get_all_words(path):
    # определяем переменную - результат выполнения функции
    result = {}

    with open(path, 'rb') as fp:
        # читаем json файл
        file_data = json.load(fp)

        for news in file_data['rss']['channel']['items']:
            # получаем все слова новости, разделяя их по пробелу
            words = news['description'].split(' ')

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
            if file_extension.lower() == '.json':
                # получаем список самых длинных слов (не более 10 слов, длиной от 6 символов)
                words = get_words(path)

                # выводим имя обработанного файла
                print('Файл:', path, 'самые частые', len(words), 'слов:')

                # выводим слова
                for word in words:
                    print('    слово "' + str(word[0]) + '", встречается ' + str(word[1]) + ' раз')

                print()


main()
