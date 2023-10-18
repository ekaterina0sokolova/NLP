import PyPDF2
import csv
import re

# убираем перенос строки в исключениях и записываем названия и номера страниц в массив
def get_title_and_page(previous_str, str):
    title, page_number = "", ""
    for i in range(len(str)):
        # когда в строке с исключением встречаем цифру, делим её на две строки: название и номер страницы
        if str[i].isdigit() and len(str[i:len(str)]) <= 4:
            page_number = "".join(reversed(str[:i - 1:-1]))
            title = str[:i]
            break
    # возвращаем исправленное название с номером страницы
    return previous_str + " " + title + " " + page_number

# создаем список названий рассказов
def get_correct_titles(titles_list):
    result = []
    result_result = []
    # по содержанию
    for i in range(2, len(titles_list)-2):
        in_exp = False
        result_title = ""
        # о символам в сроке
        for j in range(len(titles_list[i])):
            # название рассказа в три строки
            if "чугунных" in titles_list[i]:
                result_title = 'Список экспонентов, удостоенных чугунных медалей по русскому отделу на выставке в Амстердаме 1097'
                i += 2
                break
            # если перед цифрой стоит буквенный символ - то это исключение
            if titles_list[i][j].isdigit() and (titles_list[i][j-1].isalpha() or titles_list[i][j-1] == "?"):
                result_title = get_title_and_page(titles_list[i-1], titles_list[i])
                print("\nНайдено исключение: " + titles_list[i])
                print("Предыдущий: " + titles_list[i - 1])
                print("Результат: " + result_title + "\n")
                result_result.pop()
                result.pop()
                break
            else:
                result_title = result_title + titles_list[i][j]
        # разделяем по пробелу
        title = result_title.rpartition(' ')[0]
        page = result_title.rpartition(' ')[2]

        #
        # проверку проходит, но брейк переходит сразу к ретерну
        #
        #
        if title == "«О марте. Об апреле. О мае. Об июне и":
            title = "«О марте. Об апреле. О мае. Об июне и июле. Об августе»"
            page = "1311"
            titles_list.pop(i+1)
            continue

        # не добавляем части (I, IV и т.п.) в список
        for exp in exceptions:
            if exp in title:
                in_exp = True
                break
        if not in_exp:
            result.append(title)
            result_result.append([title, page])

    return result, result_result

exceptions = [
    "I",
    "Глава",
    "V",
    "Действие"
]

spez_symb = ["?", "."]

# записывает в файл текст рассказа
def write_story():
    pass

if __name__ == '__main__':
    # строка с содержанием
    content_str = ""
    titles_list = []
    with open("Chehov.pdf", "rb") as file:
        # Создание объекта PdfFReader
        reader = PyPDF2.PdfReader(file)

        # Получение кол-ва страниц
        pages_count = len(reader.pages)

        for i in range(3, 18):
            # добаляем в содержание текст страницы
            page_content = reader.pages[i].extract_text()
            # удаляем переносы в начале страницы
            page_content = "\n" + page_content[5:]
            # print("page_content: "+page_content)
            content_str = content_str + page_content
        titles_list = content_str.split("\n")

        # словарь с названиями, парами [название, страница]
        result_titles1, result_titles2 = get_correct_titles(titles_list)

        # сортируем список рассказов
        sorted_title_list = sorted(result_titles2)
        print(result_titles2)

        # запись названий в csv файл
        with open("Titles.csv", "w+", newline="") as file:
            wr = csv.writer(file, delimiter="\n")
            wr.writerow(sorted_title_list)

        print("Обрабатываются...")
        # создание файла с текстом рассказа
        for i in range(len(result_titles2)-1):
            # получение номеров страниц начала и конца рассказа
            start_page = int(result_titles2[i][1])
            end_page = int(result_titles2[i + 1][1])


            print(result_titles2[i][0] + " " + str(start_page) + "-" + str(end_page))

            # проверяем началась ли вложенность
            if start_page == end_page:
                continue

            # удаление символов ?, <, >
            file_name = re.sub(r"[.?<>]", "", result_titles2[i][0])
            with open(f'texts/{file_name}.txt', "w+", encoding="utf-8") as file:
                # получение текста рассказа
                for page in range(start_page-1, end_page-1):

                    story_text = reader.pages[page].extract_text()
                    # удаляем переносы в начале страницы
                    file.writelines(story_text)

