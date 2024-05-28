from pathlib import Path
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from pymystem3 import Mystem
import re


def preprocess(text):
    cleaned_text = re.findall('[а-яё]+', text.lower())
    cleaned_text = ' '.join(word for word in cleaned_text if word not in stop_words)
    lemm_text = ''.join(m.lemmatize(cleaned_text))
    return lemm_text


m = Mystem()
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('russian'))
path = Path(__file__).parent / 'all_advertisements'
adv_index = 0

for file in path.glob('*.txt'):
    with open(file, 'r', encoding="utf-8") as f:
        text = f.read()
        print(text)
        preprocessed_text = preprocess(text)
        print(preprocessed_text)
        with open(f"all_advertisements/cleaned_{file.name}", "w", encoding="utf-8") as g:
            g.write(preprocessed_text)
            adv_index += 1
