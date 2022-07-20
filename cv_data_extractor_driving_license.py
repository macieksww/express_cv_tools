
import spacy
from spacy import displacy
from spacy.matcher import Matcher
import os

nlp = spacy.load("pl_core_news_lg")

def process_directory(path):
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            #print(filename)
            with open( path + "/" + filename, "r") as file:
                text = file.read()
                extract_driving_license(text, filename)


def extract_driving_license(text, filename):
    matcher = Matcher(nlp.vocab)
    doc = nlp(text)
    has_license = False
    has_license_car = False
    has_license_other = False
    is_driver = False
    is_truck_driver = False
    range_from_match_positions = 5
    car_license = 'B'
    other_licenses = [ 'C', 'D', 'E', 'F', 'T']
    driving_lic_pattern1 = [{"LOWER": {"REGEX":"prawo"}},{"OP": "?"},{"OP": "?"},{"LOWER": {"REGEX":"jazdy"}}]
    driving_lic_pattern2 = [{"LOWER": {"REGEX":"prawo"}},{"OP": "?"},{"LOWER": {"NOT_IN":["cokolwiek"]}},{"OP": "?"},{"LOWER": {"REGEX":"jazdy"}}]
    driving_lic_pattern3 = [{"LOWER": {"REGEX":"jazdy"}},{"OP": "?"},{"LOWER": {"REGEX":"kat"}}]
    driving_lic_pattern4 = [{"LOWER": {"REGEX":"driving"}},{"OP": "?"},{"OP": "?"},{"LOWER": {"REGEX":"license"}}]

    matcher.add("driving_license", [driving_lic_pattern1, driving_lic_pattern2, driving_lic_pattern3, driving_lic_pattern4])
    matches = matcher(doc)
    match_positions = []
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end]
        #print(match_id, string_id, start, end, span.text)
        match_positions.append([start, end])
        has_license = True
    matcher2 = Matcher(nlp.vocab)
    #driving_lic_cat_pattern = [{"IS_UPPER": True}]
    driving_lic_cat_pattern = [{"TEXT": {"REGEX":"^[AMBCDEFT12\+]*$"}}]
    matcher2.add("driving_license_cat", [driving_lic_cat_pattern])
    matches2 = matcher2(doc)
    max_distance_after = 5
    max_distance_before = 0
    for match_id, start, end in matches2:
        is_driving_lic_cat = False
        for range in match_positions:
            if (start < range[1] + max_distance_after and start > range[0] - max_distance_before):
                is_driving_lic_cat = True
        if is_driving_lic_cat:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            # print(match_id, string_id, start, end, span.text)
            if car_license in span.text:
                has_license_car = True
            for lic_type in other_licenses:
                if lic_type in span.text:
                    has_license_other = True
                    #print(lic_type)


    #driver_pattern = [{"LOWER":"kierowca"}]
    # driver_pattern = [{"LOWER": {"IN": ["kierowca", "kierowcą", "kierowcy", "kurier", "kuriera", "kurierem", "taksówkarz", "tasówkarzem", "taksówkarza",
    # "dostawca", "dostawcy", "dostawcą"]}}]
    driver_1 = [{"LOWER": {"REGEX":"kierowc"}}]
    driver_2 = [{"LOWER": {"REGEX":"kurier"}}]
    driver_3 = [{"LOWER": {"REGEX":"taksówka"}}]
    driver_4 = [{"LOWER": {"REGEX":"dostawc"}}]
    driver_5 = [{"LOWER": {"REGEX":"rozwożenie"}}]
    driver_6 = [{"LOWER": {"REGEX":"rozwozi"}}]
    driver_7 = [{"LOWER": {"REGEX":"dostarczanie"}} ,{"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX":"paczek"}}]
    driver_8 = [{"LOWER": {"REGEX":"przewóz"}}]
    driver_9 = [{"LOWER": {"REGEX":"dowóz"}}]
    driver_10 = [{"LOWER": {"REGEX":"driving"}}]
    driver_11 = [{"LOWER": {"REGEX":"freenow"}}]
    driver_12 = [{"LOWER": {"REGEX":"uber"}}]
    driver_13 = [{"LOWER": {"REGEX":"taxi"}}]
    driver_14 = [{"LOWER": {"REGEX":"bolt"}}]
    driver_15 = [{"LOWER": {"REGEX":"driver"}}]
    driver_16 = [{"LOWER": {"REGEX":"deliverer"}}]
    driver_17 = [{"LOWER": {"REGEX":"prowadzenie"}} ,{"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX":"bus"}}]
    driver_18 = [{"LOWER": {"REGEX":"prowadzenie"}} ,{"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX":"van"}}]
    driver_19 = [{"LOWER": {"REGEX":"prowadzenie"}} ,{"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX":"samochod"}}]
    driver_20 = [{"LOWER": {"REGEX":"prowadzenie"}} ,{"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX":"autem"}}]
    driver_21 = [{"LOWER": {"REGEX":"kierowanie"}} ,{"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX":"bus"}}]
    driver_22 = [{"LOWER": {"REGEX":"kierowanie"}} ,{"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX":"van"}}]
    driver_23 = [{"LOWER": {"REGEX":"kierowanie"}} ,{"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX":"samochod"}}]
    driver_24 = [{"LOWER": {"REGEX":"kierowanie"}} ,{"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX":"autem"}}]

    matcher_driver = Matcher(nlp.vocab)
    matcher_driver.add("is_driver", [driver_1, driver_2, driver_3, driver_4, driver_5, driver_6, driver_7, driver_8,\
        driver_9, driver_10, driver_11, driver_12, driver_13, driver_14, driver_15, driver_16, driver_17, driver_18, driver_19,
        driver_20, driver_21, driver_22, driver_23, driver_24])
    matches_driver = matcher_driver(doc)
    match_driver_positions = []
    for match_id, start, end in matches_driver:
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end]
        #print(match_id, string_id, start, end, span.text)
        match_driver_positions.append([start, end])
        is_driver = True
        #print(span.text)


    # how many years pattern

    hmy_1 = [{"LOWER": {"REGEX": "od"}}, {"OP": "?"}, {"OP": "?"}, {'TEXT':{'REGEX':r'\d{2}(?:\d{2})?'}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "roku"}}]
    hmy_2 = [{'TEXT':{'REGEX':r'd{1}(?:d{1})?'}}, {"OP": "?"},  {"OP": "?"}, {"LOWER": {"REGEX": "lat"}}]  

    matcher_hmy = Matcher(nlp.vocab)
    matcher_hmy.add("ile lat", [hmy_1, hmy_2])
    matches_hmy = matcher_hmy(doc)

    if len(matches_hmy) > 0:
        for match_id, start, end in matches_hmy:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            
            if len(match_positions) > 0:
                for match_position in match_positions:
                    if (abs(start-match_position[1])<range_from_match_positions or abs(end-match_position[0])<range_from_match_positions):
                        pass
                        # print('\n\n\n')
                        # print(match_id, string_id, start, end, span.text)
                        # print('\n\n\\n')

    # truck pattern

    truck_driver_pattern = [{"LEMMA":{"IN":["autobus", "autokar", "ciężar", "TIR", "tir", "traktor", "ciągnik"]}}]
    matcher_truck_driver = Matcher(nlp.vocab)
    matcher_truck_driver.add("is_truck_driver", [truck_driver_pattern])
    matches_truck_driver = matcher_truck_driver(doc)
    max_distance_after = 8
    max_distance_before = 6
    for match_id, start, end in matches_truck_driver:
        is_driver_job = False
        for range in match_positions:
            if (start < range[1] + max_distance_after and start > range[0] - max_distance_before):
                is_driver_job = True
        if is_driver_job:
            is_truck_driver = True
    
    if has_license and ( (not has_license_car) and (not has_license_other)):
        has_license_car = True

    if not has_license and is_driver:
        has_license = True
        has_license_car = True

    if is_truck_driver:
        has_license = True
        has_license_car = True
        has_license_other = True

    # print(filename, int(has_license), int(has_license_car), int((not has_license_other) and has_license_car), int(is_driver), int(is_truck_driver))

    output = { "has_license" : has_license, "has_license_car":has_license_car, "has_license_only_car":(not has_license_other) and has_license_car, "is_driver":is_driver, "is_truck_driver":is_truck_driver}
    return output

#print("Zaakceptowane:")
#process_directory("dane/z")
#print("Odrzucone:")
#process_directory("dane/o")
