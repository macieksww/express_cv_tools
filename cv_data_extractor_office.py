import spacy
from spacy.matcher import Matcher
from csv_reader import read_csv

nlp = spacy.load("pl_core_news_lg")

def extract_office(text, filename):
    office_dict = read_csv()
    office_dict = office_dict[3]

    matcher = Matcher(nlp.vocab)
    doc = nlp(text)
    knows_office_no= False
    knows_office_good = False
    knows_office_basic = False
    knows_office = False
    knows_office_positions = []
    knows_office_position = 0
    level_list = []

    range = 5

    # tworzenie patternow do znalezienia poziomu angielskiegu
    # sprawdzenie znajomosci (czy slowo office pojawia sie w CV)

    office_name_list = list(office_dict['name'])
    office_name_pattern = [{"LOWER": {"IN": office_name_list}}]
    matcher_office_name = Matcher(nlp.vocab)
    matcher_office_name.add("office_name", [office_name_pattern])
    matches_office_name = matcher_office_name(doc)

    po = [{"LOWER": {"REGEX": "pakiet"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "office"}}]    
    po1 = [{"LOWER": {"REGEX": "pakietu"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "office"}}]    
    po2 = [{"LOWER": {"REGEX": "microsoft"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "office"}}]    
    po3 = [{"LOWER": {"REGEX": "ms"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "office"}}]    
    po4 = [{"LOWER": {"REGEX": "power"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "point"}}]    
    po5 = [{"LOWER": {"REGEX": "microsoft"}}]    
    po6 = [{"LOWER": "office"}]     
    po7 = [{"LOWER": "excel"}]     
    po8 = [{"LOWER": "word"}]     
    
    matcher_ph = Matcher(nlp.vocab)
    matcher_ph.add("ph", [po, po1, po2, po3, po4, po5, po6, po7, po8])
    matches_ph = matcher_ph(doc)

    if len(matches_office_name) == 0:
        knows_office_no = True
    else:
        for match_id, start, end in matches_office_name:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            knows_office_positions.append(start)
        knows_office = True
        knows_office_position = min(knows_office_positions) # to do zmiany na pewno, musi byc sprawdznaie dla kazdego offica a nie tylko dla 1-ego
    
    if len(matches_ph) > 0:
        for match_id, start, end in matches_ph:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            knows_office_positions.append(start)
        knows_office = True

    if len(knows_office_positions) > 0:
        knows_office_position = min(knows_office_positions)

    # sprawdzenie znajomosci podstawowej

    # office_basic_list = list(office_dict['basic'])
    # office_basic_pattern = [{"LOWER": {"IN": office_basic_list}}]
    # matcher_basic_office = Matcher(nlp.vocab)
    # matcher_basic_office.add("basic_office", [office_basic_pattern])
    # matches_basic_office = matcher_basic_office(doc)

    pk = [{"LOWER": {"REGEX": "średnio"}}, {"OP": "?"}, {"LOWER": {"REGEX": "zaawansowan"}}] 
    pk1 = [{"LOWER": {"REGEX": "średnio-zaawansowany"}}] 
    pk2 = [{"LOWER": {"REGEX": "średniozaawansowany"}}]    
    # pk3 = [{"LOWER": {"REGEX": "średnio"}}]

    matcher_basic_ph = Matcher(nlp.vocab)
    matcher_basic_ph.add("ph", [pk, pk1, pk2])
    matches_basic_ph = matcher_basic_ph(doc)

    # if len(matches_basic_office) > 0:
    #     if knows_office is True:
    #         for match_id, start, end in matches_basic_office:
    #             string_id = nlp.vocab.strings[match_id]
    #             span = doc[start:end]
    #             print(match_id, string_id, start, end, span.text)
    #             if start <= knows_office_position + range and start >= knows_office_position-range:
    #                 level_list.append([start, "basic"])

    if len(matches_basic_ph) > 0:
        for match_id, start, end in matches_basic_ph:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            if start <= knows_office_position + range and start >= knows_office_position-range:
                knows_office_basic=True

    # sprawdzenie znajomosci zaawansowanej

    office_good_list = list(office_dict['good'])
    office_good_pattern = [{"LOWER": {"IN": office_good_list}}]
    matcher_good_office = Matcher(nlp.vocab)
    matcher_good_office.add("good_office", [office_good_pattern])
    matches_good_office = matcher_good_office(doc)
    bd = [{"LOWER": {"REGEX": "bardzo"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "dobra"}}]  
    bd1 = [{"LOWER": {"REGEX": "dobra"}}]    
    bd2 = [{"LOWER": {"REGEX": "advanced"}}]    
    bd3 = [{"LOWER": {"REGEX": "zaawansowan"}}]  
    bd4 = [{"LOWER": {"REGEX": "doświadczon"}}]    
    
    matcher_good_ph = Matcher(nlp.vocab)
    matcher_good_ph.add("ph", [bd, bd1, bd2, bd3, bd4])
    matches_good_ph = matcher_good_ph(doc)

    if len(matches_good_office) > 0:
        if knows_office is True:
            for match_id, start, end in matches_good_office:
                string_id = nlp.vocab.strings[match_id]
                span = doc[start:end]
                print(match_id, string_id, start, end, span.text)
                if start <= knows_office_position + range and start >= knows_office_position-range:
                    print('\n\n')
                    print("Start")
                    print(start)
                    print("KOP")
                    print(knows_office_position)
                    print('\n\n')
                    knows_office_good=True
                    # level_list.append([start, "good"])
                    
    if len(matches_good_ph) > 0:
        if knows_office is True:
            for match_id, start, end in matches_good_ph:
                string_id = nlp.vocab.strings[match_id]
                span = doc[start:end]
                print(match_id, string_id, start, end, span.text)
                print('\n\n')
                print("Start")
                print(start)
                print("KOP")
                print(knows_office_position)
                print('\n\n')
                if start <= knows_office_position + range and start >= knows_office_position-range:
                    knows_office_good=True
                    # level_list.append([start, "good"])


    # if not level_list:
    #     if knows_office is False:
    #         office_level = "no"
    #     else:
    #         office_level = "basic"
    # else:
    #     sorted_level_list = sorted(level_list, key=lambda x: x[0])
    #     office_level = sorted_level_list[0][1]

    if knows_office is False:
        return ([1, 0, 0])
    else:
        if knows_office_good is True and knows_office_basic is False:
            return([0, 0, 1])
        else:
            return([0, 1 ,0])
