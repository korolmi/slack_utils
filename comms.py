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

import json, datetime

# %load_ext autoreload

# %autoreload
import data, slk_utils

# # Готовим списки
#
# Обновление или создание списков своих учеников
#
# * читаем список канала (группового)
# * для каждого участника читаем его параметры
#
# параметры - мои группы имеют ID каналов (узнать просто - клик по каналу в веб интерфейсе слэк)

gRes = slk_utils.getData('https://slack.com/api/groups.info?channel='+data.groups["grp5"])

# список ID участников группы
ids = gRes['group']['members']
students = {}
for im in ids:
    uRes = slk_utils.getData('https://slack.com/api/users.info?user=' + im)
    user = uRes["user"]["name"]
    real = uRes["user"]["real_name"]
    print("ID:", im, "USER:", user, "REAL:", real)
    students[im] = user+"/"+real

# ### Разошлем обратную связь
#
# Здесь файл содержит несложно оформленный текст обратной связи каждому и ту информацию о студенте, которая есть в журнале (какое-то его "имя).
#
# Часть строк файла - стандартные и одни для всех, но есть, естественно, и "конкретные" моменты (мы тут облегчаем себе жизнь, не читим...)
#
# Пример файла (резаный, конечно)
# `
#
# ***Дмитрий Воронцов
#
# Обратная связь (по заданиям вводного модуля сквозного курса)
#
# Хорошая работа, начало в этом курсе положено. Немного мыслей, которые у меня возникли, когда смотрел. Относитесь к ним как просто
#  к наблюдениям опытного человека: это Ваши взгляды и мысли, Ваше резюме, Ваша жизнь. Я - как зеркало - говорю, что я лично вижу.
#
# Вакансии, мысли...
#
# ...
#
# Впереди еще много работы, спасибо за первую!
#
# ***Victoria Yakimovich
#
# ....
# `

# Разберем сообщения из файла, найдем пользователей, сопоставим ID
with open("/home/mk/tmp/gr5.txt","r") as fp:
    buf = fp.read()
msgList = {}
for mTxt in buf.split("***")[1:]:
    rcpt = mTxt.split("\n")[0]
    txt = "\n".join(mTxt.split("\n")[1:]).strip()
    uid = [ ui for ui in students.keys() if students[ui].find(rcpt)>0 ]
    if len(uid)!=1:
        print("problem", rcpt, uid)
    else:
        print(rcpt,":",uid[0])
        msgList[uid[0]] = txt

# +
# рассылаем по директ месседжам

# получим историю директ мессаджей с пользователем
dmListRes = slk_utils.getData('https://slack.com/api/conversations.list?types=im')
dmList = dmListRes["channels"]

for stud,txt in msgList.items():

    dmChan = None
    # stud = data.ME # для отладки - себе
    for chan in dmList:
        if chan["user"]==stud:
            dmChan = chan["id"]
            break
    if dmChan is None:
        print("No channel for ID={}".format(stud))
        continue
    msg = {
        "channel": dmChan,
        "text": txt, 
        "as_user": "true"
    }
    print(slk_utils.postData("https://slack.com/api/chat.postMessage",msg))
    #break # для отладки
    
# -

# ### Рассылка сообщения участникам группы
#
# Рассылаем просто текст...
#
# Немного пробовал как-то размечать студентов, но это пока "в прогрессе" (не уверен, что пойдет дальше).

text = """
Привет!
Дедлайн по вводному модулю сквозного курса "Реальный дата сайенс" близится, в нем есть задания, а результатов их выполнения Вами я не вижу...
Очень бы здорово выложить сделанное, чтобы я мог посмотреть и откомментировать.
Выполненные задания = переход на следующий модуль.
Если чем-то могу помочь - дайте знать :-)"""

text = data.remText
tag = "NOM0"

# +
# получим список директ мессаджей с пользователем
imList = slk_utils.getData('https://slack.com/api/conversations.list?types=im')["channels"]

for stud in data.studData:
    if stud["tag"]!=tag: # шлем только размеченным
        continue
    imChan = None
    for chan in imList:
        if chan["user"]==stud["id"]:
            imChan = chan["id"]
            break
    if imChan is None:
        print("No channel for user {}, ID={}".format(stud["name"], stud["id"]))
        continue
    msg = {
        "channel": imChan,
        "text": text, 
        "as_user": "true"
    }
    print(slk_utils.postData("https://slack.com/api/chat.postMessage",msg))

# -

# ### Работа с обратной связью
#
# * получение ответов от тех, с кем удалось пообщаться
# * получение списка тех, кому рассылал, но не получил никакого ответа

# +
# какие диалоги были

# получим историю директ мессаджей с пользователем
dmListRes = slk_utils.getData('https://slack.com/api/conversations.list?types=im')
dmList = dmListRes["channels"]

noAnsList = [] # сюда сложим все остальное
for cm in dmList:
    im = cm["user"]
    if im not in ids: # не рассматриваем здесь не участников группы
        continue
    if im in data.sfList: # не шлем сотрудникам
        continue
    res = slk_utils.getData('https://slack.com/api/conversations.history?channel='+cm["id"])
    #print(res)
    if res["ok"]:
        msgList = res["messages"]
        if len(msgList)>2: # был диалог
            # ПОТОМ СДЕЛАЕМ: посмотрим - было ли там мое изначальное сообщение (и начнем показ с него)
            print("USER:", students[im], "===========================")
            for m in msgList:
                ts = int(m["ts"].split(".")[0])
                if ts>data.stDate:
                    print("ME>" if m["user"]==data.ME else "US<",
                          datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'),
                          m["text"])
        else:
            noAnsList.append([len(msgList),im])
    else:
        noAnsList.append([-1,im])
# -

# с кем диалога вообще не было..
for noa in noAnsList:
    print(*noa, students[noa[1]])
print("Total silent:", len(noAnsList))

# ### Скорее для отладки
#
# Раньше я делал все через CURL...

# получим историю директ мессаджей с пользователем
res = !curl -X GET -H 'Authorization: Bearer '{token} -H 'Content-type: application/json; charset=utf-8' https://slack.com/api/conversations.history?channel=DPP5CNSNN 2>/dev/null
#print(res)
for m in json.loads(res[0])["messages"]:
    print("TEXT",m["text"])
