# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import operator

import requests
import json
finalDict = {}


def getRelevantDataIntoDict(country, response : dict, responseDest : dict):
    global finalDict
    finalDict[country] = {}
    finalDict[country]["distance"] = "the distance from Tel Aviv is " + response["rows"][0]["elements"][0]["distance"]["text"]
    finalDict[country]["time"] = "duration time is " + response["rows"][0]["elements"][0]["duration"]["text"].split(" ")[0] + " hours"
    finalDict[country]["lat"] = responseDest['results'][0]["geometry"]["location"]['lat']
    finalDict[country]["lng"] = responseDest['results'][0]["geometry"]["location"]['lng']


def read_data():
    api_key = ''
    address = 'תל אביב, ישראל'
    # url = "https://maps.googleapis.com/maps/api/geocode/json?units=imperial&origins=%s&destinations=%s&key=%s" % (address,addressRequierd, api_key)
    # response = requests.get(url).json()  # if the response is of json format the .json() will load the json into a python object
    # print(type(response))
    # return response
    text = open('dests.txt', 'r', encoding='utf-8')
    lines = text.readlines()
    for line in lines:
        addressRequierd = line.split('\n')[0]
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=%s&destinations=%s&key=%s" % (
        address, addressRequierd, api_key)
        try:
            response = requests.get(url)
            if not response.status_code == 200:
                print("HTTP error", response.status_code)
            else:
                try:
                    response = response.json()
                except:
                    print("Response not in valid JSON format")
        except:
            print("Something went wrong with requests.get")

        urlDest = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (addressRequierd, api_key)
        ##responseDest = requests.get(urlDest).json()
        #getRelevantDataIntoDict(addressRequierd, response, responseDest)
        try:
            responseDest = requests.get(urlDest)
            if not responseDest.status_code == 200:
                print("HTTP error", responseDest.status_code)
            else:
                try:
                    responseDest = responseDest.json()
                    getRelevantDataIntoDict(addressRequierd, response, responseDest)
                except:
                    print("Response not in valid JSON format")
        except:
            print("Something went wrong with requests.get")

    print(finalDict)

def getFarCities():
    dict = {}
    for key in finalDict:
        dict[key] = finalDict[key]["distance"][:-3]
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))
    sorted_dict = [i[0] for i in sorted_dict]
    return sorted_dict[2:]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    read_data()
    cities = getFarCities()
    print (cities)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
