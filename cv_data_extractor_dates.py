import itertools
from lib2to3.pgen2 import token
from matplotlib import dates
import spacy
from spacy import displacy
from spacy.matcher import Matcher
import os
import re
import datetime
import itertools
from dateutil.relativedelta import relativedelta

nlp = spacy.load("pl_core_news_lg")

def process_directory(path):
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            print(filename)
            with open( path + "/" + filename, "r") as file:
                text = file.read()
                extract_birth_date(text, filename)


def find_dates_spacy(doc):
    lastPos = 0
    charsBetween = 1
    dateEntityList = []
    dateEntities = []
    for ent in doc.ents:
        if ent.label_ == "date":
            if lastPos + charsBetween >= ent.start_char:
                dateEntities.append(ent)
            else:
                if len(dateEntities) > 0:
                    #for dateSegment in dateEntityList:
                        #print(dateSegment.text, end =" ")
                    #print("")
                    dateEntityList.append(dateEntities)
                    dateEntities = []
                dateEntities.append(ent)
            lastPos = ent.end_char
            #print(ent.text, ent.start_char, ent.end_char, ent.label_)
    if len(dateEntities) > 0:
        #for dateSegment in dateEntityList:
            #print(dateSegment.text, end =" ")
        #print("")
        dateEntityList.append(dateEntities)
    print(dateEntityList)
    return dateEntityList

def get_year(input):
    #znalezienie 4 cyfr ze znakami innymi niż cyfry z każdej strony lub bez dodatkowych znaków i zamiana na liczbę
    matches = re.findall("^[0-9]{4}[^0-9]", input)
    matches.extend(re.findall("^[0-9]{4}$", input))
    matches.extend(re.findall("[^0-9][0-9]{4}[^0-9]", input))
    matches.extend(re.findall("[^0-9][0-9]{4}$", input))
    year = 0
    for match in matches:
        yearStr = re.findall("[0-9]{4}", match)
        if len(yearStr) == 1:
            yearConv = int(yearStr[0])
            if yearConv > 1900 and yearConv < 2050:
                if year == 0:
                    year = yearConv
                else:
                    print("Multiple match: " + str(year) + " " + str(yearConv))
                    return 0
        else:
            print("No year match: " + match)
    return year

def is_year(input):
    #sprawdzenie czy słowo zawiera 4 cyfry ze znakami innymi niż cyfry z każdej strony lub bez dodatkowych znaków
    if(get_year(input) > 0):
        return True
    else:
        return False

def get_month(input):
    months_1 = ["styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", "lipiec", "sierpień", "wrzesień", "pażdzernik", "listopad", "grudzień"]
    months_2 = ["sty", "lut", "mar", "kwi", "maj", "cze", "lip", "sie", "wrz", "paż", "lis", "gru"]
    months_3 = ["^I$", "^II$", "^III$", "^IV$", "^V$", "^VI$", "^VII$", "^VIII$", "^IX$", "^X$", "^XI$", "^XII$"]
    for i in range(0, len(months_1)):
        month_matches = re.findall(months_1[i], input.lower())
        if len(month_matches) > 0:
            return i+1
    for i in range(0, len(months_2)):
        month_matches = re.findall(months_2[i], input.lower())
        if len(month_matches) > 0:
            return i+1
    roman_matches = re.findall("[IVX]+", input)
    if len(roman_matches) > 0:
        for i in range(0, len(months_3)):
            month_matches = re.findall(months_3[i], roman_matches[0])
            if len(month_matches) > 0:
                return i+1
    #znalezienie 4 cyfr ze znakami innymi niż cyfry z każdej strony lub bez dodatkowych znaków i zamiana na liczbę
    matches = re.findall("^[0-9]{2}[^0-9]", input)
    matches.extend(re.findall("^[0-9]{2}$", input))
    matches.extend(re.findall("[^0-9][0-9]{2}[^0-9]", input))
    matches.extend(re.findall("[^0-9][0-9]{2}$", input))
    if len(matches) == 0:
        matches.extend(re.findall("^[0-9]{1}[^0-9]", input))
        matches.extend(re.findall("^[0-9]{1}$", input))
        matches.extend(re.findall("[^0-9][0-9]{1}$", input))
    month = 0
    for match in matches:
        monthStr = re.findall("[0-9]{2}", match)
        if(len(monthStr)==0):
            monthStr = re.findall("[0-9]{1}", match)
        if len(monthStr) == 1:
            monthConv = int(monthStr[0])
            if monthConv > 0 and monthConv < 13:
                if month == 0:
                    month = monthConv
                else:
                    print("Multiple match: " + str(month) + " " + str(monthConv))
                    return 0
        else:
            print("No month match: " + match)
    return month

def is_month(input):
    #sprawdzenie czy słowo zawiera 4 cyfry ze znakami innymi niż cyfry z każdej strony lub bez dodatkowych znaków
    if(get_month(input) > 0):
        return True
    else:
        return False

def is_token_part_of_entity(token, entity):
    if token.i >= entity.start and token.i < entity.end:
        return True
    else:
        return False


def find_dates_rule(dateEntityList, doc):
    dateList = []
    for token in doc:
        _date = []
        #sprawdzenie czy słowo oznacza rok
        if is_year(token.text):
            #is_already_included = False
            #sprawdzenie, czy słowo było już wykryte
            #for entList in dateEntityList:
            #    for ent in entList:
            #        if is_token_part_of_entity(token, ent):
            #            is_already_included = True
            #    if is_already_included:
            #        break
            if token.ent_type_ != 'date':
                #dodanie słowa do listy
                _date.append(token)
                dateList.append(_date)
    return dateList
        


def split_dates(dateEntityList, doc):
    #sprawdzenie czy data zawiera rok podany dwukrotnie
    dates_split = 0
    for date_pos in range(len(dateEntityList)):
        currentDate = dateEntityList[date_pos]
        yearEntPos = []
        for ent_pos in range(len(currentDate)):
            if is_year(currentDate[ent_pos].text):
                yearEntPos.append(ent_pos)
        if len(yearEntPos) > 1:
            #wyznaczenie miejsca podziału - jeżeli oba lata mają słowa przed sobą, to podział jest po pierwszym roku
            #jeżeli oba lata mają słowa za sobą, to podział jest przed drugim rokiem
            #w innym przypadku podział jest po pierwszym roku
            if yearEntPos[0] == 0 and yearEntPos[1] < len(currentDate)-1:
                new_list_1 = currentDate[:yearEntPos[1]]
                new_list_2 = currentDate[yearEntPos[1]:]
                dateEntityList[date_pos] = new_list_2
                dateEntityList.insert(date_pos, new_list_1)
            else:
                new_list_1 = currentDate[:yearEntPos[0]+1]
                new_list_2 = currentDate[yearEntPos[0]+1:]
                dateEntityList[date_pos] = new_list_2
                dateEntityList.insert(date_pos, new_list_1)
            dates_split += 1
                
    return dates_split

def entity_list_to_token_list(entityList, doc):
    tokenList = []
    for entity in entityList:
        for token in doc:
            if is_token_part_of_entity(token, entity):
                tokenList.append(token)
    return tokenList

def extend_dates(dateList, doc):
    #sprawdzenie czy słowo z dwoma lub jedną cyfrą nie występuje bezpośrednio przed lub po dacie
    #tokens_to_check = 2
    #max_token_size = 4
    dates_extended = 0
    for date in dateList:
        already_has_month = False
        for token in date:
            if is_month(token.text) or is_month(token.lemma_):
                already_has_month = True
        #TODO: dodać sprawdzenie miesięcy słowami
        if not already_has_month:
            #for i in reversed(range(date[0].i - tokens_to_check, date[0].i)):
            for i in [date[0].i - 1, date[0].i - 2, date[0].i + 1, date[0].i + 2]:
                if i >= 0 and i < len(doc):
                    if is_year(doc[i].text):
                        break
                    else:
                        if is_month(doc[i].text) or is_month(token.lemma_):
                            date.insert(0, doc[i])
                            dates_extended += 1
                            break
    #print("Dates extended: " + str(dates_extended))

                


def interpret_dates(dateList, doc):
    interpretedDates = []
    for date in dateList:
        yearIndex = -1
        year = 0
        month = 0
        for i in range(len(date)):
            yearTmp = get_year(date[i].text)
            if yearTmp != 0:
                yearIndex = i
                year = yearTmp
                break
        if year > 0:
            r1 = reversed(range(0,yearIndex+1))
            r2 = range(yearIndex+1, len(date))
            for i in itertools.chain(r1,r2):
                token = date[i]
                month_text = get_month(token.text)
                month_lemma = get_month(token.lemma_)
                if month_lemma > 0:
                    month = month_lemma
                    break
                if month_text > 0:
                    month = month_text
                    break
        if year > 0 and month == 0:
            month = 6
        if year > 0:
            interpretedDates.append(datetime.date(year,month, 15))
        else:
            interpretedDates.append(None)
    return interpretedDates


def extract_birth_date(text, filename):
    #matcher = Matcher(nlp.vocab)
    doc = nlp(text)
#    for token in doc:
#        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#            token.shape_, token.is_alpha, token.is_stop)
    dateEntityList = find_dates_spacy(doc)
    #print("spaCy dates: "+ str(len(dateEntityList)))
    #for date in dateEntityList:
    #    for ent in date:
    #        print(ent.text, end =" ")
    #    print("")
    dateList = find_dates_rule(dateEntityList, doc)
    dates_split_count = 1
    while dates_split_count != 0:
        dates_split_count = split_dates(dateEntityList, doc)
    #print("spaCy dates after splitting: "+ str(len(dateEntityList)) + "Regex matched dates: " + str(len(dateList)))
    for entityList in dateEntityList:
        dateList.append(entity_list_to_token_list(entityList, doc))
    extend_dates(dateList, doc)
    #for date in dateList:
        #print(str(date))
    interpretedDates = interpret_dates(dateList, doc)
    #for i in range(len(dateList)):
    #    dateStr = "[None]"
    #    if interpretedDates[i] is not None:
    #        dateStr = interpretedDates[i].strftime("%Y-%m")
    #    print(str(dateList[i])+" "+dateStr)

    sortedDates = []
    for date in interpretedDates:
        if date is not None:
            sortedDates.append(date)
    sortedDates.sort()

    #for i in range(len(sortedDates)):
    #    dateStr = sortedDates[i].strftime("%Y-%m")
    #    print(dateStr)
    if len(sortedDates) > 1:
        # print("Years diff. :" + str(relativedelta(sortedDates[1],  sortedDates[0]).years)) 
        if relativedelta(sortedDates[1],  sortedDates[0]).years > 6:
            return sortedDates[0]
    else:
        return None

#print("Zaakceptowane:")
#process_directory("dane/z")
#print("Odrzucone:")
#process_directory("dane/o")
