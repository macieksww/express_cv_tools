import spacy
from spacy.matcher import Matcher

nlp = spacy.load("pl_core_news_lg")

def extract_truck(text, filename):
    doc = nlp(text)

    # tworzenie patternow do znalezienia książeczki sanepidu

    tr_1 = [{"LOWER": "bus"}]    
    tr_2 = [{"LOWER": "busy"}]    
    tr_3 = [{"LOWER": "busów"}]    
    tr_4 = [{"LOWER": "van"}] 
    tr_5 = [{"LOWER": "vany"}]
    tr_6 = [{"LOWER": "vanów"}]   
    tr_7 = [{"LOWER": {"REGEX": "3"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "5"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "t"}}]    
    tr_8 = [{"LOWER": {"REGEX": "renault"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "traffic"}}]    
    tr_9 = [{"LOWER": {"REGEX": "fiat"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "ducato"}}]  
    tr_10 = [{"LOWER": {"REGEX": "ford"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "transit"}}]  
    tr_11 = [{"LOWER": {"REGEX": "dostawcz"}}]
    tr_12 = [{"LOWER": "busem"}]  
    tr_13 = [{"LOWER": "vanem"}]  
    tr_14 = [{"LOWER": {"REGEX": "prowadz"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "bus"}}]  
    tr_15 = [{"LOWER": {"REGEX": "kierowa"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "bus"}}]  
    tr_16 = [{"LOWER": {"REGEX": "prowadz"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "van"}}]  
    tr_17 = [{"LOWER": {"REGEX": "kierowa"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "van"}}]  

    matcher = Matcher(nlp.vocab)
    matcher.add("sam. dost.", [tr_1, tr_2, tr_3, tr_4, tr_5, tr_6, tr_7, tr_8, tr_9, tr_10, tr_11,\
        tr_12, tr_13, tr_14, tr_15, tr_16, tr_17])
    matches = matcher(doc)

    if len(matches) > 0:
        return([1, 0])
    else:
        return([0, 1])
