from razdel import tokenize
import spacy
import pymorphy3
from summa import summarizer

def get_normal_forms(token_list):
    lemm_tokens = []
    for t in token_list:
        if t.text.isalpha() \
                and morph.parse(t.text.lower())[0].tag.POS not in ["PREP", "CONJ", "PRCL", "INTJ"] \
                and t.text not in ".,-?!()\"\'„“«»–<>—…=°:;_{}[]*":
            lemm_tokens.append(morph.parse(t.text.lower())[0].normal_form)
    return lemm_tokens

def count_ROUGE1(filename):
    result_file = open(filename, "r", encoding="utf-8")
    obr_file = open("obr.txt", "r", encoding="utf-8")

    # лемматизация токенов полученного реферата
    tokens_ref = list(tokenize(result_file.read()))
    lemm_tokens_ref = get_normal_forms(tokens_ref)

    # лемматизация токенов образца
    tokens_obraz = list(tokenize(obr_file.read()))
    lemm_tokens_obraz = get_normal_forms(tokens_obraz)
    ROUGE1 = 0

    # считаем ROUGE-1
    for tok in lemm_tokens_obraz:
        if tok.isalpha() \
                and morph.parse(tok.lower())[0].tag.POS not in ["PREP", "CONJ", "PRCL", "INTJ"] \
                and tok not in ".,-?!()\"\'„“«»–<>—…=°:;_{}[]*":
            if tok in lemm_tokens_ref:
                ROUGE1 += 1
    ROUGE1 = ROUGE1 / len(lemm_tokens_obraz)
    return(ROUGE1)


def count_ROUGE2(filename):
    result_file = open(filename, "r", encoding="utf-8")
    obr_file = open("obr.txt", "r", encoding="utf-8")
    tokens_ref = list(tokenize(result_file.read()))
    lemm_tokens_ref = get_normal_forms(tokens_ref)

    tokens_obraz = list(tokenize(obr_file.read()))
    lemm_tokens_obraz = get_normal_forms(tokens_obraz)

    lemm_tokens_obraz_bigrams = []
    lemm_tokens_ref_bigrams = []

    for o in range(len(lemm_tokens_obraz) - 1):
        lemm_tokens_obraz_bigrams.append([lemm_tokens_obraz[o], lemm_tokens_obraz[o + 1]])

    for o in range(len(lemm_tokens_ref) - 1):
        lemm_tokens_ref_bigrams.append([lemm_tokens_ref[o], lemm_tokens_ref[o + 1]])

    ROUGE2 = 0
    for tok in lemm_tokens_obraz_bigrams:
        if tok in lemm_tokens_ref_bigrams:
            # print(tok)
            ROUGE2 += 1
    ROUGE2 = ROUGE2 / len(lemm_tokens_obraz_bigrams)
    return(ROUGE2)


def count_ROUGE3(filename):
    result_file = open(filename, "r", encoding="utf-8")
    obr_file = open("obr.txt", "r", encoding="utf-8")
    tokens_ref = list(tokenize(result_file.read()))
    lemm_tokens_ref = get_normal_forms(tokens_ref)

    tokens_obraz = list(tokenize(obr_file.read()))
    lemm_tokens_obraz = get_normal_forms(tokens_obraz)

    lemm_tokens_obraz_trigrams = []
    lemm_tokens_ref_trigrams = []
    for o in range(len(lemm_tokens_obraz) - 2):
        lemm_tokens_obraz_trigrams.append([lemm_tokens_obraz[o], lemm_tokens_obraz[o + 1], lemm_tokens_obraz[o + 2]])

    for o in range(len(lemm_tokens_ref) - 2):
        lemm_tokens_ref_trigrams.append([lemm_tokens_ref[o], lemm_tokens_ref[o + 1], lemm_tokens_ref[o + 2]])

    ROUGE3 = 0
    for tok in lemm_tokens_obraz_trigrams:
        if tok in lemm_tokens_ref_trigrams:
            ROUGE3 += 1
    ROUGE3 = ROUGE3 / len(lemm_tokens_obraz_trigrams)
    return(ROUGE3)


nlp = spacy.load("ru_core_news_sm")
morph = pymorphy3.MorphAnalyzer()

# формирование словарей
lemms_count = 0
unique_lemms = dict()

with open('input_text.txt', encoding="utf-8") as f:
    text = f.read()
    tokens = list(tokenize(text))
    # заполняем словарь лемм
    for i in tokens:
        if morph.parse(i.text.lower())[0].tag.POS not in ["PREP", "CONJ", "PRCL","INTJ"] and i.text not in ".,-?!()\"\'„“«»–<>—…=°:;_{}[]*":
            lemma = morph.parse(i.text.lower())[0].normal_form
            if unique_lemms.get(lemma) is None:
                unique_lemms[lemma] = 0
            unique_lemms[lemma] += 1
            lemms_count += 1

lemms_sort_dict = dict(sorted(unique_lemms.items(), key=lambda item: -item[1]))

# формируем веса слов
lemms_weights = dict()
for lemm in lemms_sort_dict:
    lemms_weights[lemm] = lemms_sort_dict[lemm] / lemms_count

doc = nlp(text)
sentences = text.split("\n")

sent_info = []
sent_lemms_weights = []
index = 0
for sent in sentences:
    for word in sent.split():
        if word.isalpha() \
                and morph.parse(word.lower())[0].tag.POS not in ["PREP", "CONJ", "PRCL", "INTJ"] \
                and word not in ".,-?!()\"\'„“«»–<>—…=°:;_{}[]*":
            lemma = morph.parse(word.lower())[0].normal_form
            sent_lemms_weights.append({lemma: lemms_weights[lemma]})
    weight = 0
    for lem in sent_lemms_weights:
        for w in lem:
            weight += lem[w]
    sent_info.append([index, sent_lemms_weights, weight])
    index += 1
    sent_lemms_weights = []

sent_info_sort = sorted(sent_info, key=lambda x: -x[2])

chosen_ind = []
for s in sent_info_sort[:20]:
    chosen_ind.append(s[0])

ref_sentenses = []
for c in sorted(chosen_ind):
    ref_sentenses.append(sentences[c])

result_file = open("referat.txt", "w", encoding="utf-8")
for i in ref_sentenses:
    result_file.write(i + "\n")
result_file.close()

sum_ref = open("summa.txt", "w", encoding="utf-8")
sum_ref.write(summarizer.summarize(text, ratio=0.1))
sum_ref.close()

round_num = 3
refs_list = ["referat.txt", "splitbrain.txt", "visual_word.txt", "summa.txt"]

max_length = max(len(string) for string in refs_list)
refs_list = [string.ljust(max_length) for string in refs_list]

print("               ROUGE1 "+"ROUGE2 "+"ROUGE3")
for ref in refs_list:
    cnt1 = round(count_ROUGE1(ref), 3)
    cnt2 = round(count_ROUGE2(ref), 3)
    cnt3 = round(count_ROUGE3(ref), 3)
    print(ref+" "+str(cnt1)+" "+str(cnt2)+" "+str(cnt3))
