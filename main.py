import nltk
nltk.download('punkt') # загрузка необходимых данных для NLTK

filename = input("Введите имя файла: ")
word = input("Введите слово: ")

with open(filename, "r") as file:
    text = file.read()

sentences = nltk.sent_tokenize(text)

for sentence in sentences:
    words = nltk.word_tokenize(sentence)
    if word in words:
        tags = nltk.pos_tag(words)
        for i, (w, tag) in enumerate(tags):
            if w == word:
                print("Слово:", w)
                print("Предложение:", sentence)
                print("Часть речи:", tag)
                if tag in ['NN', 'NNS', 'NNP', 'NNPS']: # определение рода для существительных
                    word_lemmatizer = nltk.WordNetLemmatizer()
                    lemma = word_lemmatizer.lemmatize(w) # лемматизация слова
                    noun_synset = nltk.corpus.wordnet.synsets(lemma, pos='n') # поиск синсетов существительных в WordNet
                    if noun_synset: # если синсет найден, печатаем его информацию
                        noun = noun_synset[0]
                        print("Род:", noun.lexname().split('.')[0])
                tree = nltk.parse.parse_one(sentence) # получение синтаксического дерева
                print("Синтаксический разбор:")
                tree.pretty_print() # вывод синтаксического дерева
                print("="*80) # разделитель между результатами