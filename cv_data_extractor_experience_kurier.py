import spacy
from spacy.matcher import Matcher
from csv_reader import read_csv

nlp = spacy.load("pl_core_news_lg")

def extract_experience(text, filename):
    cv_exp_dict = read_csv()
    exp_dict = cv_exp_dict[0]
    cv_dict = cv_exp_dict[1]

    matcher = Matcher(nlp.vocab)
    doc = nlp(text)
    has_experience = False
    has_experience_kurier = False
    has_experience_phy = False
    has_experience_oth = False

    # sprawdzenie, czy osoba posiada doswiadczenie
    d1 = [{"LOWER": {"REGEX": "przebieg"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "pracy"}}]    
    d2 = [{"LOWER": {"REGEX": "kariera"}}]
    d3 = [{"LOWER": {"REGEX": "career"}}]
    d4 = [{"LOWER": {"REGEX": "historia"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "zatrudnienia"}}]    
    d5 = [{"LOWER": {"REGEX": "zatrudnieni"}}]
    d6 = [{"LOWER": {"REGEX": "doświadczeni"}}]
    d7 = [{"LOWER": {"REGEX": "experience"}}]


    exp_list = list(cv_dict['exp'])
    exp_part_pattern = [{"LOWER": {"IN": exp_list}}]
    matcher_exp_part = Matcher(nlp.vocab)
    matcher_exp_part.add("has_exp", [exp_part_pattern])
    matches_exp = matcher_exp_part(doc)

    matcher_exp_ph = Matcher(nlp.vocab)
    matcher_exp_ph.add("has_exp", [d1, d2, d3, d4, d5, d6, d7])
    matches_exp_ph = matcher_exp_ph(doc)

    if len(matches_exp) > 0 or len(matches_exp_ph) > 0:
        has_experience = True

    
    # sprawdzenie, czy osoba posiada doświadczenie w pracy na magazynie


    k_1 = [{"LOWER": {"REGEX": "kierowca"}}]    
    k_2 = [{"LOWER": {"REGEX": "kurier"}}] 
    k_3 = [{"LOWER": {"REGEX": "rozwożenie"}}]
    k_4 = [{"LOWER": {"REGEX": "dostawca"}}]
    k_5 = [{"LOWER": {"REGEX": "dostarczanie"}}]   
    k_6 = [{"LOWER": {"REGEX": "pakowacz"}}]    
    k_7 = [{"LOWER": {"REGEX": "przewóz"}}]    
    k_8 = [{"LOWER": {"REGEX": "taksówka"}}]  
    k_9 = [{"LOWER": {"REGEX": "taxi"}}]  
    k_10 = [{"LOWER": {"REGEX": "freenow"}}]  
    k_11 = [{"LOWER": {"REGEX": "uber"}}]  
    k_12 = [{"LOWER": {"REGEX": "bolt"}}]  
    k_13 = [{"LOWER": {"REGEX": "driver"}}]  
    k_14 = [{"LOWER": {"REGEX": "deliverer"}}]  
    k_15 = [{"LOWER": {"REGEX": "kierowanie"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "autem"}}]  
    k_16 = [{"LOWER": {"REGEX": "kierowanie"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "busem"}}]  
    k_17 = [{"LOWER": {"REGEX": "kierowanie"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "pojazd"}}]  
    k_18 = [{"LOWER": {"REGEX": "kierowanie"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "samochod"}}]  
    
    matcher = Matcher(nlp.vocab)
    matcher.add("kurier/kierowca", [k_1, k_2, k_3, k_4, k_5, k_6, k_7, k_8, k_9, k_10,\
        k_11, k_12, k_13, k_14, k_15, k_16, k_17, k_18])
    matches = matcher(doc)

    if len(matches) > 0:
        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            has_experience_kurier = True


    # sprawdzenie czy ma doświadczenie w pracy innej fizycznej

    phy_ph_1 = [{"LOWER": {"REGEX": "zieleń"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "miejska"}}]    
    phy_ph_2 = [{"LOWER": {"REGEX": "operator"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "dźwigu"}}] 
    phy_ph_3 = [{"LOWER": {"REGEX": "operator"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "koparki"}}]
    phy_ph_4 = [{"LOWER": {"REGEX": "operator"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "maszyn"}}]
    phy_ph_5 = [{"LOWER": {"REGEX": "wózek"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "widłowy"}}]
    phy_ph_6 = [{"LOWER": {"REGEX": "wózka"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "widłowego"}}]    
    phy_ph_9 = [{"LOWER": {"REGEX": "budowie"}}]    
    phy_ph_10 = [{"LOWER": {"REGEX": "murarz"}}]    
    phy_ph_11 = [{"LOWER": {"REGEX": "tynkarz"}}]    
    phy_ph_12 = [{"LOWER": {"REGEX": "malarz"}}]    
    phy_ph_13 = [{"LOWER": {"REGEX": "remont"}}]    
    phy_ph_14 = [{"LOWER": {"REGEX": "przprowadzkowa"}}]    
    phy_ph_15 = [{"LOWER": {"REGEX": "przeprowadzki"}}]    
    phy_ph_16 = [{"LOWER": {"REGEX": "praca"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "fizyczna"}}]
    phy_ph_17 = [{"LOWER": {"REGEX": "pracownik"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "fizyczny"}}]    
    phy_ph_18 = [{"LOWER": {"REGEX": "wykoczeni"}}]    
    phy_ph_19 = [{"LOWER": {"REGEX": "monter"}}]    
    phy_ph_20 = [{"LOWER": {"REGEX": "montaż"}}]    
    phy_ph_21 = [{"LOWER": {"REGEX": "brukarz"}}]    
    phy_ph_22 = [{"LOWER": {"REGEX": "budowlan"}}]    
    phy_ph_23 = [{"LOWER": {"REGEX": "ślusarz"}}]    
    phy_ph_24 = [{"LOWER": {"REGEX": "spawacz"}}]    
    phy_ph_25 = [{"LOWER": {"REGEX": "remont"}}] 
    phy_ph_26 = [{"LOWER": {"REGEX": "gipsiarz"}}]    
    phy_ph_27 = [{"LOWER": {"REGEX": "szpachlarz"}}]    
    phy_ph_28 = [{"LOWER": {"REGEX": "konserwator"}}]    
    phy_ph_29 = [{"LOWER": {"REGEX": "kurier"}}]    
    phy_ph_30 = [{"LOWER": {"REGEX": "serwisant"}}]   
    phy_ph_31 = [{"LOWER": {"REGEX": "sprząta"}}]    
    phy_ph_32 = [{"LOWER": {"REGEX": "przerobowy"}}]    
    phy_ph_33 = [{"LOWER": {"REGEX": "zbi"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "owoców"}}]  
    phy_ph_34 = [{"LOWER": {"REGEX": "zbi"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "warzyw"}}]
    phy_ph_35 = [{"LOWER": "budowa"}] 
    phy_ph_36 = [{"LOWER": {"REGEX": "warehouse"}}]    
    phy_ph_37 = [{"LOWER": {"REGEX": "magazyn"}}] 
    phy_ph_38 = [{"LOWER": {"REGEX": "pakowanie"}}]
    phy_ph_39 = [{"LOWER": {"REGEX": "sortowa"}}]
    phy_ph_40 = [{"LOWER": {"REGEX": "sorter"}}]   
    phy_ph_41 = [{"LOWER": {"REGEX": "pakowacz"}}]    
    phy_ph_42 = [{"LOWER": {"REGEX": "sortownik"}}]    
    phy_ph_43 = [{"LOWER": {"REGEX": "hurtowni"}}]  


    matcher = Matcher(nlp.vocab)
    matcher.add("inna fizyczna", [phy_ph_1, phy_ph_2, phy_ph_3, phy_ph_4, phy_ph_5, phy_ph_6,\
    phy_ph_9, phy_ph_10, phy_ph_11, phy_ph_12, phy_ph_13, phy_ph_14, phy_ph_15,\
    phy_ph_16, phy_ph_17, phy_ph_18, phy_ph_19, phy_ph_20, phy_ph_21, phy_ph_22, phy_ph_23, phy_ph_24,\
    phy_ph_25, phy_ph_26, phy_ph_27, phy_ph_28, phy_ph_29, phy_ph_30, phy_ph_31, phy_ph_32, phy_ph_33,\
    phy_ph_34, phy_ph_35, phy_ph_36, phy_ph_37, phy_ph_38, phy_ph_39, phy_ph_40, phy_ph_41,\
    phy_ph_42, phy_ph_43])
    matches = matcher(doc)

    if len(matches) > 0:
        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            has_experience_phy = True


    # # sprawdzenie czy ma doświadczenie w oth

    # job_list = list(exp_dict['oth'])
    # oth_pattern = [{"LOWER": {"IN": job_list}}]
    # matcher_oth = Matcher(nlp.vocab)
    # matcher_oth.add("has_oth_exp", [oth_pattern])
    # matches_oth = matcher_oth(doc,)

    # if len(matches_oth) > 0:
    #     for match_id, start, end in matches_oth:
    #         string_id = nlp.vocab.strings[match_id]
    #         span = doc[start:end]
    #         print(match_id, string_id, start, end, span.text)
    #         has_experience_oth = True

    if has_experience is True or has_experience_kurier is True or has_experience_phy is True:
        if has_experience_kurier is True:
            return([1, 0, 0, 0])
        elif has_experience_phy is True:
            return([0, 1, 0, 0])
        else:
            return([0, 0, 1, 0]) 
    else:
        return([0, 0, 0, 1])

