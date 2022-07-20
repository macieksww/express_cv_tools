from fileinput import close
import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from csv_reader import read_csv


nlp = spacy.load("pl_core_news_lg")

def extract_education(text, filename):
    edu_dict = read_csv()
    edu_dict = edu_dict[4]

    doc = nlp(text)
    has_edu = False
    has_ground_edu = False
    has_mid_edu = False
    has_high_edu = False
    has_still_edu = False
    has_tech_edu = False
    has_unfn_edu = False
    edu_list = []
    master_studies = False
    high_edu_pos = []
    dates = []
    close_dates = {}
    closest_dates = {}
    close_still_phrases = {}
    close_break_phrases = {}
    still_acceptance_rate = 15
    break_acceptance_rate = 15
    range = 20

    # szukanie daty w okolicy informacji o wyższym wykształceniu
    # wykorzystane w celu sprawdzenia, czy osoba która aktualnie studiuje ukończyła już jakiś kierunek
    # szukanie dat w uniwersalnych formatach liczbowych

    d_1 = [{'TEXT':{'REGEX':r'\d{1,2}/\d{1,2}/\d{2}(?:\d{2})?'}}]
    d_2 = [{'TEXT':{'REGEX':r'\d{1,2}/\d{2}(?:\d{2})?'}}]
    d_3 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{1,2}'}}]
    d_4 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{2}(?:\d{2})?'}}]
    d_5 = [{'IS_DIGIT': True}, {'ORTH': '-'}, {'IS_DIGIT': True}, {'ORTH': '-'}, {'IS_DIGIT': True}]
    d_6 = [{'IS_DIGIT': True}, {'ORTH': '-'}, {'IS_DIGIT': True}]

    matcher_whole_date = Matcher(nlp.vocab)
    matcher_whole_date.add("data_pattern", [d_1, d_2, d_3, d_4, d_5, d_6])
    matches_whole_date = matcher_whole_date(doc)

    if len(matches_whole_date) > 0:
        for match_id, start, end in matches_whole_date:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            # print(match_id, string_id, start, end, span.text)
            dates.append([start, end, span.text])

    # tworzenie patternow do znalezienia poziomu wykształcenia
    # wykształcenie podstawowe
    edu_ground_list = list(edu_dict['ground'])
    edu_ground_pattern = [{"LOWER": {"IN": edu_ground_list}}]
    matcher_ground_edu = Matcher(nlp.vocab)
    matcher_ground_edu.add("ground_edu", [edu_ground_pattern])
    matches_ground_edu = matcher_ground_edu(doc)

    if len(matches_ground_edu) > 0:
        for match_id, start, end in matches_ground_edu:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            # if start <= knows_office_position + range and start >= knows_office_position-range:
            edu_list.append([1, "ground"])

    # wykształcenie średnie 

    mid_1 = [{"LOWER": {"REGEX":"szkoł"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"średni"}}]
    mid_2 = [{"LOWER": {"REGEX":"liceum"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"ogólnokształcące"}}]
    mid_3 = [{"LOWER": "lo"}]
    mid_4 = [{"LOWER": {"REGEX":"matura"}}]
    mid_5 = [{"LOWER": {"REGEX":"liceum"}}]
    mid_6 = [{"LOWER": {"REGEX":"średnie"}}]
    mid_7 = [{"LOWER": {"REGEX":"matura"}}]
    mid_8 = [{"LOWER": "zse"}]
    mid_9 = [{"LOWER": "zs"}]
    mid_8 = [{"LOWER": "z.s.e."}]
    mid_9 = [{"LOWER": "z.s."}]
    mid_10 = [{"LOWER": {"REGEX":"szk"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"ponadgim"}}]

    matcher = Matcher(nlp.vocab)
    matcher.add("srednie", [mid_1, mid_2, mid_3, mid_4, mid_5, mid_6, mid_7, mid_8, mid_9, mid_10])
    matches = matcher(doc)
    
    if len(matches) > 0:
        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            edu_list.append([2, "mid"])

    # wykształcenie średnie techniczne

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



    matcher = Matcher(nlp.vocab)
    matcher.add("tech/zaw", [tech_1, tech_2, tech_3, tech_4, tech_5, tech_6,\
        tech_7, tech_8, tech_9, tech_10, tech_14, tech_15, tech_11, tech_12, tech_13,\
        tech_16, tech_17, tech_18, tech_19, tech_20, tech_21, tech_22, tech_23, tech_24,\
             tech_25, tech_26, tech_27])
    matches = matcher(doc)
    
    if len(matches) > 0:
        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            edu_list.append([3, "tech"])


    # wykształcenie wyższe

    edu_high_list = list(edu_dict['high'])
    edu_high_pattern = [{"LOWER": {"IN": edu_high_list}}]
    matcher_high_edu = Matcher(nlp.vocab)
    matcher_high_edu.add("high_edu", [edu_high_pattern])
    matches_high_edu = matcher_high_edu(doc)

    msc_1 = [{"LOWER": "wyształcenie"}, {"OP": "?"},  {"OP": "?"}, {"LOWER": "wyższe"}]
    msc_2 = [{"LOWER": {"REGEX":"magister"}}]
    msc_3 = [{"LOWER": {"REGEX":"master"}}]
    msc_4 = [{"LOWER": "msc"}]
    msc_5 = [{"LOWER": {"REGEX":"podyplom"}}]

    bsc_1 = [{"LOWER": {"REGEX":"wyższa"}}, {"OP": "?"},  {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX":"szkoła"}}]
    bsc_2 = [{"LOWER": {"REGEX":"uniwersyte"}}]
    bsc_3 = [{"LOWER": {"REGEX":"politechnika"}}]
    bsc_4 = [{"LOWER": {"REGEX":"licencj"}}]
    bsc_5 = [{"LOWER": {"REGEX":"akademia"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"wychowania"}}]
    bsc_6 = [{"LOWER": {"REGEX":"akademia"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"wychowania"}}]
    bsc_7 = [{"LOWER": {"REGEX":"bachelor"}}]
    bsc_8 = [{"LOWER": "bsc"}]
    bsc_9 = [{"LOWER": "awf"}]
    bsc_10 = [{"LOWER": "asp"}]
    bsc_11 = [{"LOWER": {"REGEX":"inynier"}}]
    bsc_12 = [{"LOWER": {"REGEX":"wykształcenie"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"wyższe"}}]
    bsc_13 = [{"LOWER": {"REGEX":"szkoła"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"główna"}}]

    matcher = Matcher(nlp.vocab)
    matcher.add("bsc", [bsc_1, bsc_2, bsc_3, bsc_4, bsc_5, bsc_6\
    , bsc_7, bsc_8, bsc_9, bsc_10, bsc_11, bsc_12, bsc_13])
    matcher.add("msc", [msc_1, msc_2, msc_3, msc_4, msc_5])
    matches = matcher(doc)
    

    if len(matches_high_edu) > 0:
        for match_id, start, end in matches_high_edu:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            edu_list.append([4, "high"])
            high_edu_pos.append([start, end, span.text])
            has_high_edu = True

    if len(matches) > 0:
        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            edu_list.append([4, "high"])
            high_edu_pos.append([start, end, span.text])
            has_high_edu = True
            if string_id == "msc":
                master_studies = True

    # print('high edu positions')
    # print(high_edu_pos)

    # wykształcenie w trakcie

    edu_still_list = list(edu_dict['still'])
    edu_still_pattern = [{"LOWER": {"IN": edu_still_list}}]
    matcher_still_edu = Matcher(nlp.vocab)
    matcher_still_edu.add("still_edu", [edu_still_pattern])
    matches_still_edu = matcher_still_edu(doc)
    # terms = ["1 rok", "2 rok", "pierwszy rok", "drugi rok"]
    # patterns = [nlp.make_doc(text) for text in terms]

    still_1 = [{"LOWER": "1"}, {"OP": "?"}, {"LOWER": {"REGEX": "rok"}}]
    still_2 = [{"LOWER": "2"}, {"OP": "?"}, {"LOWER": {"REGEX": "rok"}}]   
    still_3 =  [{"LOWER": "rok"}]
    still_4 = [{"LOWER": {"REGEX": "pierwszy"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "rok"}}]    
    still_5 = [{"LOWER": {"REGEX": "drugi"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "rok"}}]
    still_6 = [{"LOWER": {"REGEX": "nadal"}}]
    still_7 = [{"LOWER": {"REGEX": "teraz"}}]
    still_8 = [{"LOWER": {"REGEX": "obecnie"}}]
    still_9 = [{"LOWER": {"REGEX": "w"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "trakcie"}}]

    matcher = Matcher(nlp.vocab)
    matcher.add("still", [still_1, still_2, still_3, still_4, still_5,\
    still_6, still_7, still_8, still_9])
    matches = matcher(doc)

    if has_high_edu is True:
        if master_studies is False:
            # przeszukanie odległości od znalezionych dat, do miejsca, w którym
            # wystąpiła informacja o wyższym wykształceniu
            for edu_pos in high_edu_pos:
                close_dates[edu_pos[2]] = []
                for date in dates:
                    temp_close_dates = []

                    # dodanie daty do listy dat bliskich, w wypaku gdy znajduje się
                    # w promieniu "range". Wybierana jest bliższa odległość - (od końca daty
                    # do początku określenia oznacajcego szkołę wyższą lub odwrotnie)

                    if abs(date[1]-edu_pos[0]) < range:
                        temp_close_dates.append(abs(date[1]-edu_pos[0])) 
                    if abs(date[0]-edu_pos[1]) < range:
                        temp_close_dates.append(abs(date[0]-edu_pos[1]))
                    if len(temp_close_dates) > 0:
                        close_dates[edu_pos[2]].append(min(temp_close_dates))
            print("close dates")
            print(close_dates)

            # znaleziono daty bliskie informacji o wyższym wykształceniu
            if len(close_dates) > 0:
                for key in close_dates.keys():
                    if len(close_dates[key]) > 0:
                        closest_dates[key] = min(close_dates[key])
            
            # dodanie do listy closest dates daty najbliższej do 
            # określenia oznacajcego szkołę wyższą
            
            # dodanie sufiksu inc w przypadku gdy fraza określająca szkołę wyższą
            # powtórzyła się 

            inc=1
            if len(high_edu_pos) > 0:
                print(high_edu_pos)

            for high_edu_position in high_edu_pos:

                # same_uni - flaga zabezpieczajaca przed dodaniem jednej szkoly wyzszej o takiej samej nazwie np. "uniwersytet"
                # znajdujacej sie na tym samym miejscu w tekscie, kilka razy

                same_uni = 0
                if len(matches_still_edu) > 0:
                    for match_id, start, end in matches_still_edu:
                        string_id = nlp.vocab.strings[match_id]
                        span = doc[start:end]
                        print(match_id, string_id, start, end, span.text)
                        # if str(span.text) in closest_dates.keys():
                        if start > high_edu_position[0]-range and start < high_edu_position[0]+range:
                            if high_edu_position[2] not in  close_still_phrases.keys():
                                close_still_phrases[high_edu_position[2]] = min(abs(high_edu_position[1]-start), abs(high_edu_position[0]-end))
                                same_uni = 1
                            else:
                                if same_uni == 0:
                                    close_still_phrases[str(high_edu_position[2])+str(inc)] = min(abs(high_edu_position[1]-start), abs(high_edu_position[0]-end))
                                    inc = inc+1

                if len(matches) > 0:
                    for match_id, start, end in matches:
                        string_id = nlp.vocab.strings[match_id]
                        span = doc[start:end]
                        print(match_id, string_id, start, end, span.text)
                        if start > high_edu_position[0]-range and start < high_edu_position[0]+range:
                            if high_edu_position[2] not in close_still_phrases.keys():
                                close_still_phrases[high_edu_position[2]] = min(abs(high_edu_position[1]-start), abs(high_edu_position[0]-end))
                                same_uni = 1
                            else:
                                if same_uni == 0:
                                    close_still_phrases[str(high_edu_position[2])+str(inc)] = min(abs(high_edu_position[1]-start), abs(high_edu_position[0]-end))
                                    inc = inc+1
                    
               
            if len(close_still_phrases) > 0:
                print("keys")
                print(close_still_phrases.keys())
                print(close_still_phrases)
            
            # dodane odległości od fraz określających nieukończone studia
            
            if len(close_still_phrases) > 0 and len(closest_dates) == 0:
                if len(close_still_phrases) == len(high_edu_pos):
                    return([0, 1, 0, 0, 0, 0])

            if len(closest_dates) > 0:
                print(closest_dates)
         
            if len(close_still_phrases) > 0 and len(closest_dates) == len(close_still_phrases):
                print(close_dates.keys())
                print(close_still_phrases.keys())
                for key_d, value_d in closest_dates.items():
                    for key_s, value_s in close_still_phrases.items():
                        if key_d == key_s:
                            if value_s-still_acceptance_rate > value_d:
                                return([1, 0, 0, 0, 0, 0])
                return([0, 1, 0, 0, 0, 0])



    # wykształcenie wyższe przerwane

    break_1 = [{"LOWER": {"REGEX": "przerwa"}}]    

    matcher = Matcher(nlp.vocab)
    matcher.add("break", [break_1])
    matches = matcher(doc)

    if has_high_edu is True:
        if master_studies is False:
            inc=1
            if len(high_edu_pos) > 0:
                print(high_edu_pos)

            for high_edu_position in high_edu_pos:

                # same_uni - flaga zabezpieczajaca przed dodaniem jednej szkoly wyzszej o takiej samej nazwie np. "uniwersytet"
                # znajdujacej sie na tym samym miejscu w tekscie, kilka razy

                same_uni = 0

                if len(matches) > 0:
                    for match_id, start, end in matches:
                        string_id = nlp.vocab.strings[match_id]
                        span = doc[start:end]
                        print(match_id, string_id, start, end, span.text)
                        if start > high_edu_position[0]-range and start < high_edu_position[0]+range:
                            if high_edu_position[2] not in close_break_phrases.keys():
                                close_break_phrases[high_edu_position[2]] = min(abs(high_edu_position[1]-start), abs(high_edu_position[0]-end))
                                same_uni = 1
                            else:
                                if same_uni == 0:
                                    close_break_phrases[str(high_edu_position[2])+str(inc)] = min(abs(high_edu_position[1]-start), abs(high_edu_position[0]-end))
                                    inc = inc+1
                    
               
            if len(close_break_phrases) > 0:
                print("keys")
                print(close_break_phrases.keys())
                print(close_break_phrases)
            
            # dodane odległości od fraz określających nieukończone studia
            
            if len(close_break_phrases) > 0 and len(closest_dates) == 0:
                if len(close_break_phrases) == len(high_edu_pos):
                    return([0, 0, 1, 0, 0, 0])

            if len(closest_dates) > 0:
                print(closest_dates)
         
            if len(close_break_phrases) > 0 and len(closest_dates) == len(close_break_phrases):
                print(close_dates.keys())
                print(close_break_phrases.keys())
                for key_d, value_d in closest_dates.items():
                    for key_s, value_s in close_break_phrases.items():
                        if key_d == key_s:
                            if value_s-break_acceptance_rate > value_d:
                                return([1, 0, 0, 0, 0, 0])
                return([0, 0, 1, 0, 0, 0])


    # finding education level
    if not edu_list:
        edu_level = "no"
    else:
        edu_level = sorted(edu_list, key = lambda i: i[0], reverse = True)[0][1]

    if edu_level == "high": 
        return([1, 0, 0, 0, 0, 0])
    elif edu_level == "still":
        return([0, 1, 0, 0, 0, 0])
    elif edu_level == "mid":
        return([0, 0, 1, 0, 0, 0])
    elif edu_level == "tech":
        return([0, 0, 0, 1, 0, 0])
    elif edu_level == "ground":
        return([0, 0, 0, 0, 1, 0])
    else:
        return([0, 0, 0, 0, 0, 1])
