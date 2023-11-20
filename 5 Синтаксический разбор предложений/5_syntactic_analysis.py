import spacy_udpipe

spacy_udpipe.download("ru")
udpipe_model = spacy_udpipe.load("ru")

# with open("Дачница.txt", "r+", encoding="utf-8") as file:
#     text = file.read()
#
# docUP = udpipe_model(text)
# for sent in docUP:
#     for word in sent.words:
#         print(word.id, word.form, word.deprel)
