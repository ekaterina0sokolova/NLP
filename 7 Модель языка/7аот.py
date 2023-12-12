import spacy
import requests
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt
import json
import os
import wget

nlp = spacy.load("ru_core_news_sm")

# получаем список частей речи
def get_pos_tags(text):
    # разбиваем текст на части по 100 000 символов
    chunk = text[:1000]
    pos_tags = []
    doc = nlp(chunk)
    # исключаем знаки препинания и пробелы
    chunk_pos_tags = [token.pos_ for token in doc if not token.is_punct and token.pos_ != 'SPACE']
    pos_tags.extend(chunk_pos_tags)
    return pos_tags


# отрисовка графа
def build_graph(pos_tags):
    graph = nx.DiGraph()
    prev_tag = None
    for tag in pos_tags:
        if prev_tag is not None:
            if not graph.has_edge(prev_tag, tag):
                graph.add_edge(prev_tag, tag, weight=1)
            else:
                graph[prev_tag][tag]['weight'] += 1
        prev_tag = tag
        if tag not in graph.nodes:
            graph.add_node(tag)

    return graph

def pairs(graph):
    top_pairs = Counter()
    for edge in graph.edges(data=True):
        source, target, data = edge
        weight = data['weight']
        pos_pair = (source, target, weight)
        top_pairs[pos_pair] += weight
    return top_pairs.most_common(5)

def translate_pos_tag(pos_tag):
    translation_dict = {
        "ADJ": "прил",
        "ADP": "пред.",
        "ADV": "нар.",
        "AUX": "гл.",
        "CONJ": "союз",
        "CCONJ": "союз",
        "DET": "опр.",
        "INTJ": "межд.",
        "NOUN": "сущ.",
        "NUM": "числ.",
        "PART": "частица",
        "PRON": "местоим.",
        "PROPN": "имя собств.",
        "PUNCT": "пункт.",
        "SCONJ": "союз",
        "SYM": "симв.",
        "VERB": "гл.",
        "X": "др.",
        "SPACE": "пробел"
    }

    return translation_dict.get(pos_tag, pos_tag)

# построение графа
def visualize_graph(file_name, graph, ignore_nodes=None):
    if ignore_nodes is None:
        ignore_nodes = ["X", "INTJ", "PUNCT", "SPACE"]

    # создаем подграф, исключая узлы, которые мы хотим игнорировать
    subgraph_nodes = [node for node in graph.nodes if node not in ignore_nodes]
    subgraph = graph.subgraph(subgraph_nodes)

    pos = nx.spring_layout(subgraph, k=0.5)
    labels = nx.get_edge_attributes(subgraph, 'weight')
    plt.figure(figsize=(20, 20))
    nx.draw(subgraph, pos, with_labels=True, font_weight='bold', node_size=3000)
    nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=labels)
    plt.savefig(f'{file_name[:-4]}.png')
    plt.show()

def process_text(path):
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()

    file_name = os.path.basename(path)

    pos_tags = get_pos_tags(text)
    pos_tags_ru = []
    for tag in pos_tags:
        pos_tags_ru.append(translate_pos_tag(tag))
    # print(pos_tags_ru)
    graph = build_graph(pos_tags_ru)

    # выводим топ-5 пар частей речи
    print(f"Топ-5 пар частей речи {file_name}:")
    for i, (pair, count) in enumerate(pairs(graph), 1):
        translated_pair = tuple(translate_pos_tag(tag) for tag in pair)
        print(f"{i}. {translated_pair[0]} - {translated_pair[1]}: {count}")
    visualize_graph(file_name, graph)

# загрузка текстов с репозитория
json_text = requests.get("https://github.com/nevmenandr/word2vec-russian-novels/tree/master/books_before").text
json_dict = json.loads(json_text)

item_list_len = len(json_dict["payload"]["tree"]["items"])

path_books = "C:/Users/Admin/Desktop/5_semestr/Автоматическая обработка текста/books_before"

# добавление названий в список
file_name_list = []
for i in range(item_list_len):
    file_name_list.append(json_dict["payload"]["tree"]["items"][i]['name'])

# загрузка текстов
if len(file_name_list) != len(os.listdir(path_books))-1:
    # загружаем недостающие файлы
    print("Не все файлы загружены...")
    for i in range(len(file_name_list)):
        if os.path.isfile(os.path.join(path_books)) == file_name_list[i]:
            continue
        else:
            print(f"Загружаем: {file_name_list[i]}")
            link = "https://raw.githubusercontent.com/nevmenandr/word2vec-russian-novels/master/books_before/" + str(
                file_name_list[i])
            wget.download(link)

print("Все файлы загружены!\n")

print("Файлы обрабатываются...")
for file_name in file_name_list:
    path = f"C:/Users/Admin/Desktop/5_semestr/Автоматическая обработка текста/books_before/{file_name}"
    print(f"{file_name}...")
    process_text(path)

