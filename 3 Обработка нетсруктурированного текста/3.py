import PyPDF2
import re
# сделано запись списка рассказов в файл story_list.txt
# сделать:
# обработку вложенности
# сортировку названий рассказов
# запись текста рассказа в файл
def page_converting(page_content):
    print("page_content: "+page_content)
    # делим по переносу строки
    for i in range(1, len(page_content)):
        content = page_content.split("\n")
    content.pop(0)
    content.pop(0)
    return content

# фукнция для обработки исключения с переносом строки в содержании
# аргументы:    previous_str - строка до переноса, с которой нужно соединить оставшуюся часть названия
#               str - строка вида strint - "слипшийся" кусочек названия с номером страницы
# возвращает строку вида "title page_number"
def remove_line_break(previous_str, str):
    for i in range(len(str)):
        # когда в строке с исключением встречаем цифру, делим её на две строки: название и номер страницы
        if str[i].isdigit():
            page_number = "".join(reversed(str[:i-1:-1]))
            title = str[:i]
            break
    # возвращаем исправленное название с номером страницы
    return previous_str + " " + title + " " + page_number

def handle_exeptions(caption_str):
    # получаем список рассказов из содержания
    caption_list = caption_str.split("\n")
    result = []
    # по строкам
    for s in range(1, len(caption_list) - 1):
        result_title = ""
        # по символам в строке
        for i in range(len(caption_list[s])):
            str = caption_list[s]
            if caption_list[s][i] == r"\s":
                caption_list[s].pop(i)
            # если перед цифрой стоит буквенный символ - то это исключение
            if caption_list[s][i].isdigit() and caption_list[s][i - 1].isalpha():
                print("\nНайдено исключение: " + caption_list[s])
                print("Предыдущий: " + caption_list[s - 1])
                # вызываем функцию для обработки исключения
                result_title = remove_line_break(caption_list[s-1], caption_list[s])
                print("Результат:" + result_title + "\n")
                result.pop()
                break
            else:
                result_title = result_title + caption_list[s][i]
        result.append(result_title)
    return(result)

if __name__ == '__main__':
    with open("Chehov.pdf", "rb") as file:
        # Создание объекта PdfFReader
        reader = PyPDF2.PdfReader(file)

        # Получение кол-ва страниц
        pages_count = len(reader.pages)

        # создаем двумерный массив для записи пар название рассказа - страница
        content_list = []
        story_title, page_number = "", ""
        content_str = ""

        # записываем список рассказов в файл story_list.txt
        f = open("story_list.txt", "w", encoding="utf-8")
        for i in range(3, 18):
            n = 0
            # получаем содержимое страницы
            page_content = reader.pages[i].extract_text()
            r = page_converting(page_content)
            # конвертируем строку в массив
            content_list = content_list + r
            content_str = content_str + "".join(page_content)

            # записываем страницу с названиями
            f.write(page_content[5:])

            # на стыке страниц добавляем перенос строки
            f.write("\n")
            n+=1
        f.close()

        # получилось удалить \xa0
        # осталось убрать ненужны проверки выше и переписать обработку строк
        content_str = re.sub(r"[^\S\n]", " ", content_str)
        print("content: "+content_str)
        # поиск и обработка исключений
        result_titles = handle_exeptions(content_str)
        print(result_titles)
        sorted(result_titles)

        f = open(f"result_titles.txt", "w+", encoding="utf-8")
        for i in range(len(result_titles)):
            f.write(result_titles[i]+"\n")
        f.close()
