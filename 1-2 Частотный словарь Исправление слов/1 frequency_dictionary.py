import os
import requests
import json
import wget

json_text = requests.get("https://github.com/nevmenandr/word2vec-russian-novels/tree/master/books_before").text
json_dict = json.loads(json_text)

item_list_len = len(json_dict["payload"]["tree"]["items"])

# имена текстов в лист
file_name_list = []
for i in range(item_list_len):
    file_name_list.append(json_dict["payload"]["tree"]["items"][i]['name'])

# загрузка текстов
if len(file_name_list) != len(os.listdir(r"texts")):
    # загружаем недостающие файлы
    print("Не все файлы загружены...")
    for i in range(len(file_name_list)):
        if os.path.isfile(os.path.join(os.curdir+r"texts")) == file_name_list[i]:
            continue
        else:
            print(f"{file_name_list[i]} не загружен")
            link = "https://raw.githubusercontent.com/nevmenandr/word2vec-russian-novels/master/books_before/" + str(file_name_list[i])
            wget.download(link)

print("Все файлы загружены!\n")

# расчет частоты встречаемости символов/слов в словаре
def calculate_freq(dict):
    total = sum(dict.values())
    frequencies = {}
    for char, count in dict.items():
        frequencies[char] = round(count / total, 4)
    return(frequencies)

# общий словарь уникальных симв по всем текстам
unic_symb = dict()
# общий словарь уникальных слов по всем текстам
unic_words = dict()

symbol_list = []
all_words_count = 0

print("Обработка файлов: \n")
for i in range(len(os.listdir(r"books_before"))):
    path = r"books_before\\" + str(file_name_list[i])
    with open(path, encoding="utf-8") as f:
        print(f"{file_name_list[i]}")
        text = f.read().lower()
        words = text.split()
        words = [w.strip('.,"\'-?:!;<>_«»{}()[]°=*„“…—') for w in words]
        all_words_count += len(words)
        # посимвольная обработка (+ спец символы)
        for j in range(len(text)):
            if unic_symb.get(text[j]) is None:
                unic_symb[text[j]] = 0
            unic_symb[text[j]] += 1
        # обработка по словам
        for word in words:
            if word != ' ' and word != '–' and word != '':
                if word in unic_words:
                    unic_words[word] += 1
                else:
                    unic_words[word] = 1

result_symb_dict = sorted(calculate_freq(unic_symb).items(), key = lambda x : x[1], reverse=True)

# Вывод информации о символах
print("\nСимволы и их частота встречаемости:\n", result_symb_dict)
print("\nКол-во различных символов, встречающихся в текстах: ", len(result_symb_dict))
text_symb = []
# чаще всего встречающиеся буквенные символы
for i in range(1, 5):
    text_symb.append(result_symb_dict[i][0])
print("Буквы, которые чаще всего встречаются в словах: ", text_symb)
print("Небуквенные символы: ")
for key, value in dict(result_symb_dict).items():
    if not str(key).isalpha():
        symbol_list.append(key)
print(symbol_list)

# Вывод информации о словах
print("Слова и их частота встречаемости:")
result_words_dict = sorted(calculate_freq(unic_words).items(), key = lambda x : x[1], reverse=True)
for i in range(100):
    print(result_words_dict[i])
print("...")
print("Слова записаны в файл dictionary.txt\n")
print("Общее кол-во слов в текстах: ", all_words_count)
print("Кол-во уникальных слов в текстах: ", len(unic_words))
print("Слова, которые чаще всего встречаются в текстах: ")
top_words = []
# чаще всего встречающиеся слова
for i in range(6):
    top_words.append(result_words_dict[i][0])
print(top_words)

# записываем слова в файл
file = open('dictionary.txt', "w+", encoding='utf-8')
for i in range(len(result_words_dict)):
    file.write(f"{result_words_dict[i][0]}\n")
file.close()
