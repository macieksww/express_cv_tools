import time
import cv_data_extractor_driving_license
print(" dl ")
time.sleep(5)
import cv_data_extractor_dates
print(" dt ")
time.sleep(5)
# import cv_data_extractor_truck
# print(" tr ")
# time.sleep(5)
# import cv_data_extractor_sanepid
# print(" san ")
# time.sleep(30)
# import cv_data_extractor_experience_kurier
# print(" exp ")
time.sleep(5)
import cv_data_extractor_birthdate_from_school
print(" bdt ")
time.sleep(5)

import datetime
from dateutil.relativedelta import relativedelta
import os

person_distance_dict = {}
exp_rates = []
sanepid_rates = []
truck_rates = []

class ScoringFeature:
    def __init__(self, value, weight, name):
        self.value = value
        self.weight = weight
        self.name = name

def process_directory(path, add_header, outputFile):
    separator = ';'
    for filename in sorted(os.listdir(path)):
        if filename.endswith(".txt"):
            print("-----------------------------------")
            print(filename)
            with open( path + "/" + filename, "r") as file:
                text = file.read()

            driving_license = cv_data_extractor_driving_license.extract_driving_license(text, filename)
            birth_date = cv_data_extractor_dates.extract_birth_date(text, filename)
            age = relativedelta(datetime.date.today(), birth_date)
            age_from_school = cv_data_extractor_birthdate_from_school.extract_birthdate_school(text, filename)

            # print("Age: " + str(age.years))
            # print("Age from school: " + str(age_from_school))
            if age.years == 0:
                age.years = age_from_school
            
            print( "age years")
            print(age.years)

            # exp_level = cv_data_extractor_experience_kurier.extract_experience(text, filename)
            # exp_rates.append(exp_level)
            # print(exp_rates)

            # sanepid = cv_data_extractor_sanepid.extract_sanepid(text, filename)
            # sanepid_rates.append(sanepid)
            # print(sanepid_rates)

            # truck = cv_data_extractor_truck.extract_truck(text, filename)
            # truck_rates.append(truck)
            # print(truck_rates)

            scoringFeatures = []

            # # scoring features for experience
            
            # scoringFeatures.append(ScoringFeature(value=exp_level[0], weight=4, name="Dośw. kurier"))

            # scoringFeatures.append(ScoringFeature(value=exp_level[1], weight=3, name="Dośw. praca fizyczna"))

            # scoringFeatures.append(ScoringFeature(value=exp_level[2], weight=2, name="Dośw. inne"))

            # scoringFeatures.append(ScoringFeature(value=exp_level[3], weight=0, name="BRak dośw."))

            # # scoring features for sanepid
            
            # scoringFeatures.append(ScoringFeature(value=sanepid[0], weight=2, name="Posiada ks. sanepid"))

            # scoringFeatures.append(ScoringFeature(value=sanepid[1], weight=0, name="Nie posiada ks. sanepid"))

            # # scoring features for truck
            
            # scoringFeatures.append(ScoringFeature(value=truck[0], weight=3, name="Dośw. w kierowaniu samochodem dostawczym"))

            # scoringFeatures.append(ScoringFeature(value=truck[1], weight=0, name="Brak dośw. w kierowaniu samochodem dostawczym"))


            # scoringFeatures.append(ScoringFeature(value=driving_license["has_license"], weight=5, name="Ma prawo jazdy B"))

            # scoringFeatures.append(ScoringFeature(value=driving_license["has_license_only_car"], weight=5, name="Ma tylko prawo jazdy B"))

            # scoringFeatures.append(ScoringFeature(value=(birth_date is not None) and (age.years < 20), weight=0, name="Posiada prawo jazdy od < 2 lat"))

            # scoringFeatures.append(ScoringFeature(value=(birth_date is not None) and (age.years >= 20 and age.years < 21), weight=2, name="Posiada prawo jazdy 2-3 lata"))

            # scoringFeatures.append(ScoringFeature(value=(birth_date is not None) and (age.years >= 21), weight=4, name="Posiada prawo jazdy od >3 lat"))

            age_test = (age.years <= 21)
            scoringFeatures.append(ScoringFeature(value=age_test, weight=0, name="Wiek < 21"))

            age_test = (age.years > 21 and age.years <= 30)
            scoringFeatures.append(ScoringFeature(value=age_test, weight=4, name="Wiek 19-25"))

            age_test = (age.years > 30 and age.years <= 40)
            scoringFeatures.append(ScoringFeature(value=age_test, weight=3, name="Wiek 26-30"))

            age_test = (age.years > 40 and age.years <= 50)
            scoringFeatures.append(ScoringFeature(value=age_test, weight=1, name="Wiek 31-40"))

            age_test = (age.years > 50)
            scoringFeatures.append(ScoringFeature(value=age_test, weight=0, name="Wiek > 40"))


            if add_header:
                headerStr = "Ścieżka;Nazwa pliku"
                add_header = False
                for feature in scoringFeatures:
                    headerStr += separator + feature.name
                outputFile.write(headerStr+'\n')
            
            outputStr = path + ";" + filename
            for feature in scoringFeatures:
                outputStr += separator + str(feature.weight*feature.value)
            
            print(outputStr)
            outputFile.write(outputStr+'\n')


outputFile = open("wyniki_kurier.txt", "w")
print("Zaakceptowane:")
process_directory(path="dane_kurier/z/txt", add_header=True, outputFile=outputFile)
print("Odrzucone:")
process_directory(path="dane_kurier/o/txt", add_header=False, outputFile=outputFile)
outputFile.close()