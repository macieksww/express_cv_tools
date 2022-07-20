import spacy
from spacy import displacy
from spacy.matcher import Matcher
import os
import csv

nlp = spacy.load("pl_core_news_lg")
exp_dict = {
            'name': [],
            'cc': [],
            'cs': [],
            'ovr': [],
            'oth': [],
            }

cv_part_dict = {
            'exp': [],
            'cap': [],
            'edu': [],
            'hbb': [],
            'ach': [],
            }

eng_dict = {
            'no': [],
            'basic': [],
            'int': [],
            'good': [],
            }

office_dict = {
            'name': [],
            'basic': [],
            'good': [],
            }

edu_dict = {
            'name': [],
            'mid': [],
            'high': [],
            'still': [],
            'unfn': [],
            'ground': [],
}

# funkcja do odczytania plikow csv z patternami do poszczegolnych podkategorii dla kategoii
# i okresleniami definiujacymi poszczegolne czesci cv

def read_csv(path='experience.csv'):
    rows = []
    for i in range(0,5):
        file = open('experience.csv')
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            row = row[i].split(';')
            if row[0] != '':
                if i == 0:
                    exp_dict['name'].append(row[0])
                elif i == 1:
                    exp_dict['cc'].append(row[0])
                elif i == 2:
                    exp_dict['cs'].append(row[0])
                elif i == 3:
                    exp_dict['ovr'].append(row[0])
                elif i == 4:
                    exp_dict['oth'].append(row[0])

    for i in range(0,5):
        file = open('cv_parts.csv')
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            row = row[i].split(';')
            if row[0] != '':
                if i == 0:
                    cv_part_dict['exp'].append(row[0])
                elif i == 1:
                    cv_part_dict['cap'].append(row[0])
                elif i == 2:
                    cv_part_dict['edu'].append(row[0])
                elif i == 3:
                    cv_part_dict['hbb'].append(row[0])
                elif i == 4:
                    cv_part_dict['ach'].append(row[0])

    for i in range(0,4):
        file = open('eng.csv')
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            row = row[i].split(';')
            if row[0] != '':
                if i == 0:
                    eng_dict['no'].append(row[0])
                elif i == 1:
                    eng_dict['basic'].append(row[0])
                elif i == 2:
                    eng_dict['int'].append(row[0])
                elif i == 3:
                    eng_dict['good'].append(row[0])

    for i in range(0,3):
        file = open('office.csv')
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            row = row[i].split(';')
            if row[0] != '':
                if i == 0:
                    office_dict['name'].append(row[0])
                elif i == 1:
                    office_dict['good'].append(row[0])
                elif i == 2:
                    office_dict['basic'].append(row[0])

    for i in range(0,6):
        file = open('education.csv')
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            row = row[i].split(';')
            if row[0] != '':
                if i == 0:
                    edu_dict['name'].append(row[0])
                elif i == 1:
                    edu_dict['mid'].append(row[0])
                elif i == 2:
                    edu_dict['high'].append(row[0])
                elif i == 3:
                    edu_dict['still'].append(row[0])
                elif i == 4:
                    edu_dict['unfn'].append(row[0])
                elif i == 5:
                    edu_dict['ground'].append(row[0])

    return (exp_dict, cv_part_dict, eng_dict, office_dict, edu_dict)
