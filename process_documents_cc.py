import os
import time
# time.sleep(2)
# from cv_data_extractor_birthdate_from_school import extract_birthdate_school
# time.sleep(5)
print("sys imported")
from cv_data_extractor_experience import extract_experience
print("exp imported")
time.sleep(5)
from cv_data_extractor_eng import extract_english
print("eng imported")
time.sleep(5)
from cv_data_extractor_office import extract_office
print("off imported")
time.sleep(5)
from cv_data_extractor_education import extract_education
print("edu imported")

print("Imports completed.")

exp_rates = []
office_rates = []
eng_rates = []
edu_rates = []
age_list = []

class ScoringFeature:
    def __init__(self, value, weight, name):
        self.value = value
        self.weight = weight
        self.name = name    

def process_directory(path, add_header, outputFile):
    separator = ';'
    exp_rates_list = []

    for filename in sorted(os.listdir(path)):
        if filename.endswith(".txt"):
            print("-----------------------------------")
            print(filename)
            with open( path + "/" + filename, "r") as file:
                text = file.read()

            office_level = extract_office(text, filename)
            office_rates.append(office_level)
            print(office_rates)

            eng_level = extract_english(text, filename)
            eng_rates.append(eng_level)
            print(eng_rates)

            edu_level = extract_education(text, filename)
            edu_rates.append(edu_level)
            print(edu_rates)

            exp_level = extract_experience(text, filename)
            exp_rates.append(exp_level)
            print(exp_rates)

            # age = extract_birthdate_school(text, filename)
            # age_list.append(age)

            scoringFeatures = []

            # # scoring features for age from school

            # age_test = (age >= 18) and (age <= 26)
            # scoringFeatures.append(ScoringFeature(value=age_test, weight=5, name="Wiek 18-26"))

            # age_test = (age > 26) and (age <= 45)
            # scoringFeatures.append(ScoringFeature(value=age_test, weight=3, name="Wiek 27-45"))

            # age_test = (age > 45) and (age <= 55)
            # scoringFeatures.append(ScoringFeature(value=age_test, weight=2, name="Wiek 45-55"))

            # age_test = (age > 55)
            # scoringFeatures.append(ScoringFeature(value=age_test, weight=0, name="Wiek 55+"))

            # scoring features for english
            
            scoringFeatures.append(ScoringFeature(value=eng_level[1], weight=2, name="Angielski podstawowy"))

            scoringFeatures.append(ScoringFeature(value=eng_level[2], weight=5, name="Angielski śreniozaawansowany"))

            scoringFeatures.append(ScoringFeature(value=eng_level[3], weight=3, name="Angielski zaawansowany"))

            scoringFeatures.append(ScoringFeature(value=eng_level[0], weight=0, name="Angielski brak"))
            
            # scoring features for experience

            scoringFeatures.append(ScoringFeature(value=exp_level[0], weight=5, name="Doświadczenie call-center"))

            scoringFeatures.append(ScoringFeature(value=exp_level[1], weight=3, name="Brak doświadczenia"))

            scoringFeatures.append(ScoringFeature(value=exp_level[2], weight=4, name="Doświadczenie obs. klienta"))
            
            scoringFeatures.append(ScoringFeature(value=exp_level[3], weight=0, name="Doświadczenie ovq"))

            scoringFeatures.append(ScoringFeature(value=exp_level[4], weight=1, name="Doświadczenie inne"))

            # scoring features for MS Office

            scoringFeatures.append(ScoringFeature(value=office_level[0], weight=0, name="Office brak"))
            
            scoringFeatures.append(ScoringFeature(value=office_level[1], weight=3, name="Office podstawowy"))

            scoringFeatures.append(ScoringFeature(value=office_level[2], weight=5, name="Office śreniozaawansowany"))

            # scoring features for education

            scoringFeatures.append(ScoringFeature(value=edu_level[2], weight=5, name="Wyk. średnie"))

            scoringFeatures.append(ScoringFeature(value=edu_level[0], weight=5, name="Wyk. wyższe"))
            
            scoringFeatures.append(ScoringFeature(value=edu_level[3], weight=2, name="Wyk. podstawowe"))
            
            scoringFeatures.append(ScoringFeature(value=edu_level[4], weight=0, name="Brak wyk."))

            scoringFeatures.append(ScoringFeature(value=edu_level[1], weight=5, name="W trakcie studiów"))

            if add_header:
                headerStr = "Ścieżka;Nazwa pliku"
                add_header = False
                for feature in scoringFeatures:
                    headerStr += separator + feature.name
                outputFile.write(headerStr+'\n')
            
            outputStr = path + ";" + filename
            for feature in scoringFeatures:
                outputStr += separator + str(feature.weight*feature.value)
            outputFile.write(outputStr+'\n')


outputFile = open("wyniki.txt", "w")

print("Zaakceptowane:")
process_directory(path="dane_cc/txt/z", add_header=True, outputFile=outputFile)
print("Odrzucone:")
process_directory(path="dane_cc/txt/o", add_header=False, outputFile=outputFile)
print("Pozostale formaty:")
process_directory(path="dane_cc/txt/oth", add_header=False, outputFile=outputFile)
outputFile.close()
