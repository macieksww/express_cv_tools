import spacy
from spacy import displacy
from spacy.matcher import Matcher
import os
import csv
import pandas as pd
from csv_reader import read_csv

nlp = spacy.load("pl_core_news_lg")

# funkcja do odczytania plikow csv z patternami do poszczegolnych podkategorii dla kategoii
# i okresleniami definiujacymi poszczegolne czesci cv


def extract_cv_parts(text, filename):

    csv_dict = read_csv()
    cv_dict = csv_dict[1]

    matcher = Matcher(nlp.vocab)
    doc = nlp(text)

    exp_start_end = []
    cap_start_end = []
    edu_start_end = []
    hbb_start_end = []
    ach_start_end = []

    exp_start = []
    cap_start = []
    edu_start = []
    hbb_start = []
    ach_start = []

    # tworzenie patternow do znalezienia czesci CV (doswiadczenie, umiejetnosci, edukacja, zainteresowania, osiagniecia)
    # szukanie punktow mogacych oznaczac poczatek sekcji "Doswiadczenie"

    exp_list = list(cv_dict['exp'])
    exp_part_pattern = [{"LOWER": {"IN": exp_list}}]
    matcher_exp_part = Matcher(nlp.vocab)
    matcher_exp_part.add("has_exp", [exp_part_pattern])
    matches_exp = matcher_exp_part(doc)

    for match_id, start, end in matches_exp:
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end]
        print(match_id, string_id, start, end, span.text)
        exp_start.append(start)

    # szukanie punktow mogacych oznaczac poczatek sekcji "Umiejetnosci"

    cap_list = list(cv_dict['cap'])
    cap_part_pattern = [{"LOWER": {"IN": cap_list}}]
    matcher_cap_part = Matcher(nlp.vocab)
    matcher_cap_part.add("has_cap", [cap_part_pattern])
    matches_cap = matcher_cap_part(doc)

    for match_id, start, end in matches_cap:
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end]
        print(match_id, string_id, start, end, span.text)
        cap_start.append(start)

    # szukanie punktow mogacych oznaczac poczatek sekcji "Edukacja"

    edu_list = list(cv_dict['edu'])
    edu_part_pattern = [{"LOWER": {"IN": edu_list}}]
    matcher_edu_part = Matcher(nlp.vocab)
    matcher_edu_part.add("has_edu", [edu_part_pattern])
    matches_edu = matcher_edu_part(doc)

    for match_id, start, end in matches_edu:
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end]
        print(match_id, string_id, start, end, span.text)
        edu_start.append(start)

    # szukanie punktow mogacych oznaczac poczatek sekcji "Zainteresowania"

    hbb_list = list(cv_dict['hbb'])
    hbb_part_pattern = [{"LOWER": {"IN": hbb_list}}]
    matcher_hbb_part = Matcher(nlp.vocab)
    matcher_hbb_part.add("has_hbb", [hbb_part_pattern])
    matches_hbb = matcher_hbb_part(doc)

    for match_id, start, end in matches_hbb:
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end]
        print(match_id, string_id, start, end, span.text)
        hbb_start.append(start)

    # szukanie punktow mogacych oznaczac poczatek sekcji "Osiagniecia"

    ach_list = list(cv_dict['ach'])
    ach_part_pattern = [{"LOWER": {"IN": ach_list}}]
    matcher_ach_part = Matcher(nlp.vocab)
    matcher_ach_part.add("has_ach", [ach_part_pattern])
    matches_ach = matcher_ach_part(doc)

    for match_id, start, end in matches_ach:
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end]
        print(match_id, string_id, start, end, span.text)
        ach_start.append(start)

    cv_part_spans = [(min(exp_start, default=0), "exp"), (min(edu_start, default=0), "edu"),
     (min(hbb_start, default=0), "hbb"), (min(cap_start, default=0), "cap"), (min(ach_start, default=0), "ach")]
    cv_part_spans = sorted(cv_part_spans, key=lambda x: x[1])
    print(cv_part_spans)
    return (cv_part_spans)