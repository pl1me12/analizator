import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag, ne_chunk
nltk.download('punkt')

filename = input("Введите имя файла: ")
word = input("Введите слово: ")
sentences = []  # список для хранения предложений с искомым словом

# открываем файл и считываем все содержимое
with open(filename, "r", encoding='utf-8') as f:
    text = f.read()

# токенизируем текст на предложения и слова
tokenized_text = sent_tokenize(text)
words = word_tokenize(text)

# определяем стоп-слова
stop_words = set(stopwords.words("english"))

# проходимся по каждому предложению
for sentence in tokenized_text:
    # токенизируем предложение на слова
    sentence_words = word_tokenize(sentence)
    # проверяем, есть ли искомое слово в предложении
    if word in sentence_words:
        # убираем стоп-слова из предложения
        filtered_words = [word for word in sentence_words if word.casefold() not in stop_words]
        # определяем части речи слов в предложении
        tagged_words = pos_tag(filtered_words)
        # определяем синтаксический разбор предложения
        parsed_sentence = ne_chunk(tagged_words)
        # добавляем предложение в список, если оно содержит искомое слово
        sentences.append((sentence, parsed_sentence))

# выводим результаты
if len(sentences) > 0:
    for sentence, parsed_sentence in sentences:
        print("Найдено в предложении: ", sentence)
        print("Части речи слов: ", parsed_sentence)
else:
    print("Искомое слово не найдено в тексте.")