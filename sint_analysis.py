import re
from pathlib import Path

path = Path(__file__).parent / 'all_advertisements'

questions = 0
exclamations = 0
sentences = []

reason = ['так как', 'потому что', 'поскольку', 'ибо', 'благодаря тому что', 'благодаря тому, что',
          'оттого что', 'из-за того что', 'из-за того, что', 'потому, что']
reason_count = 0


def preprocess(text):
    cleaned_text = re.findall('[а-яё]+', text.lower())
    cleaned_text = ' '.join(cleaned_text)
    return cleaned_text


for file in path.glob('text_*.txt'):
    with open(file, 'r', encoding="utf-8") as f:
        text = f.read()
        if '?' in text:
            questions += 1
        if '!' in text:
            exclamations += 1
        for conj in reason:
            if conj in text.lower():
                reason_count += 1
        text = text.replace('\n', ' ')
        sentences.extend(re.split(r'(?<=\w[.!?])', text))

print(questions)
print(exclamations)
print(reason_count)
