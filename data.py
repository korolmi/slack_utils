# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# Здесь содержатся все данные
#
# * о студентах
# * о событиях
# * тексты и прочее
#
# т.е. то, что создается в процессе общения (не для процесса общения)

import datetime

# Дата, начиная с которой нужно анализировать диалоги
stDate = datetime.datetime(2019,10,3,0,0).timestamp()

groups = { # каналы групп
    "grp1": "GPC2KAYBZ",
    "grp5": "GP3QCUGN5"
}

# список сотрудников - им не рассылаем
sfList = [
    "UHAJXCWFL",  # Mikhail Dekterev
    "UNT1YLTLJ",  # Oksana Bykova
    "UL9FNBJCE",  # какой-то контроль
    "UHR4EE9B2",  # Анастасия Лобанова
    "UKQBB74TZ",  # Антон Шавинский
    "USLACKBOT",  # бот...
    "UPCCN4K9V"   # я
]
ME = "UPCCN4K9V"

# +
# Студенты с "раскраской"
# NOM0 - нет результатов по модулю 0
studData = [
    { "grp": "grp1", "id": "UHGDA720K", "tag": "NOM0", "name": "Gotovtsev Dmitry" },
    { "grp": "grp1", "id": "UHJTQKQ9F", "tag": "NOM0", "name": "Irina Alexeeva" },

    { "grp": "grp5", "id": "UMBGDPMQU", "tag": "NOM0", "name": "sunrise-new REAL: Viktoria" },
    { "grp": "grp5", "id": "UME53RCB1", "tag": "NOM0", "name": "pentilla REAL: Леонид Багмат" },
]
# -

# напоминалка про несделанные задания 08.11.2019 - разослано в 17:38
remText = """
Привет!
Дедлайн по вводному модулю сквозного курса "Реальный дата сайенс" уже совсем скоро, в нем есть задания, а результатов их выполнения Вами я не вижу...
Очень бы здорово выложить сделанное, чтобы я мог посмотреть и откомментировать.
Выполненные задания = переход на следующий модуль.
Если чем-то могу помочь - дайте знать :-)"""
