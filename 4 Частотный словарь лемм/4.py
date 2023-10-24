import requests
import json
import os
import wget

# загрузка текстов с репозитория
json_text = requests.get("https://github.com/nevmenandr/word2vec-russian-novels/tree/master/books_before").text
json_dict = json.loads(json_text)

item_list_len = len(json_dict["payload"]["tree"]["items"])

path = "C://Users/Admin/Desktop/5 семестр/Автоматическая обработка текста/books_before"

# добавление названий в список
file_name_list = []
for i in range(item_list_len):
    file_name_list.append(json_dict["payload"]["tree"]["items"][i]['name'])

# загрузка текстов
if len(file_name_list) != len(os.listdir(path)):
    # загружаем недостающие файлы
    print("Не все файлы загружены...")
    for i in range(len(file_name_list)):
        if os.path.isfile(os.path.join(path)) == file_name_list[i]:
            continue
        else:
            print(f"Загружаем: {file_name_list[i]}")
            link = "https://raw.githubusercontent.com/nevmenandr/word2vec-russian-novels/master/books_before/" + str(file_name_list[i])
            wget.download(link)
print(file_name_list)

print("Все файлы загружены!\n")

# сегментация
for i in range(len(file_name_list)):
    # path = f"books_before/{file_name_list}.txt"
    path = "test.txt"
    with open(path, "r", encoding="utf-8") as file:
        pass


# Формирование общего словаря уникальных лемм слов по всем текстам
# Построить диаграмму, описывающую закон Зипфа
# Рассчитать постоянную Зипфа.
