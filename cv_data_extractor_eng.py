import spacy
from spacy.matcher import Matcher
from csv_reader import read_csv

nlp = spacy.load("pl_core_news_lg")

def extract_english(text, filename):
    eng_dict = read_csv()
    eng_dict = eng_dict[2]

    matcher = Matcher(nlp.vocab)
    doc = nlp(text)
    knows_eng_basic= False
    knows_eng_int = False
    knows_eng_no = False
    knows_eng_good = False
    knows_eng = False
    knows_eng_positions = []
    knows_eng_position = 0
    level_list = []
    srz_end = 0
    zaw_end = 0

    range = 20

    # tworzenie patternow do znalezienia poziomu angielskiegu
    # sprawdzenie znajomosci (tak/nie)
    eng_no_list = list(eng_dict['no'])
    eng_no_pattern = [{"LOWER": {"IN": eng_no_list}}]
    matcher_no_eng = Matcher(nlp.vocab)
    matcher_no_eng.add("no_eng", [eng_no_pattern])
    matches_no_eng = matcher_no_eng(doc)

    matcher_eng_ph = Matcher(nlp.vocab)
    e1 = [{"LOWER": {"REGEX": "english"}}]    
    e2 = [{"LOWER": {"REGEX": "j"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "angielski"}}]
    e3 = [{"LOWER": {"REGEX": "angielski"}}]
    e4 = [{"LOWER": {"REGEX": "język"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "ang"}}]
    e5 = [{"LOWER": {"REGEX": "język"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "angielski"}}]

    matcher_eng_ph.add("ph", [e1, e2, e3, e4, e5])
    matches_eng_ph = matcher_eng_ph(doc)

    if len(matches_no_eng) > 0:
        for match_id, start, end in matches_no_eng:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            knows_eng_positions.append(start)
        knows_eng = True
        # knows_eng_position_1 = min(knows_eng_positions)
    
    if len(matches_eng_ph) > 0:
        for match_id, start, end in matches_eng_ph:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            knows_eng_positions.append(start)
        knows_eng = True
        # knows_eng_position = min(knows_eng_positions)


    # sprawdzenie znajomosci podstawowej

    eng_basic_list = list(eng_dict['basic'])
    eng_basic_pattern = [{"LOWER": {"IN": eng_basic_list}}]
    matcher_basic_eng = Matcher(nlp.vocab)
    matcher_basic_eng.add("basic_eng", [eng_basic_pattern])
    matches_basic_eng = matcher_basic_eng(doc)

    matcher_basic_ph = Matcher(nlp.vocab)
    p1 = [{"LOWER": {"REGEX": "poziomie"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "komunikatywnym"}}]   
    p2 = [{"LOWER": {"REGEX": "a1"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "a2"}}]
    p3 = [{"LOWER": {"REGEX": "a1/a2"}}]
    p4 = [{"LOWER": {"REGEX": "komunikatywny"}}]
    p5 = [{"LOWER": {"REGEX": "a1"}}]
    p5 = [{"LOWER": {"REGEX": "a2"}}]

    # zja = [{"LOWER": {"REGEX": "znajomość"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "języka"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "angielskiego"}}]    

    matcher_basic_ph.add("ph", [p1, p2, p3, p4])
    matches_basic_ph = matcher_basic_ph(doc)

    for eng_position in knows_eng_positions:
        if len(matches_basic_eng) > 0:
            if knows_eng is True:
                for match_id, start, end in matches_basic_eng:
                    string_id = nlp.vocab.strings[match_id]
                    span = doc[start:end]
                    print(match_id, string_id, start, end, span.text)
                    if start <= eng_position + range and start >= eng_position - range:
                        level_list.append([start, "basic"])

    for eng_position in knows_eng_positions:
        if len(matches_basic_ph) > 0:
            for match_id, start, end in matches_basic_ph:
                string_id = nlp.vocab.strings[match_id]
                span = doc[start:end]
                print(match_id, string_id, start, end, span.text)
                if start <= eng_position + range and start >= eng_position - range:
                    level_list.append([start, "basic"])

    # sprawdzenie znajomosci sredniej

    eng_int_list = list(eng_dict['int'])
    eng_int_pattern = [{"LOWER": {"IN": eng_int_list}}]
    matcher_int_eng = Matcher(nlp.vocab)
    matcher_int_eng.add("int_eng", [eng_int_pattern])
    matches_int_eng = matcher_int_eng(doc)

    matcher_int_ph = Matcher(nlp.vocab)
    sz = [{"LOWER": {"REGEX": "średnio"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "zaawansowany"}}]    
    bd3 = [{"LOWER": {"REGEX": "b1"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "b2"}}]
    bd4 = [{"LOWER": {"REGEX": "b1/b2"}}]
    bd5 = [{"LOWER": {"REGEX": "a2"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "b1"}}]
    bd6 = [{"LOWER": {"REGEX": "a2/b1"}}]
    bd7 = [{"LOWER": {"REGEX": "b1"}}]
    bd8 = [{"LOWER": {"REGEX": "b2"}}]

    matcher_int_ph.add("ph", [sz, bd3, bd4, bd5, bd6, bd7, bd8])
    matches_int_ph = matcher_int_ph(doc)

    for eng_position in knows_eng_positions:
        if len(matches_int_eng) > 0:
            if knows_eng is True:
                for match_id, start, end in matches_int_eng:
                    string_id = nlp.vocab.strings[match_id]
                    span = doc[start:end]
                    print(match_id, string_id, start, end, span.text)
                    if start <= eng_position + range and start >= eng_position - range:
                        level_list.append([start, "int"])
                        # knows_eng_int=True

    for eng_position in knows_eng_positions:
        if len(matches_int_ph) > 0:
            for match_id, start, end in matches_int_ph:
                string_id = nlp.vocab.strings[match_id]
                span = doc[start:end]
                print(match_id, string_id, start, end, span.text)
                if start <= eng_position + range and start >= eng_position - range:
                    level_list.append([start, "int"])


    # sprawdzenie znajomosci zaawansowanej

    eng_good_list = list(eng_dict['good'])
    eng_good_pattern = [{"LOWER": {"IN": eng_good_list}}]
    matcher_good_eng = Matcher(nlp.vocab)
    matcher_good_eng.add("good_eng", [eng_good_pattern])
    matches_good_eng = matcher_good_eng(doc)

    matcher_good_ph = Matcher(nlp.vocab)
    sz = [{"LOWER": {"REGEX": "biegłość"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "zawodowa"}}]    
    me = [{"LOWER": {"REGEX": "major"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "in"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "english"}}]
    ep = [{"LOWER": {"REGEX": "egzamin"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "państwowy"}}]
    bd1 = [{"LOWER": {"REGEX": "b2"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "c1"}}]
    bd2 = [{"LOWER": {"REGEX": "b2/c1"}}]
    bd3 = [{"LOWER": {"REGEX": "c1"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "c2"}}]
    bd4 = [{"LOWER": {"REGEX": "c1/c2"}}]
    bd5 = [{"LOWER": {"REGEX": "c1"}}]
    bd6 = [{"LOWER": {"REGEX": "c2"}}]
    bd7 = [{"LOWER": {"REGEX": "b"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "dobry"}}]
    bd8 = [{"LOWER": {"REGEX": "bardzo"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "dobry"}}]
    bd9 = [{"LOWER": {"REGEX": "zaawansowan"}}]


    matcher_good_ph.add("ph", [sz, me, ep, bd1, bd2, bd3, bd4, bd5, bd6, bd7, bd8, bd9])
    matches_good_ph = matcher_good_ph(doc)


    for eng_position in knows_eng_positions:
        if len(matches_good_eng) > 0:
            if knows_eng is True:
                for match_id, start, end in matches_good_eng:
                    string_id = nlp.vocab.strings[match_id]
                    span = doc[start:end]
                    print(match_id, string_id, start, end, span.text)
                    if start <= eng_position  + range and start >= eng_position - range:
                        level_list.append([start, "good"])
                        # knows_eng_good=True

    for eng_position in knows_eng_positions:
        if len(matches_good_ph) > 0:
            for match_id, start, end in matches_good_ph:
                string_id = nlp.vocab.strings[match_id]
                span = doc[start:end]
                print(match_id, string_id, start, end, span.text)
                if start <= eng_position  + range and start >= eng_position - range:
                    level_list.append([start, "good"])

    if not level_list:
        if knows_eng is False:
            eng_level = "no"
        else:
            eng_level = "basic"
    else:
        sorted_level_list = sorted(level_list, key=lambda x: x[0])
        eng_level = sorted_level_list[0][1]

    if eng_level == "no":
        return([1, 0, 0, 0])
    elif eng_level == "basic":
        return([0, 1, 0, 0])
    elif eng_level == "int":
        return([0, 0, 1, 0])
    elif eng_level == "good":
        return([0, 0, 0, 1])