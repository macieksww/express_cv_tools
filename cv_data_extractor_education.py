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
    has_unfn_edu = False
    edu_list = []
    master_studies = False
    high_edu_pos = []
    dates = []
    close_dates = {}
    closest_dates = {}
    close_still_phrases = {}
    still_acceptance_rate = 15
    range = 20

    # szukanie daty w okolicy informacji o wyższym wykształceniu
    # wykorzystane w celu sprawdzenia, czy osoba która aktualnie studiuje ukończyła już jakiś kierunek
    # szukanie dat w uniwersalnych formatach liczbowych

    dp1 = [{'TEXT':{'REGEX':r'\d{1,2}/\d{1,2}/\d{2}(?:\d{2})?'}}]
    dp2 = [{'TEXT':{'REGEX':r'\d{1,2}/\d{2}(?:\d{2})?'}}]
    dp3 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{1,2}'}}]
    dp4 = [{'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{1,2}'}}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{2}(?:\d{2})?'}}]
    dp5 = [{'IS_DIGIT': True}, {'ORTH': '-'}, {'IS_DIGIT': True}, {'ORTH': '-'}, {'IS_DIGIT': True}]
    dp6 = [{'IS_DIGIT': True}, {'ORTH': '-'}, {'IS_DIGIT': True}]

    matcher_whole_date = Matcher(nlp.vocab)
    matcher_whole_date.add("data_pattern", [dp1, dp2, dp3, dp4, dp5, dp6])
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
            edu_list.append([1, "basic"])

    # wykształcenie średnie

    edu_mid_list = list(edu_dict['mid'])
    edu_mid_pattern = [{"LOWER": {"IN": edu_mid_list}}]
    matcher_mid_edu = Matcher(nlp.vocab)
    matcher_mid_edu.add("mid_edu", [edu_mid_pattern])
    matches_mid_edu = matcher_mid_edu(doc)
    matcher_mid_ph = Matcher(nlp.vocab)

    ss = [{"LOWER": {"REGEX":"szkoła"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"średnia"}}]
    sz = [{"LOWER": "szkół"}, {"OP": "?"},  {"OP": "?"}, {"LOWER": "zawodowych"}]
    mat = [{"LOWER": "egzamin"}, {"OP": "?"},  {"OP": "?"}, {"LOWER": "maturalny"}]
    lo = [{"LOWER": {"REGEX":"liceum"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"ogólnokształcące"}}]
    lo2 = [{"LOWER": "lo"}]

    matcher_mid_ph.add("ph", [ss, sz, mat, lo, lo2])
    matches_mid_ph = matcher_mid_ph(doc)

    if len(matches_mid_edu) > 0:
        for match_id, start, end in matches_mid_edu:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            # if start <= knows_office_position + range and start >= knows_office_position-range:
            edu_list.append([2, "mid"])
    
    if len(matches_mid_ph) > 0:
        for match_id, start, end in matches_mid_ph:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            edu_list.append([2, "mid"])


    # wykształcenie wyższe

    edu_high_list = list(edu_dict['high'])
    edu_high_pattern = [{"LOWER": {"IN": edu_high_list}}]
    matcher_high_edu = Matcher(nlp.vocab)
    matcher_high_edu.add("high_edu", [edu_high_pattern])
    terms = ["Wyższa Szkoła", "Wyższa szkoła", "wyższa szkoła", "Państwowa Wyższa Szkoła Zawodowa"]
    patterns = [nlp.make_doc(text) for text in terms]
    matcher_high_ph = PhraseMatcher(nlp.vocab)
    matcher_high_ph.add("TerminologyList", patterns)
    matches_high_edu = matcher_high_edu(doc)

    sw = [{"LOWER": {"REGEX":"wyższa"}}, {"OP": "?"},  {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX":"szkoła"}}]
    # pwsz = [{"LOWER": "państwowa"}, {"OP": "?"},  {"OP": "?"}, {"LOWER": "wyższa"}, {"OP": "?"},  {"OP": "?"}, {"LOWER": "szkoła"}, {"OP": "?"},  {"OP": "?"}, {"LOWER": "zawodowa"}]
    ww = [{"LOWER": "wyształcenie"}, {"OP": "?"},  {"OP": "?"}, {"LOWER": "wyższe"}]
    u = [{"LOWER": {"REGEX":"uniwersyte"}}]
    p = [{"LOWER": {"REGEX":"politechnika"}}]
    l = [{"LOWER": {"REGEX":"licencj"}}]
    m = [{"LOWER": {"REGEX":"magister"}}]
    awf = [{"LOWER": {"REGEX":"akademia"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"wychowania"}}]
    asp = [{"LOWER": {"REGEX":"akademia"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX":"wychowania"}}]
    m2 = [{"LOWER": {"REGEX":"master"}}]
    b = [{"LOWER": {"REGEX":"bachelor"}}]
    bsc = [{"LOWER": "bsc"}]
    msc = [{"LOWER": "msc"}]
    awf2 = [{"LOWER": "awf"}]
    asp2 = [{"LOWER": "asp"}]
    pdp = [{"LOWER": {"REGEX":"podyplom"}}]
    inz = [{"LOWER": {"REGEX":"inynier"}}]

    matcher = Matcher(nlp.vocab)
    matcher.add("bsc", [sw, u, p, l, b, bsc, awf, awf2, asp, asp2])
    matcher.add("msc", [ww, m, m2, msc, pdp])
    matches = matcher(doc)
    

    if len(matches_high_edu) > 0:
        for match_id, start, end in matches_high_edu:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            # print(match_id, string_id, start, end, span.text)
            edu_list.append([4, "high"])
            high_edu_pos.append([start, end, span.text])
            has_high_edu = True

    if len(matches) > 0:
        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            # print(match_id, string_id, start, end, span.text)
            edu_list.append([4, "high"])
            high_edu_pos.append([start, end, span.text])
            has_high_edu = True
            if string_id == "msc":
                master_studies = True

    print('high edu positions')
    print(high_edu_pos)

    # wykształcenie w trakcie

    edu_still_list = list(edu_dict['still'])
    edu_still_pattern = [{"LOWER": {"IN": edu_still_list}}]
    matcher_still_edu = Matcher(nlp.vocab)
    matcher_still_edu.add("still_edu", [edu_still_pattern])
    matches_still_edu = matcher_still_edu(doc)
    matcher_still_ph = Matcher(nlp.vocab)
    # terms = ["1 rok", "2 rok", "pierwszy rok", "drugi rok"]
    # patterns = [nlp.make_doc(text) for text in terms]

    y_1 = [{"LOWER": "1"}, {"OP": "?"}, {"LOWER": {"REGEX": "rok"}}]
    y_2 = [{"LOWER": "2"}, {"OP": "?"}, {"LOWER": {"REGEX": "rok"}}]   
    r =  [{"LOWER": "rok"}]
    y_p = [{"LOWER": {"REGEX": "pierwszy"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "rok"}}]    
    y_s = [{"LOWER": {"REGEX": "drugi"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "rok"}}]
    n = [{"LOWER": {"REGEX": "nadal"}}]
    t = [{"LOWER": {"REGEX": "teraz"}}]
    o = [{"LOWER": {"REGEX": "obecnie"}}]
    wt = [{"LOWER": {"REGEX": "w"}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "trakcie"}}]

    matcher_still_ph.add("ph", [y_p, y_s, y_1, y_2, n, t , wt, r, o])
    matches_still_ph = matcher_still_ph(doc)

    if has_high_edu is True:
        if master_studies is False:
            # przeszukanie odległości od znalezionych dat, do miejsca, w którym
            # wystąpiła informacja o wyższym wykształceniu
            for edu_pos in high_edu_pos:
                close_dates[edu_pos[2]] = []
                for date in dates:
                    temp_close_dates = []
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
            
            inc=1
            print('\n\n')
            print('high edu pos')
            print(high_edu_pos)
            print('\n\n')
            print(closest_dates.keys())
            print('\n\n')
            for high_edu_position in high_edu_pos:
                if len(matches_still_edu) > 0:
                    for match_id, start, end in matches_still_edu:
                        string_id = nlp.vocab.strings[match_id]
                        span = doc[start:end]
                        # print(match_id, string_id, start, end, span.text)
                        # if str(span.text) in closest_dates.keys():
                        if start > high_edu_position[0]-range and start < high_edu_position[0]+range:
                            if high_edu_position[2] not in  close_still_phrases.keys():
                                close_still_phrases[high_edu_position[2]] = min(abs(high_edu_position[1]-start), abs(high_edu_position[0]-end))
                            else:
                                close_still_phrases[str(high_edu_position[2])+str(inc)] = min(abs(high_edu_position[1]-start), abs(high_edu_position[0]-end))
                                inc = inc+1

                if len(matches_still_ph) > 0:
                    for match_id, start, end in matches_still_ph:
                        string_id = nlp.vocab.strings[match_id]
                        span = doc[start:end]
                        # print(match_id, string_id, start, end, span.text)
                        if start > high_edu_position[0]-range and start < high_edu_position[0]+range:
                            # close_still_phrases[high_edu_position[2]] = min(abs(high_edu_position[1]-start), abs(high_edu_position[0]-end))
                            if high_edu_position[2] not in close_still_phrases.keys():
                                    close_still_phrases[high_edu_position[2]] = min(abs(high_edu_position[1]-start), abs(high_edu_position[0]-end))
                            else:
                                close_still_phrases[str(high_edu_position[2])+str(inc)] = min(abs(high_edu_position[1]-start), abs(high_edu_position[0]-end))
                                inc = inc+1
               
            if len(close_still_phrases) > 0:
                print("keys")
                print(close_still_phrases.keys())
                print(close_still_phrases)
            
            # dodane odległości od fraz określających nieukończone studia
            
            if len(close_still_phrases) > 0 and len(closest_dates) == 0:
                if len(close_still_phrases) == len(high_edu_pos):
                    return([0, 1, 0, 0, 0])
         
            if len(close_still_phrases) > 0 and len(closest_dates) == len(close_still_phrases):
                print(close_dates.keys())
                print(close_still_phrases.keys())
                for key_d, value_d in closest_dates.items():
                    for key_s, value_s in close_still_phrases.items():
                        if key_d == key_s:
                            if value_s-still_acceptance_rate > value_d:
                                return([1, 0, 0, 0, 0])
                return([0, 1, 0, 0, 0])

    # finding education level
    if not edu_list:
        edu_level = "no"
    else:
        edu_level = sorted(edu_list, key = lambda i: i[0], reverse = True)[0][1]

    if edu_level == "high": 
        return([1, 0, 0, 0, 0])
    elif edu_level == "still":
        return([0, 1, 0, 0, 0])
    elif edu_level == "mid":
        return([0, 0, 1, 0, 0])
    elif edu_level == "ground":
        return([0, 0, 0, 1, 0])
    else:
        return([0, 0, 0, 0, 1])
