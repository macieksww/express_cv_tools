import spacy
from spacy.matcher import Matcher
from csv_reader import read_csv

nlp = spacy.load("pl_core_news_lg")

def extract_motor(text, filename):
    office_dict = read_csv()
    office_dict = office_dict[3]

    matcher = Matcher(nlp.vocab)
    doc = nlp(text)
    into_moto = False

    # tworzenie patternow do znalezienia poziomu angielskiegu
    # sprawdzenie znajomosci (czy slowo office pojawia sie w CV)

    m1 = [{"LOWER": {"REGEX": "motoryzacja"}}]    
    m2 = [{"LOWER": {"REGEX": "samochody"}}]    
    m3 = [{"LOWER": {"REGEX": "rajdy"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "samochodowe"}}]    
    m4 = [{"LOWER": {"REGEX": "rajdy"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "motorowe"}}]    
    m5 = [{"LOWER": {"REGEX": "rajdy"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "motocyklowe"}}]    
    m6 = [{"LOWER": {"REGEX": "jazda"}}, {"OP": "?"}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "motor"}}]    
    m7 = [{"LOWER": {"REGEX": "gokart"}}]    
    m8 = [{"LOWER": {"REGEX": "branża"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "motor"}}]    
    m9 = [{"LOWER": {"REGEX": "wrc"}}]    
    m10 = [{"LOWER": {"REGEX": "f1"}}]
    m11 = [{"LOWER": {"REGEX": "formula"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "1"}}]    
    m12 = [{"LOWER": {"REGEX": "rajd"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "dakar"}}]    
    m13 = [{"LOWER": {"REGEX": "wyścigi"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "samochodowe"}}]    
    m14 = [{"LOWER": {"REGEX": "wyścigi"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "moto"}}]    
    m15 = [{"LOWER": {"REGEX": "warsztat"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "samochod"}}]    
    m16 = [{"LOWER": {"REGEX": "mechanik"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "samochod"}}]    
    m17 = [{"LOWER": {"REGEX": "myjnia"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "samochod"}}]    


    matcher_motor = Matcher(nlp.vocab)
    matcher_motor.add("motor", [m1, m2, m3, m4, m5, m6, m7,m8, m9, m10, m11, m12, m13, m14])
    matches_motor = matcher_motor(doc)

    if len(matches_motor) > 0:
        into_moto = True
