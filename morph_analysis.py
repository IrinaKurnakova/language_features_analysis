import pymorphy2
import re
from pathlib import Path


def preprocess(text):
    cleaned_text = re.findall('[а-яё]+', text.lower())
    cleaned_text = ' '.join(cleaned_text)
    return cleaned_text


def count_numerals(text):
    text = re.sub('[Рр]еклама[\s\S]+', '', text)
    text = re.sub('ИНН[\s\S]*', '', text)
    numerals = re.findall('\d+[ ]*\d*', text)
    return numerals


morph = pymorphy2.MorphAnalyzer()

per_pronouns_total = {'1per sing': 0, '1per plur': 0, '2per sing': 0, '2per plur': 0}
poss_pronouns_total = {'мой': 0, 'твой': 0, 'наш': 0, 'ваш': 0}
per_pronouns_current = {'1per sing': 0, '1per plur': 0, '2per sing': 0, '2per plur': 0}
poss_pronouns_current = {'мой': 0, 'твой': 0, 'наш': 0, 'ваш': 0}

imperatives_current = {'impr sing': 0, 'impr plur': 0}
imperatives_total = {'impr sing': 0, 'impr plur': 0}

verbs_current = {'pres 1per': 0, 'pres 2per': 0, 'pres 3per': 0, 'past': 0, 'futr': 0}
verbs_total = {'pres 1per': 0, 'pres 2per': 0, 'pres 3per': 0, 'past': 0, 'futr': 0}

adj_current = {'ADJF': 0, 'Qual': 0, 'Supr': 0, 'COMP': 0}
adj_total = {'ADJF': 0, 'Qual': 0, 'Supr': 0, 'COMP': 0}

adverbs = {'выгодный': 0, 'удобный': 0, 'доступный': 0, 'комфортный': 0, 'бесплатный': 0}
total_adverbs = 0
total_intensifiers = 0

numerals_total = []
numerals_context = 0
numerals_all_context = 0
numerals_words_total = []
numerals_words_current = []

path = Path(__file__).parent / 'all_advertisements'
total_imperatives = 0
total_impr_sing = 0
total_impr_plur = 0

total_verbs_pres = 0
total_verbs_pres1 = 0
total_verbs_pres2 = 0
total_verbs_pres3 = 0
total_verbs_past = 0
total_verbs_futr = 0

adjectives = 0
adjectives_qual = 0
comparatives = 0

total_pronouns = 0
total_1per = 0
total_2per = 0
total_3per = 0
total_3per_amount = 0
current_3per = 0
total_1per_sing = 0
total_1per_plur = 0
total_2per_sing = 0
total_2per_plur = 0
slang = 0
slang_text = 0
flag = 0

for file in path.glob('text_*.txt'):
    with open(file, 'r', encoding="utf-8") as f:
        text = f.read()
        numerals = count_numerals(text)
        if numerals:
            numerals_total.extend(numerals)
            numerals_context += 1

        if 'её' in text:
            current_3per += text.count('её')

        text = preprocess(text)
        if 'выгод' in text:
            adverbs['выгодный'] += 1
            flag = 1
        if 'удоб' in text:
            adverbs['удобный'] += 1
            flag = 1
        if 'доступн' in text:
            adverbs['доступный'] += 1
            flag = 1
        if 'комфорт' in text:
            adverbs['комфортный'] += 1
            flag = 1
        if 'бесплатн' in text:
            adverbs['бесплатный'] += 1
            flag = 1
        if re.findall('любим[ыаоу]', text):
            flag = 1
        if flag == 1:
            total_adverbs += 1
            flag = 0

        for word in ['очень', 'абсолютно', 'всегда', 'именно']:
            if word in text:
                total_intensifiers += 1
                break

        for word in ['классн', 'крут', 'кайф', 'обалд', 'чилл', 'тус', 'балд', 'офиг', 'залетай']:
            if word in text:
                slang += 1
                flag = 1
        if flag == 1:
            slang_text += 1
            flag = 0

        for word in text.split():
            parsed = morph.parse(word)[0].tag

            if 'NUMR' in parsed:
                numerals_words_current.append(word)

            if {'impr', 'sing'} in parsed:
                imperatives_current['impr sing'] += 1
            if {'impr', 'plur'} in parsed:
                imperatives_current['impr plur'] += 1

            if {'VERB', 'pres', '1per'} in parsed:
                verbs_current['pres 1per'] += 1
            if {'VERB', 'pres', '2per'} in parsed:
                verbs_current['pres 2per'] += 1
            if {'VERB', 'pres', '3per'} in parsed:
                verbs_current['pres 3per'] += 1
            if {'VERB', 'past'} in parsed:
                verbs_current['past'] += 1
            if {'VERB', 'futr'} in parsed:
                verbs_current['futr'] += 1

            if 'ADJF' in parsed:
                for key in adj_current.keys():
                    if key in parsed:
                        adj_current[key] += 1
            if 'COMP' in parsed:
                adj_current['COMP'] += 1

            if 'NPRO' in parsed:
                for key in per_pronouns_current.keys():
                    if {key.split()[0], key.split()[1]} in parsed:
                        per_pronouns_current[key] += 1
                if '3per' in parsed:
                    current_3per += 1

            if {'ADJF', 'Apro'} in parsed:
                if word[:2] == 'мо':
                    poss_pronouns_current['мой'] += 1
                elif word[:2] == 'тв':
                    poss_pronouns_current['твой'] += 1
                elif word[:3] == 'ваш':
                    poss_pronouns_current['ваш'] += 1
                elif word[:3] == 'наш':
                    poss_pronouns_current['наш'] += 1

    if numerals_words_current or numerals:
        numerals_all_context += 1
        numerals_words_total.extend(numerals_words_current)
        numerals_words_current = []

    for key, value in verbs_current.items():
        verbs_total[key] += value
    if verbs_current['pres 1per'] > 0 or verbs_current['pres 2per'] > 0 \
            or verbs_current['pres 3per'] > 0:
        total_verbs_pres += 1
    if verbs_current['pres 1per'] > 0:
        total_verbs_pres1 += 1
    if verbs_current['pres 2per'] > 0:
        total_verbs_pres2 += 1
    if verbs_current['pres 3per'] > 0:
        total_verbs_pres3 += 1
    if verbs_current['past'] > 0:
        total_verbs_past += 1
    if verbs_current['futr'] > 0:
        total_verbs_futr += 1

    verbs_current = {'pres 1per': 0, 'pres 2per': 0, 'pres 3per': 0, 'past': 0, 'futr': 0}

    for key, value in imperatives_current.items():
        imperatives_total[key] += value
        if value > 0:
            flag = 1
    if flag == 1:
        total_imperatives += 1
        flag = 0
    if imperatives_current['impr sing'] > 0:
        total_impr_sing += 1
    if imperatives_current['impr plur'] > 0:
        total_impr_plur += 1
    imperatives_current = {'impr sing': 0, 'impr plur': 0}

    for key, value in adj_current.items():
        adj_total[key] += value
        if value > 0:
            flag = 1
    if flag == 1:
        adjectives += 1
        flag = 0
    if adj_current['Qual'] > 0:
        adjectives_qual += 1
    if adj_current['COMP'] > 0:
        comparatives += 1
    adj_current = {'ADJF': 0, 'Qual': 0, 'Supr': 0, 'COMP': 0}

    for key, value in per_pronouns_current.items():
        per_pronouns_total[key] += value
        if value > 0:
            flag = 1
    for key, value in poss_pronouns_current.items():
        poss_pronouns_total[key] += value
        if value > 0:
            flag = 1
    if flag == 1:
        total_pronouns += 1
        flag = 0

    if current_3per > 0:
        total_3per += 1
        total_3per_amount += current_3per
        current_3per = 0
    if (per_pronouns_current['1per sing'] > 0 or per_pronouns_current['1per plur'] > 0 or
            poss_pronouns_current['мой'] > 0 or poss_pronouns_current['наш'] > 0):
        total_1per += 1
        if per_pronouns_current['1per sing'] > 0 or poss_pronouns_current['мой'] > 0:
            total_1per_sing += 1
        if per_pronouns_current['1per plur'] > 0 or poss_pronouns_current['наш'] > 0:
            total_1per_plur += 1
    if (per_pronouns_current['2per sing'] > 0 or per_pronouns_current['2per plur'] > 0 or
            poss_pronouns_current['твой'] > 0 or poss_pronouns_current['ваш'] > 0):
        total_2per += 1
        if per_pronouns_current['2per sing'] > 0 or poss_pronouns_current['твой'] > 0:
            total_2per_sing += 1
        if per_pronouns_current['2per plur'] > 0 or poss_pronouns_current['ваш'] > 0:
            total_2per_plur += 1
    per_pronouns_current = {'1per sing': 0, '1per plur': 0, '2per sing': 0, '2per plur': 0}
    poss_pronouns_current = {'мой': 0, 'твой': 0, 'наш': 0, 'ваш': 0}

print('Всего контекстов, содержащих императивы:', total_imperatives)
print('Императивы ед:', total_impr_sing)
print('Императивы мн:', total_impr_plur)
print(imperatives_total)

print('Всего контекстов, содержащих прилагательные:', adjectives)
print('Качественные прилагательные', adjectives_qual)
print('Компаративы:', comparatives)
print(adj_total)

print('Всего контекстов, содержащих местоимения:', total_pronouns)
print('1 лицо:', total_1per)
print('2 лицо:', total_2per)
print('3 лицо:', total_3per, total_3per_amount)
print('1 лицо ед:', total_1per_sing)
print('1 лицо мн:', total_1per_plur)
print('2 лицо ед:', total_2per_sing)
print('2 лицо мн:', total_2per_plur)
print(per_pronouns_total)
print(poss_pronouns_total)

print('Всего контекстов, содержащих наречия:', total_adverbs)
print('Интенсификаторы:', total_intensifiers)
print(adverbs)

print('Всего словоупотреблений числительных (цифрами):', len(numerals_total))
print('Всего числительных в контексте (цифрами):', numerals_context)
print('Всего словоупотреблений числительных (буквами):', len(numerals_words_total))
print('Всего числительных в контексте (все):', numerals_all_context)

print('Всего контекстов, содержащих глаголы в настоящем времени:', total_verbs_pres)
print('Наст.вр. 1 лицо:', total_verbs_pres1)
print('Наст.вр. 2 лицо:', total_verbs_pres2)
print('Наст.вр. 3 лицо:', total_verbs_pres3)
print('Прош.вр.:', total_verbs_past)
print('Буд.вр.:', total_verbs_futr)
print(verbs_total)

print('Всего словоупотреблений разговорной и сленговой лексики:', slang)
print('Контекстов, содержащих разговорную и сленговую лексику:', slang_text)

