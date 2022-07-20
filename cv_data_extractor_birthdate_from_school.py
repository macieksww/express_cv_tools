from difflib import Match
import spacy
from spacy.matcher import Matcher
from csv_reader import read_csv
import re
from datetime import date

nlp = spacy.load("pl_core_news_lg")

def extract_birthdate_school(text, filename):
    office_dict = read_csv()
    office_dict = office_dict[3]

    matcher = Matcher(nlp.vocab)
    doc = nlp(text)
    has_mid = False
    has_gim = False
    has_close_dates = False
    mid_positions = []
    mid_position = []
    gim_positions = []
    gim_position = []
    school_type = ""
    dates = []
    close_dates = {}
    range = 10
    birth_date = 0
    age = 0

    # tworzenie patternow do znalezienia szkoły średniej

    mid_1 = [{"LOWER": {"REGEX":"szkoł"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"średni"}}]
    mid_2 = [{"LOWER": {"REGEX":"liceum"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"ogólnokształcące"}}]
    mid_3 = [{"LOWER": "lo"}]
    mid_4 = [{"LOWER": {"REGEX":"matura"}}]
    mid_5 = [{"LOWER": {"REGEX":"liceum"}}]
    mid_6 = [{"LOWER": {"REGEX":"średnie"}}]
    mid_7 = [{"LOWER": {"REGEX":"matura"}}]
    mid_8 = [{"LOWER": {"REGEX":"szk"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"ponadgim"}}]

    tech_1 = [{"LOWER": "szkół"}, {"OP": "?"},  {"OP": "?"}, {"LOWER": "zawodowych"}]
    tech_2 = [{"LOWER": {"REGEX":"szkoł"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"zawodow"}}]
    tech_3 = [{"LOWER": "egzamin"}, {"OP": "?"},  {"OP": "?"}, {"LOWER": "maturalny"}]
    tech_4 = [{"LOWER": {"REGEX":"technikum"}}]
    tech_5 = [{"LOWER": "zsz"}]
    tech_6 = [{"LOWER": "zsme"}]
    tech_7 = [{"LOWER": "zsb"}]
    tech_8 = [{"LOWER": "z.s.z."}]
    tech_9 = [{"LOWER": "z.s.me"}]
    tech_10 = [{"LOWER": "z.s.b."}]
    tech_11 = [{"LOWER": "z"}, {"OP": "?"},  {"OP": "?"}, {"LOWER": "s"}, {"OP": "?"},  {"OP": "?"}, {"LOWER": "z"}]
    tech_12 = [{"LOWER": "z"}, {"OP": "?"},  {"OP": "?"}, {"LOWER": "s"}]
    tech_13 = [{"LOWER": "z"}, {"OP": "?"},  {"OP": "?"}, {"LOWER": "s"}, {"OP": "?"},  {"OP": "?"}, {"LOWER": "b"}]
    tech_14 = [{"LOWER": {"REGEX":"technik"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"budow"}}]
    tech_15 = [{"LOWER": {"REGEX":"technik"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"geode"}}]
    tech_16 = [{"LOWER": {"REGEX":"technik"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"informaty"}}]
    tech_17 = [{"LOWER": {"REGEX":"technik"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"mechani"}}]
    tech_18 = [{"LOWER": {"REGEX":"technik"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"inynierii"}}]
    tech_19 = [{"LOWER": {"REGEX":"technik"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"elektroni"}}]
    tech_20 = [{"LOWER": {"REGEX":"technik"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"tele"}}]
    tech_21 = [{"LOWER": {"REGEX":"technik"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"logisty"}}]
    tech_22 = [{"LOWER": {"REGEX":"technik"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"mechatroni"}}]
    tech_23 = [{"LOWER": {"REGEX":"technik"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"transport"}}]
    tech_24 = [{"LOWER": {"REGEX":"wykształce"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"zawodowe"}}]
    tech_25 = [{"LOWER": {"REGEX":"wykształce"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"techniczne"}}]
    tech_26 = [{"LOWER": {"REGEX":"tytuł"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"technika"}}]
    tech_27 = [{"LOWER": {"REGEX":"zespół"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"szkół"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"zawodowych"}}]

    matcher_mid = Matcher(nlp.vocab)
    # matcher_mid.add("gimnazjum", [gim_1, gim_2])
    matcher_mid.add("technikum", [tech_1, tech_2, tech_3, tech_4, tech_5, tech_6,\
        tech_7, tech_8, tech_9, tech_10, tech_14, tech_15, tech_11, tech_12, tech_13,\
        tech_16, tech_17, tech_18, tech_19, tech_20, tech_21, tech_22, tech_23, tech_24,\
        tech_25, tech_26, tech_27])

    matcher_mid.add("liceum", [mid_1, mid_2, mid_3, mid_4, mid_5, mid_6, mid_7, mid_8])
    matches_mid = matcher_mid(doc)

    if len(matches_mid) > 0:
        has_mid = True
        for match_id, start, end in matches_mid:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            mid_positions.append([start, end, span.text])
            # print(match_id, string_id, start, end, span.text)
            school_type = str(string_id)

    
    # tworzenie patternow do znalezienia gimnazjum

    gim_1 = [{"LOWER": "gim"}]
    gim_2 = [{"LOWER": "gimnazjum"}]
    matcher_gim = Matcher(nlp.vocab)
    matcher_gim.add("gimnazjum", [gim_1, gim_2])
    matches_gim = matcher_gim(doc)
    if len(matches_gim) > 0:
        has_gim = True
        for match_id, start, end in matches_mid:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            gim_positions.append([start, end, span.text])
            # print(match_id, string_id, start, end, span.text)
            # school_type = str(string_id)

    # szukanie daty w okolicy informacji o szkole 
    # szukanie dat w uniwersalnych formatach liczbowych

    dp1 = [{'TEXT':{'REGEX':r'\d{1,2}/\d{1,2}/\d{2}(?:\d{2})?'}}]
    dp2 = [{'TEXT':{'REGEX':r'\d{1,2}/\d{2}(?:\d{2})?'}}]
    dp3 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{1,2}'}}]
    dp4 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{2}(?:\d{2})?'}}]
    dp5 = [{'IS_DIGIT': True}, {'ORTH': '-'}, {'IS_DIGIT': True}, {'ORTH': '-'}, {'IS_DIGIT': True}]
    dp6 = [{'IS_DIGIT': True}, {'ORTH': '-'}, {'IS_DIGIT': True}]
    # dp7 = [{'TEXT':{'REGEX':r'\d{4}'}}]
    dp7 = [{"SHAPE": "dddd"}]

    matcher_whole_date = Matcher(nlp.vocab)
    matcher_whole_date.add("data_pattern", [dp1, dp2, dp3, dp4, dp5, dp6, dp7])
    matches_whole_date = matcher_whole_date(doc)

    if len(matches_whole_date) > 0:

        for match_id, start, end in matches_whole_date:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            # print(match_id, string_id, start, end, span.text)
            dates.append([start, end, span.text])

    # szukanie daty z miesiącem w środku

    m1 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "sty"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{1,2}'}}]
    m2 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "lut"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{1,2}'}}]
    m3 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "mar"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{1,2}'}}]
    m4 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "kwi"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{1,2}'}}]
    m5 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "maj"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{1,2}'}}]
    m6 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "cze"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{1,2}'}}]
    m7 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "lip"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{1,2}'}}]
    m8 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "sie"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{1,2}'}}]
    m9 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "wrz"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{1,2}'}}]
    m10 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "paź"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{1,2}'}}]
    m11 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "lis"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{1,2}'}}]
    m12 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "gru"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{1,2}'}}]
    
    m13 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "sty"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{2}(?:\d{2})?'}}]
    m14 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "lut"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{2}(?:\d{2})?'}}]
    m15 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "mar"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{2}(?:\d{2})?'}}]
    m16 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "kwi"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{2}(?:\d{2})?'}}]
    m17 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "maj"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{2}(?:\d{2})?'}}]
    m18 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "cze"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{2}(?:\d{2})?'}}]
    m19 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "lip"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{2}(?:\d{2})?'}}]
    m20 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "sie"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{2}(?:\d{2})?'}}]
    m21 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "wrz"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{2}(?:\d{2})?'}}]
    m22 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "paź"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{2}(?:\d{2})?'}}]
    m23 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "lis"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{2}(?:\d{2})?'}}]
    m24 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {"LOWER": {"REGEX": "gru"}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{2}(?:\d{2})?'}}]

    matcher_month_date = Matcher(nlp.vocab)
    matcher_month_date.add("data_pattern", [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10,\
        m11, m12, m13, m14, m15, m16, m17, m18, m19, m20, m21, m22, m23, m24])
    matches_month_date = matcher_month_date(doc)

    if len(matches_month_date) > 0:
        for match_id, start, end in matches_month_date:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            # print(match_id, string_id, start, end, span.text)
            dates.append([start, end, span.text])

    
    if has_gim is True and has_mid is False:
        if len(dates) > 0:
            for date in dates:
                for gim_position in gim_positions:
                    if gim_position[2] not in close_dates.keys():
                        close_dates[gim_position[2]] = []
                    if date[0] > gim_position[0] - range and date[0] < gim_position[0] + range:
                        has_close_dates = True
                        close_dates[gim_position[2]].append([min(abs(date[0]-gim_position[1]), abs(date[1]-gim_position[0])), date[2]])

        # print ("gim_position")
        # print (gim_position)
        
        if has_close_dates is True:
            dates_by_gim=[]
            for key in close_dates.keys():
                cd = close_dates[key]
                if len(cd) > 0:
                    sorted_close_dates = sorted(cd, key=lambda x: x[0])
                    dates_by_gim.append(sorted_close_dates[0][1])
            # print ("dates by mid school")
            # print (dates_by_mid_school)
            birth_date = min(dates_by_gim)
            birth_date = process_birth_date(birth_date)
            if birth_date == 0:
                return(0)
            else:
                age = calculate_age_gim(birth_date)
        return (age)



    if has_mid is True:
        if len(dates) > 0:
            for date in dates:
                for mid_position in mid_positions:
                    if mid_position[2] not in close_dates.keys():
                        close_dates[mid_position[2]] = []
                    if date[0] > mid_position[0] - range and date[0] < mid_position[0] + range:
                        has_close_dates = True
                        close_dates[mid_position[2]].append([min(abs(date[0]-mid_position[1]), abs(date[1]-mid_position[0])), date[2]])

        # print ("mid positions")
        # print (mid_positions)
        
        if has_close_dates is True:
            dates_by_mid_school=[]
            for key in close_dates.keys():
                cd = close_dates[key]
                if len(cd) > 0:
                    sorted_close_dates = sorted(cd, key=lambda x: x[0])
                    dates_by_mid_school.append(sorted_close_dates[0][1])
            # print ("dates by mid school")
            # print (dates_by_mid_school)
            birth_date = min(dates_by_mid_school)
            birth_date = process_birth_date(birth_date)
            if birth_date == 0:
                return(0)
            else:
                print("Age from school")
                age = calculate_age(birth_date, school_type)
                print(age)
    return (age)

def process_birth_date(birth_date):
    years = re.findall('(\d{4})', birth_date)
    years = [int(year) for year in years]
    if len(years)>0:
        return(max(years))
    else:
        return(0)

def calculate_age(birth_date, school_type):

    if school_type == "liceum":
        year_offset = 19
    elif school_type == "technikum":
        year_offset = 20
    curr_year = date.today().year
    age = int(curr_year)-int(birth_date)+year_offset
    
    return age

def calculate_age_gim(birth_date):
    year_offset = 16
    curr_year = date.today().year
    age = int(curr_year)-int(birth_date)+year_offset
