print("Для завершения программы введите 'exit'")
while True:
    word = input("Введите слово: \n")
    if word == 'exit':
        exit(0)

    dictionary = []
    f = open("dictionary.txt", encoding='utf-8')
    for line in f:
        dictionary.append(line[:len(line)-1])
    f.close()
    if dictionary.count(word) > 0:
        print("Слово написано правильно!")
    else:
        # поочередно применяем оперции для исправления слова
        corrections = []
        word_len = len(word)
        alphabet = 'абвгдеёжзийклмнопрстуфхцчшщыъьэюя'
        def is_word_in_dictionary(word):
            if word in dictionary:
                return True
            else:
                return False

        # вставить букву
        for i in range(word_len+1):
            for letter in alphabet:
                new_word = word[:i] + letter + word[i:]
                if is_word_in_dictionary(new_word):
                    corrections.append(new_word)
       # удалить букву
        for i in range(word_len):
            new_word = word[:i] + word[i+1:]
            if is_word_in_dictionary(new_word) and new_word not in corrections:
                corrections.append(new_word)
            # заменить букву на другую
            for letter in alphabet:
                new_word = word[:i] + letter + word[i+1:]
                if is_word_in_dictionary(new_word) and new_word not in corrections:
                    corrections.append(new_word)
            # поменять местами две соседние буквы
            for i in range(len(word) - 1):
                new_word = word[:i] + word[i + 1] + word[i] + word[i + 2:]
                if is_word_in_dictionary(new_word) and new_word not in corrections:
                    corrections.append(new_word)
        if len(corrections) == 0:
            print("Исправления не найдены!")
        else:
            print(corrections)