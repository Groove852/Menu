import random
import requests
import pandas as pd

URL_MASTER = 'https://shoko.ru/'
URL_POSES = []
MENU = []
VALUE_ALL = []

text = "Are you ready?\n"

compound = pd.read_excel("https://shoko.ru/upload/iblock/b24/b240901d66729a4f5190fb8506724858.xlsx",
                         engine='openpyxl',
                         sheet_name='Прейскурант-город',
                         usecols='F')

name = pd.read_excel("https://shoko.ru/upload/iblock/b24/b240901d66729a4f5190fb8506724858.xlsx",
                     engine='openpyxl',
                     sheet_name='Прейскурант-город',
                     usecols='B')


def parse(url, key):
    for lines in requests.get(url + key).text.split('<'):
        if lines[0:13] == 'a href=\"/menu':
            if lines.split("\"")[1] not in URL_POSES and lines.split("\"")[1] != '/menu/':
                URL_POSES.append(lines.split("\"")[1])
    for pose in URL_POSES:
        url_pose = url + pose[1:]
        for lines in requests.get(url_pose).text.split('<'):
            if lines[0:3] == "h4>" and lines[3:] not in MENU:
                MENU.append(lines[3:])
    MENU.remove('Ваш город Москва?')
    MENU.remove('О компании')
    MENU.remove('Акции')
    MENU.remove('')


def learn():
    global text
    while True:
        if input(text) == "end" or "End":
            break
        else:
            text = "Next or End?\n"
            value = random.randint(0, len(MENU))
            if value not in VALUE_ALL:
                pose = MENU[value]
                print(f'Блюдо - {pose}\n')
                VALUE_ALL.append(value)
                if input("Show?(yes/no)\n") == "yes":
                    find_element(pose)


def find_element(pose):
    for i in range(56, name.size):
        if name.iloc[i].to_dict()['Unnamed: 1'] == pose:
            print(f'Состав: {compound.iloc[i].to_dict()["Unnamed: 5"]}\n')


if __name__ == '__main__':
    parse(URL_MASTER, "menu/")
    learn()
