import cv_data_extractor_driving_license
import cv_data_extractor_dates
import cv_data_extractor_locations
import datetime
from dateutil.relativedelta import relativedelta
import os

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
                print("read")
                driving_license = cv_data_extractor_driving_license.extract_driving_license(text, filename)
                print("dl")
                birth_date = cv_data_extractor_dates.extract_birth_date(text, filename)
                print("bd")
                distance_from_base = cv_data_extractor_locations.extract_distance_from_base(text, filename)
                print("d")
            age = relativedelta(datetime.date.today(), birth_date)

            print("Age appended")

            scoringFeatures = []
            scoringFeatures.append(ScoringFeature(value=driving_license["has_license"], weight=5, name="Ma prawo jazdy B"))

            print("Scoring features appended")


            scoringFeatures.append(ScoringFeature(value=driving_license["has_license_only_car"], weight=5, name="Ma tylko prawo jazdy B"))

            scoringFeatures.append(ScoringFeature(value=(birth_date is not None) and (age.years >= 19), weight=4, name="Posiada prawo jazdy od > 1 roku"))

            scoringFeatures.append(ScoringFeature(value=driving_license["is_driver"] or driving_license["is_truck_driver"], weight=2, name="Pracował jako kierowca"))

            scoringFeatures.append(ScoringFeature(value=0, weight=1, name="Inne doświadzczenie"))

            age_test = (birth_date is not None) and (age.years < 19)
            scoringFeatures.append(ScoringFeature(value=age_test, weight=1, name="Wiek < 19"))

            age_test = (birth_date is not None) and (age.years >= 19 and age.years <= 25)
            scoringFeatures.append(ScoringFeature(value=age_test, weight=5, name="Wiek 19-25"))

            age_test = (birth_date is not None) and (age.years > 25 and age.years <= 30)
            scoringFeatures.append(ScoringFeature(value=age_test, weight=4, name="Wiek 26-30"))

            age_test = (birth_date is not None) and (age.years > 30 and age.years <= 40)
            scoringFeatures.append(ScoringFeature(value=age_test, weight=2, name="Wiek 31-40"))

            age_test = (birth_date is not None) and (age.years > 40)
            scoringFeatures.append(ScoringFeature(value=age_test, weight=0, name="Wiek > 40"))

            dist_test = (distance_from_base is not None) and (distance_from_base <= 5)
            scoringFeatures.append(ScoringFeature(value=dist_test, weight=5, name="Odl. <= 5km"))

            dist_test = (distance_from_base is not None) and (distance_from_base > 5 and distance_from_base <= 10)
            scoringFeatures.append(ScoringFeature(value=dist_test, weight=3, name="5km > Odl <= 10km"))


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
# print(len(outputFile))
print("Zaakceptowane:")
process_directory(path="dane/z", add_header=True, outputFile=outputFile)
print("Odrzucone:")
process_directory(path="dane/o", add_header=False, outputFile=outputFile)
outputFile.close()