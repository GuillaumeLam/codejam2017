# from urllib import urlopen
import urllib.parse
import csv
import requests
from pprint import pprint
import time
import json

html_string = ''
base_url = "https://api.opencagedata.com/geocode/v1/json?"

f = open("codejam2017\key.txt", "r")
key = f.read()

lattitude = 0
longitude = 0
state = 0

def parseJson():
    with open('./roaddata/useable-dictionaries-json/filtered-manhatan.json', 'r') as file:
        death_points = json.loads(file)

    return death_points


def getCoordinates():

    data = dict()

    file = open('./datasets/Transportation/NYC General Transport/vehicle-collisions-abridged.csv', 'r')
    j = 0
    with file as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for i, line in enumerate(reader):
            if i == 0:
                continue           
            else:
                lattitude = float(line[1])
                longitude = float(line[2])
                results = sendQuery(lattitude, longitude)
                write_to_file(str(lattitude) + ', ' + str(longitude))
                
                time.sleep(1.01)

            j+=1
            if(j >=1):
                return

def write_to_file(data):
    with open("geo-data.json", 'w+') as f:
        json.dump(data, f)

def sendQuery(lattitude, longitude):
    latlon = str(lattitude) + '+' + str(longitude)
    getVariables = {'q': latlon , 'key': key}
    page_url = base_url + urllib.parse.urlencode(getVariables)
    print(page_url)
    try:
        response = requests.get(page_url)
        data = response.json()
        
        isResult = data['total_results']

        if int(isResult) == 0 :
            print('no results')
            return
        results = data['results']
        return results
        #write_to_file(results)
    except:
        print('Error: cannot crawl page')

    
if __name__ == "__main__":
    getCoordinates()
