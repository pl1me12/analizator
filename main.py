# загрузка и отображение данных

f = open('пушкин.txt', "r", encoding="utf-8")
text = f.read()
type(text)
len(text)
text[:300]

# предворительная обработка текста
# перевод в единый регистр(нижний)
text = text.lower()
import string
string.punctuation
type(string.punctuation)
spec_chars = string.punctuation + '\n\xa0«»\t—…'
text = "".join([ch for ch in text if ch not in spec_chars])
import re
text = re.sub('\n', '', text)
def remove_chars_from_text(text, chars):
    return "".join([ch for ch in text if ch not in chars])
text = remove_chars_from_text(text, spec_chars)
text = remove_chars_from_text(text, string.digits)
