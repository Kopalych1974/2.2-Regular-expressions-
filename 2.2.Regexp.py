'''
Домашнее задание к лекции 2.2 «Regular expressions»
Иногда при знакомстве мы записываем контакты в адресную книгу кое-как с мыслью, что "когда-нибудь потом все обязательно поправим". Копируем данные из интернета или из смски. Добавляем людей в разных мессенджерах. В результате получается адресная книга, в которой совершенно невозможно кого-то нормально найти: мешает множество дублей и разная запись одних и тех же имен.

Кейс основан на реальных данных из https://www.nalog.ru/opendata/, https://www.minfin.ru/ru/opendata/

Ваша задача: починить адресную книгу, используя регулярные выражения.
Структура данных будет всегда:
lastname,firstname,surname,organization,position,phone,email
Предполагается, что телефон и e-mail у человека может быть только один.
Необходимо:

поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно. В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О;
привести все телефоны в формат +7(999)999-99-99. Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999;
объединить все дублирующиеся записи о человеке в одну.
from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
# ваш код

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(contacts_list)

'''

from pprint import pprint
import csv
import re

with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Задание 1: распределяем фамилию, имя и отчество по отдельным полям
header = contacts_list[0]
contacts_list_clean = [header]

for item in contacts_list[1:]:
    if item[0] != '' and item[1] != '' and item[2] != '':
        contacts_list_clean.append(item)
    else:
        full_name = ' '.join(item[0:3]).strip()
        rest_of_item = item[3:]

        full_name_divided = re.split('\s+', full_name)

        # добавляем пустую строку в поле surname, если отчества нет
        if len(full_name_divided) == 3:
            pass
        else:
            full_name_divided.append('')

        full_raw = full_name_divided + rest_of_item

        contacts_list_clean.append(full_raw)

# Задание 2: приводим все телефоны к формату +7(999)999-99-99 или +7(999)999-99-99 доб.9999
for item in contacts_list_clean:
    phone_pattern = '(\+7|8)(\s*)(\(?)(\d{3})(\)?)(\s*)(\-*)(\d{3})(-*)(\d{2})(-*)(\d{2})(\s*)(\(?)(\s?(доб)?)(\.?)(\s*)(\d*)(\)?)'
    find_phone = re.findall(phone_pattern, item[5])
    clean_phone = re.sub(phone_pattern, r'+7(\4)\8-\10-\12\13\15\17\19', item[5])

    item[5] = clean_phone

# Задание 3: объединяем все дублирующиеся записи о человеке в одну
contacts_list_clean_search = contacts_list_clean.copy()

# добавляем новое поле для полного ФИО — по нему будем ускать дублирующие записи
contacts_list_clean_search[0].append('search_name_field')

i = 1
for item in contacts_list_clean_search[i:]:
    search_name = ' '.join(item[0:3]).strip()
    contacts_list_clean_search[i].append(search_name)
    i += 1

contacts_list_clean_no_dub = [header]

j = 0
for item in contacts_list_clean_search[1:]:
    j += 1
    k = 0
    for another_item in contacts_list_clean_no_dub:

        # добавляем в новый список уникальные записи
        if contacts_list_clean_search[j][-1] not in contacts_list_clean_no_dub[k][-1]:
            k += 1
            if k == len(contacts_list_clean_no_dub):
                contacts_list_clean_no_dub.append(item)
                break

        # объединяем неуникальные записи
        else:
            for index, yet_another_item in enumerate(another_item[0:7]):
                if yet_another_item == '' and contacts_list_clean_search[j][index] != '':
                    another_item[index] = contacts_list_clean_search[j][index]
            break

# удаляем уже ненужное поле search_name_field
for item in contacts_list_clean_no_dub:
    del item[7]

pprint(contacts_list_clean_no_dub)

with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list_clean_no_dub)
