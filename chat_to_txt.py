#!/usr/bin/python3

import json
import os
import shutil

adv_index = 0
total_posts = 0
total_words = 0
total_symbols = 0
images = 0
patterns = ["Реклама.", "Реклама ООО", "Реклама ОАО", "Реклама, ООО", "Реклама, ОАО",
            "реклама ООО", "реклама ОАО", "реклама, ООО", "реклама, ОАО"]
for i in range(27):
    posts = 0
    with open(f"Chat_{i+1}/result.json", encoding="utf-8") as f:
        data = json.load(f)
    messages = data["messages"]
    name = data["name"]
    adv_posts = []
    for message in messages:
        if "media_type" in message:
            continue
        if "text" not in message:
            continue
        full_text = ''
        for element in message["text"]:
            if isinstance(element, str):
                full_text += element
            elif isinstance(element, dict):
                full_text += element['text']
        for pattern in patterns:
            if pattern in full_text:
                if "photo" in message:
                    adv_posts.append([full_text, message['photo'][7:]])
                else:
                    adv_posts.append([full_text])
                total_symbols += len(full_text)
                total_words += len(full_text.split())
                break

    for adv_post in adv_posts:
        with open(f"all_advertisements/text_{adv_index}.txt", "w", encoding="utf-8") as f:
            f.write(adv_post[0])
        if len(adv_post) == 2:
            shutil.copy(f"Chat_{i+1}/photos/{adv_post[1]}", "all_advertisements")
            os.rename(f"all_advertisements/{adv_post[1]}", f"all_advertisements/photo_{adv_index}.jpg")
            images += 1
        adv_index += 1
        posts += 1
        total_posts += 1
    print(f"Собрано постов с канала {name}:", posts)

print('Всего собрано постов:', total_posts)
print('Всего постов, содержащих изображение:', images)
print('Общее количество слов:', total_words)
print('Общее количество символов:', total_symbols)
