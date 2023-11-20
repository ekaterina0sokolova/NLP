import requests
import json
import os
import wget
import re
from pymorphy3 import MorphAnalyzer

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

print("Все файлы загружены!\n")

lemm_dict = dict()
morf = MorphAnalyzer()

print("Файлы обрабатываются...")
for file_name in file_name_list:
    path = f"C:/Users/Admin/Desktop/5 семестр/Автоматическая обработка текста/books_before/{file_name}"
    # path = "test.txt"
    print(f"{file_name}...")
    with open(path, "r", encoding="utf-8") as input_file:
        for line in input_file:
            line = re.sub('[^A-Za-zА-Яа-я0-9]+', ' ', line)
            for word in line.split():
                result_lemm = morf.parse(word)[0].normal_form
                if result_lemm.lower() not in lemm_dict:
                    lemm_dict[result_lemm.lower()] = 1
                else:
                    lemm_dict[result_lemm.lower()] += 1

lemm_list = []

for k, v in lemm_dict.items():
    lemm_list.append((v, k))
lemm_list.sort(reverse=True)
with open("result_lemms.txt", "w", encoding="utf-8") as output_file:
    rank = 1
    for j in range(len(lemm_list)-1):
        output_file.write(str(rank)+" "+str(lemm_list[j][1])+" "+str(lemm_list[j][0])+"\n")
        if int(lemm_list[j+1][0]) != int(lemm_list[j][0]):
            rank += 1

