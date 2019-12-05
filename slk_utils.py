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

# Тут всякие утилитные функции, чтобы не замусоривать другие книжки

import requests, json

token = "xoxp-6..."
headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'Authorization': 'Bearer ' + token
}


# +
def getData(url):
    """ возвращает JSON с результатом GET запроса или None если вернулась ошибка 
    пока непонятно - почему может быть ошибка..."""
    
    resp = requests.get(url, headers=headers)
    
    if resp:
        return resp.json()
    else:
        return None

def postData(url,data):
    """ постит данные по урлу """
    
    resp = requests.post(url, data=json.dumps(data), headers=headers)
    
    if resp:
        return resp.json()
    else:
        return resp.text    
# -


