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
    has_experience_cc = False
    has_experience_cs = False
    has_experience_ovr = False
    has_experience_oth = False

    exp_start_end = []
    cap_start_end = []
    edu_start_end = []
    hbb_start_end = []
    ach_start_end = []
    rate = 0

    # sprawdzenie, czy osoba posiada doswiadczenie
    d1 = [{"LOWER": {"REGEX": "przebieg"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "pracy"}}]    
    d2 = [{"LOWER": {"REGEX": "kariera"}}]
    d3 = [{"LOWER": {"REGEX": "career"}}]
    d4 = [{"LOWER": {"REGEX": "historia"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "zatrudnienia"}}]    
    d5 = [{"LOWER": {"REGEX": "zatrudnienie"}}]
    d6 = [{"LOWER": {"REGEX": "doswiadczeni"}}]
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

    
    # sprawdzenie, czy osoba posiada doświadczenie w CC


    job_list = list(exp_dict['cc'])
    cc_pattern = [{"LOWER": {"IN": job_list}}]
    matcher_cc = Matcher(nlp.vocab)
    matcher_cc.add("has_cc_exp", [cc_pattern])
    matches_cc = matcher_cc(doc)

    cc = [{"LOWER": {"REGEX": "call"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "center"}}]    
    ts = [{"LOWER": {"REGEX": "telephone"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "service"}}] 
    vp = [{"LOWER": {"REGEX": "voice"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "picker"}}]
    gl = [{"LOWER": {"REGEX": "gorąca"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "linia"}}]
    to = [{"LOWER": {"REGEX": "telefoniczna"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "obsługa"}}]   
    ol = [{"LOWER": {"REGEX": "obsługa"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "linii"}}]    
    dr = [{"LOWER": {"REGEX": "dział"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "reklamacji"}}]    
    kt = [{"LOWER": {"REGEX": "konsultant"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "telefoniczny"}}]  
    dz = [{"LOWER": {"REGEX": "dział"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "zamówień"}}]    
    # r  = [{"LOWER": {"REGEX": "rozmow"}}]
    ca = [{"LOWER": {"REGEX": "call"}}]
    tele = [{"LOWER": {"REGEX": "telefoni"}}]
    
    matcher_cc_ph = Matcher(nlp.vocab)
    matcher_cc_ph.add("ph", [cc, ts, vp, gl, to, ol, dr, kt, dz, ca, tele])
    matches_cc_ph = matcher_cc_ph(doc)

    if len(matches_cc) > 0:
        for match_id, start, end in matches_cc:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            has_experience_cc = True

    if len(matches_cc_ph) > 0:
        for match_id, start, end in matches_cc_ph:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            has_experience_cc = True

    # sprawdzenie czy ma doświadczenie w cs


    job_list = list(exp_dict['cs'])
    cs_pattern = [{"LOWER": {"IN": job_list}}]
    matcher_cs = Matcher(nlp.vocab)
    matcher_cs.add("has_cs_exp", [cs_pattern])
    matches_cs = matcher_cs(doc)

    cc = [{"LOWER": {"REGEX": "customer"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "care"}}]    
    cs = [{"LOWER": {"REGEX": "customer"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "service"}}] 
    sp = [{"LOWER": {"REGEX": "sales"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "person"}}]
    ok = [{"LOWER": {"REGEX": "obsługa"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "klient"}}]
    # dk = [{"LOWER": {"REGEX": "doradztwo"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "klient"}}]   
    pk = [{"LOWER": {"REGEX": "przy"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "kasie"}}]    
    pok = [{"LOWER": {"REGEX": "punkt"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "obsługi"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "klienta"}}] 
    kk = [{"LOWER": {"REGEX": "kontakt"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "klientem"}}]    
    ph = [{"LOWER": {"REGEX": "przedstawiciel"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "handlowy"}}]    

    matcher_cs_ph = Matcher(nlp.vocab)
    matcher_cs_ph.add("ph", [cc, cs, sp, ok, pk, pok, ph, kk])
    matches_cs_ph = matcher_cs_ph(doc)

    if len(matches_cs) > 0:
        for match_id, start, end in matches_cs:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            has_experience_cs = True

    if len(matches_cs_ph) > 0:
        for match_id, start, end in matches_cs_ph:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            has_experience_cs = True


    # sprawdzenie czy ma doświadczenie w ovr


    job_list = list(exp_dict['ovr'])
    ovr_pattern = [{"LOWER": {"IN": job_list}}]
    matcher_ovr = Matcher(nlp.vocab)
    matcher_ovr.add("has_ovr_exp", [ovr_pattern])
    matches_ovr = matcher_ovr(doc)

    if len(matches_ovr) > 0:
        for match_id, start, end in matches_ovr:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            has_experience_ovr = True

    # sprawdzenie czy ma doświadczenie w oth

    job_list = list(exp_dict['oth'])
    oth_pattern = [{"LOWER": {"IN": job_list}}]
    matcher_oth = Matcher(nlp.vocab)
    matcher_oth.add("has_oth_exp", [oth_pattern])
    matches_oth = matcher_oth(doc,)

    if len(matches_oth) > 0:
        for match_id, start, end in matches_oth:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            has_experience_oth = True

    if has_experience is True or has_experience_cc is True or has_experience_cs is True or has_experience_oth is True or has_experience_ovr is True:
        if has_experience_cc is True:
            return([1, 0, 0, 0, 0])
        elif has_experience_cs is True:
            return([0, 0, 1, 0, 0])
        elif has_experience_ovr is not True:
            return([0, 0, 0, 1, 0])
        else:
            return([0, 0, 0, 0, 1]) 
    else:
        return([0, 1, 0, 0, 0])

