import spacy
import pymorphy3
import matplotlib.pyplot as plt
import networkx as nx

# Загружаем модель
nlp = spacy.load("ru_core_news_sm")
morph = pymorphy3.MorphAnalyzer(lang='ru')


# получаем грамматические основы из файлика для сравнения
def get_correct_osn():
    correct_osn = []
    with open('gramm_osnov.txt', 'r+', encoding="utf-8") as f:
        for line in f:
            osnvs = line.rstrip().split(",")
            podlej_list = []
            skaz_list = []
            for o in osnvs:
                podlej = o.split(":")[0].split()
                skaz = o.split(":")[1].split()
                for p in podlej:
                    podlej_list.append(p)
                for s in skaz:
                    skaz_list.append(s)
            podl_sort = sorted(podlej_list)
            skaz_sort = sorted(skaz_list)
            correct_osn.append([podl_sort, skaz_sort])
    return correct_osn


# выводит в консоль точность работы алгоритма
def get_alg_accuracy(correct_gr_os, lib_gr_os):
    # счетчик совпадений
    count = 0
    for i in range(len(lib_gr_os)):
        if lib_gr_os[i] == correct_gr_os[i]:
            print(f"+ {lib_gr_os[i]} : {correct_gr_os[i]}")
            count += 1
        else:
            print(f"- {lib_gr_os[i]} : {correct_gr_os[i]}")
    acc = round(count / 58, 2)
    print(f"Результат: {count}/58 \nТочность: {acc}")


def draw_graphs():
    i = 0
    for sentence in sentences[:4]:
        sent = nlp(sentence)
        tok = []
        deps = []
        for token in sent:
            tok.append([token.text, token.head.text])
            deps.append(token.dep_)

        G = nx.Graph()
        G.add_edges_from(tok)
        pos = nx.spring_layout(G)
        plt.figure(figsize=(20, 6))
        nx.draw(G, pos, edge_color='black',
                width=1,
                linewidths=1,
                node_size=800,
                node_color='#b4a7d6',
                # прозрачность вершин
                alpha=1,
                labels={node: node for node in G.nodes()})
        k = 0
        for d in deps:
            nx.draw_networkx_edge_labels(G, pos, edge_labels={tuple(tok[k]): d}, font_color='#14145b')
            k += 1
        plt.axis('off')
        plt.savefig('{}_sentence.png'.format(i + 1))
        plt.show()
        i += 1


if __name__ == '__main__':
    f = open("Дачница.txt", "r", encoding="utf-8")
    text = f.read()

    # Обработка текста с помощью модели
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]

    # Поиск подлежащего и сказуемого в предложении
    lib_gr_os = []
    wrong_padezh = ['datv', 'ablt', 'gent', 'loct']  # дат., твор., род., предлож.

    for sentence in doc.sents:
        # подлежащее
        subject = []
        # сказуемое
        predicate = []

        for token in sentence:
            # падеж
            case = morph.parse(token.text)[0].tag.case
            # nsubj - подлежащее, ROOT - корень
            if (token.dep_ == "nsubj" or token.dep_ == "nsubj:pass") and (
                    case not in wrong_padezh or case == 'loct') and case != None:
                subject.append(token.text)
            if token.dep_ == "obj" and case not in wrong_padezh and token.pos_ == "PROPN":
                subject.append(token.text)
            if token.dep_ == "ROOT" and case not in wrong_padezh and token.pos_ != "NOUN" and token.text[-2:] != "сь":
                predicate.append(token.text)
            if token.dep_ == "conj" and token.pos_ in ["VERB", "ADJ"] and case not in wrong_padezh and token.text[
                                                                                                       -2:] != "сь" \
                    and token.text[-2:] not in ["ый", "ий", "ая", "яя", "ое", "ее"]:
                predicate.append(token.text)
            if token.dep_ == "cop" and token.pos_ == "AUX" and case not in wrong_padezh and token.text[-2:] != "сь":
                predicate.append(token.text)
            if token.dep_ == "ccomp" and token.pos_ == "VERB" and case not in wrong_padezh and token.text[-2:] != "сь":
                predicate.append(token.text)
            if token.dep_ == "parataxis" and token.pos_ == "VERB" and case not in wrong_padezh and token.text[
                                                                                                   -2:] != "сь":
                predicate.append(token.text)
            if token.dep_ == "xcomp" and case not in wrong_padezh:
                predicate.append(token.text)
        subj_sort = sorted(subject)
        pred_sort = sorted(predicate)
        lib_gr_os.append([subj_sort, pred_sort])

    # print("lib_gr_os"+str(lib_gr_os))

    # получаем правильные грамматические основы
    correct_gr_os = get_correct_osn()
    # точность работы алгоритма
    get_alg_accuracy(correct_gr_os, lib_gr_os)
    # строим графы
    draw_graphs()