import spacy
from spacy import displacy

text = None

with open("../dane/z/Aplikacja 19.txt", "r") as file:
    text = file.read()

nlp = spacy.load("pl_core_news_lg")
doc = nlp(text)
displacy.serve(doc, style="ent")