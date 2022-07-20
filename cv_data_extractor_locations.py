import spacy
from spacy import displacy
from spacy.matcher import Matcher
import os
import re
import csv
import requests
import json
import time

nlp = spacy.load("pl_core_news_lg")

# osrm_ports = [5000,5001, 5002]
osrm_ports = [5000]


def process_directory(path):
    for filename in sorted(os.listdir(path)):
        if filename.endswith(".txt"):
            print("-----------------------------------")
            print(filename)
            with open( path + "/" + filename, "r") as file:
                text = file.read()
                extract_distance_from_base(text, filename)

def loadCitiesList():
    citiesFile=open("miejscowosci.csv")
    citiesReader = csv.reader(citiesFile, delimiter = ';')
    cities = []
    for city in citiesReader:
        cities.append(city[0])
    return cities

def loadBasesList():
    basesFile=open("bazy.txt")
    basesReader = csv.reader(basesFile, delimiter = ';')
    bases = []
    for base in basesReader:
        bases.append(base[0])
    return bases

def getCoordinates(location):
    print("Get coordinates start")
    r = requests.get("http://localhost:8080/search.php?q="+str(location))
    print("Get coordinates end")

    if r.text is not None:
        reply = json.loads(r.text)
        if len(reply) > 0:
            selected_match = 0
            for match_idx in range(0,len(reply)):
                if reply[match_idx]["category"] == "building":
                    selected_match = match_idx
                    break
            if reply[selected_match]["lat"] is not None and reply[selected_match]["lon"] is not None:
                return {"lat":reply[selected_match]["lat"], "lon":reply[selected_match]["lon"]}
    return None

def getDistance(location1, location2, port):
    print("Get distance start")
    try:
        r = requests.get("http://127.0.0.1:"+str(port)+"/route/v1/profile/"+str(location1["lon"])+","+str(location1["lat"])+";"+str(location2["lon"])+","+str(location2["lat"])+"?steps=false&alternatives=false")
        print("Request ok")
    except:
        print("Request failed")
        pass

    print("Get distance end")
    print('\n')
    print("Request response:")
    print('\n')
    print(r)

    if r.text is not None:
        reply = json.loads(r.text)
        if reply["routes"] is not None:
            shortest_distance = 20000000
            for route in reply["routes"]:
                distance = float(route["distance"])
                if distance < shortest_distance:
                    shortest_distance = distance
            return shortest_distance
            #return float(reply["routes"][0]["distance"])

    return None

def testRouting():
    loc1 = getCoordinates("16-200")
    loc2 = getCoordinates("02-315")
    print(loc1)
    print(loc2)
    dist = getDistance(loc1,loc2)
    print("Distance: " + str(dist))
    bases = loadBasesList()
    for base in bases:
        print(base)
        print(getCoordinates(base))

def extract_distance_from_base(text, filename):
    matcher = Matcher(nlp.vocab)
    doc = nlp(text)
    currentPlaceList = []
    locationPrefixes = ["miejscowość", "miasto", "miejsce", "zamieszkania", "zameldowania", "adres"]
    citiesList = loadCitiesList()
    locPrefixIndex = -1
    search_range = 4
    search_forward = 25
    for token in doc:
        for prefix in locationPrefixes:
            if token.lower_.find(prefix,0, len(token.text)) != -1:
                locPrefixIndex = token.i
                #print("Prefix found:" + token.text)
                break
        if locPrefixIndex != -1:
            break
    
    cityName = None

    if locPrefixIndex != -1:
        for startIndex in range(locPrefixIndex, locPrefixIndex+search_forward):
            searchedString = ""
            cityFound = False
            for tokenIndex in range(startIndex, startIndex+search_range):
                if tokenIndex < len(doc):
                    searchedString += doc[tokenIndex].text_with_ws
            #print("Searched string: "+ searchedString)
            lastCityStrLen = 0
            for city in citiesList:
                if searchedString.lower().find(city.lower(),0, len(searchedString)) != -1:
                    cityMatches = re.findall("([^a-z]|^)"+city.lower()+"([^a-z]|$)", searchedString.lower())
                    if len(cityMatches) > 0:
                        #print(searchedString.lower() + " "+ city)
                        if len(city) > lastCityStrLen:
                            cityName = city
                            lastCityStrLen = len(city)
                        cityFound = True
            if cityFound:
                break
#    for ent in doc.ents:
#        if ent.label_ == "placeName":
#            print(ent.text, ent.start_char, ent.end_char, ent.label_)
    matches = re.findall("[^0-9][0-9]{2}\-[0-9]{3}[^0-9]", text)
#    for match in matches:
#        print(match)
    
    location = None

    if len(matches) > 0:
        location = matches[0]
    elif cityName is not None:
        location = cityName

    if location is not None:
        loc1 = getCoordinates(location)
        bases = loadBasesList()
        distance = 0
        closest_port = ""
        isFirst = True
        for base in bases:
            for port in osrm_ports:
                loc2 = getCoordinates(base)
                print("Location 1: \n")
                print(loc1)
                print("Location 2: \n")
                print(loc2)

                dist = getDistance(loc1, loc2, port)
                if distance > dist or isFirst:
                    distance = dist
                    closest_port = port
                    isFirst = False
                print("Distance read, sleep 2s.")
                # time.sleep(2)

        print(location + " " + str(distance/1000.0) + " " + str(closest_port))
        return distance/1000.0
    else:
        return None



#testRouting()
#print("Zaakceptowane:")
#process_directory("dane/z")
#print("Odrzucone:")
#process_directory("dane/o")
