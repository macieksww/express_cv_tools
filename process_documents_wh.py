import os
import time
import datetime
from dateutil.relativedelta import relativedelta
from docker_manager import stop_all_containers, run_car_container, run_nominatim_container, \
run_bike_container, run_foot_container, stop_bike_container, \
stop_car_container, stop_foot_container, stop_nominatim_container
print("docker imported")
time.sleep(8)
import cv_data_extractor_locations_new
print("locations imported")
time.sleep(8)
# import cv_data_extractor_dates
# print("dates imported")
# time.sleep(8)
# from cv_data_extractor_birthdate_from_school import extract_birthdate_school
# time.sleep(5)
# from cv_data_extractor_experience_wh import extract_experience
# print("exp imported")
# time.sleep(8)
# from cv_data_extractor_education_wh import extract_education
# print("edu imported")

# print("Imports completed.")

exp_rates = []
edu_rates = []
cv_distance = {}

class ScoringFeature:
    def __init__(self, value, weight, name):
        self.value = value
        self.weight = weight
        self.name = name    

def process_directory(path, add_header, outputFile):
    separator = ';'
    exp_rates_list = []

    cv_distance_dict = process_locations(path)

    for filename in sorted(os.listdir(path)):
        if filename.endswith(".txt"):
            print("-----------------------------------")
            print(filename)
            with open( path + "/" + filename, "r") as file:
                text = file.read()

            file_key = filename[10:-4]
            distance_from_base = cv_distance_dict[file_key]

            # age_from_school = extract_birthdate_school(text, filename)
            # birth_date = cv_data_extractor_dates.extract_birth_date(text, filename)
            # age = relativedelta(datetime.date.today(), birth_date)
            # if age.years == 0:
            #     age.years = age_from_school

            # edu_level = extract_education(text, filename)
            # exp_level = extract_experience(text, filename)

            scoringFeatures = []

            # scoring features for age

            # age_test = (age.years >= 18 and age.years <= 30)
            # scoringFeatures.append(ScoringFeature(value=age_test, weight=5, name="Wiek 18-30"))

            # age_test = (age.years > 30 and age.years <= 40)
            # scoringFeatures.append(ScoringFeature(value=age_test, weight=4, name="Wiek 30-40"))

            # age_test = (age.years > 40 and age.years <= 45)
            # scoringFeatures.append(ScoringFeature(value=age_test, weight=1, name="Wiek 41-45"))

            # age_test = (age.years > 45)
            # scoringFeatures.append(ScoringFeature(value=age_test, weight=0, name="Wiek 45>"))

            # # scoring features for experience

            # scoringFeatures.append(ScoringFeature(value=exp_level[0], weight=5, name="Doświadczenie magazyn"))

            # scoringFeatures.append(ScoringFeature(value=exp_level[1], weight=3, name="Brak doświadczenia"))

            # scoringFeatures.append(ScoringFeature(value=exp_level[2], weight=4, name="Doświadczenie w pracy fiz."))
            
            # scoringFeatures.append(ScoringFeature(value=exp_level[3], weight=0, name="Doświadczenie ovq"))

            # scoringFeatures.append(ScoringFeature(value=exp_level[4], weight=1, name="Doświadczenie inne"))


            # # scoring features for education

            # scoringFeatures.append(ScoringFeature(value=edu_level[0], weight=1, name="Wyk. wyższe"))

            # scoringFeatures.append(ScoringFeature(value=edu_level[1], weight=3, name="W trakcie studiów"))

            # scoringFeatures.append(ScoringFeature(value=edu_level[2], weight=5, name="Wyk. średnie"))

            # scoringFeatures.append(ScoringFeature(value=edu_level[3], weight=5, name="Wyk. techniczne"))
            
            # scoringFeatures.append(ScoringFeature(value=edu_level[4], weight=0, name="Wyk. podstawowe"))
            
            # scoringFeatures.append(ScoringFeature(value=edu_level[5], weight=0, name="Brak wyk."))


            dist_test = (distance_from_base is not None) and (distance_from_base <= 5)
            scoringFeatures.append(ScoringFeature(value=dist_test, weight=5, name="Odl. <= 5km"))
            sf1 = ScoringFeature(value=dist_test, weight=5, name="Odl. <= 5km")
            print("pierwszy")
            print(sf1.weight*sf1.value)

            dist_test = (distance_from_base is not None) and (distance_from_base > 5 and distance_from_base <= 10)
            scoringFeatures.append(ScoringFeature(value=dist_test, weight=3, name="5km > Odl <= 10km"))
            sf2 = ScoringFeature(value=dist_test, weight=3, name="5km > Odl <= 10km")
            print("drugi")
            print(sf2.weight*sf2.value)

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


def process_locations(path):
    osrm_ports = [5000, 5001, 5002]
    for port in osrm_ports:
        stop_all_containers()
        # print("All containers stopped")
        run_nominatim_container()
        # print("Nominatim container running")
        time.sleep(10)

        if port == 5000:
            run_car_container()
            # print("Car container running")
            time.sleep(10)

        elif port == 5001:
            stop_car_container()
            # print("Car container stopped")
            run_bike_container()
            # print("Bike container running")
            time.sleep(10)

        elif port == 5002:
            stop_bike_container()
            # print("Bike container stopped")
            run_foot_container()
            # print("Foot container running")
            time.sleep(10)

        for filename in sorted(os.listdir(path)):
            if filename.endswith(".txt"):
                print("-----------------------------------")
                print(filename)
                file_key=filename[10:-4]
                with open( path + "/" + filename, "r") as file:
                    text = file.read()
                    distance_from_base = cv_data_extractor_locations_new.extract_distance_from_base(text, filename, port)
                    if distance_from_base is not None:
                        print(distance_from_base)
                        if file_key in cv_distance.keys():
                            if cv_distance[file_key]>distance_from_base:
                                cv_distance[file_key] = distance_from_base
                        else:
                            cv_distance[file_key] = distance_from_base
                    else:
                        if file_key in cv_distance.keys():
                            pass
                        else:
                            cv_distance[file_key] = 999
    stop_all_containers()

    print(cv_distance)
    return cv_distance


outputFile = open("wyniki.txt", "w")
print("Zaakceptowane:")
process_directory(path="dane_mag/p/txt", add_header=True, outputFile=outputFile)
# print("Odrzucone:")
# process_directory(path="dane_mag/o/txt", add_header=False, outputFile=outputFile)
outputFile.close()

