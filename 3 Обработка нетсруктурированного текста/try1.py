import PyPDF2
import csv
import io

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

# склеиваем двустрочные названия
def get_correct_titles(titles_list):
    result_result = []
    # по содержанию
    for i in range(2, len(titles_list)-2):
        result_title = ""
        # о символам в сроке
        for j in range(len(titles_list[i])):
            # если перед цифрой стоит буквенный символ - то это исключение
            if titles_list[i][j].isdigit() and titles_list[i][j-1].isalpha():
                result_title = get_title_and_page(titles_list[i-1], titles_list[i])
                print("\nНайдено исключение: " + titles_list[i])
                print("Предыдущий: " + titles_list[i - 1])
                print("Результат: " + result_title + "\n")
                result_result.pop()
                break
            else:
                result_title = result_title + titles_list[i][j]
        # разделяем по пробелу
        title = result_title.rpartition(' ')[0]
        page = result_title.rpartition(' ')[2]
        result_result.append([title, page])
    return result_result


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

        result_titles = get_correct_titles(titles_list)

        # print(content_str)
        print(sorted(result_titles))

        # запись в файл
        with open("Titles.csv", "w+", newline="") as file:
            wr = csv.writer(file)
            for i in range(len(result_titles)):
                wr.writerow(result_titles[i])
