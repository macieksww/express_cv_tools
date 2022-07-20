import spacy
from spacy.matcher import Matcher

nlp = spacy.load("pl_core_news_lg")

def extract_sanepid(text, filename):
    doc = nlp(text)

    # tworzenie patternow do znalezienia książeczki sanepidu

    san_1 = [{"LOWER": {"REGEX": "książeczka"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "sanepid"}}]    
    san_2 = [{"LOWER": {"REGEX": "ks"}}, {"OP": "?"}, {"OP": "?"}, {"LOWER": {"REGEX": "sanep"}}]    
    san_3 = [{"LOWER": {"REGEX": "sanepid"}}]    
    san_4 = [{"LOWER": {"REGEX": "san"}}, {"OP": "?"}, {"LOWER": {"REGEX": "epid"}}]
    
    matcher = Matcher(nlp.vocab)
    matcher.add("sanepid", [san_1, san_2, san_3, san_4])
    matches = matcher(doc)

    if len(matches) > 0:
        return([1, 0])
    else:
        return([0, 1])
