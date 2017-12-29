from app.mac import mac, signals
import json
import math
import random
import re

cars = json.load(open('db.json'))

welcomeMsg = [
    "Hi",
    "Hey",
    "Hello"
]
errMsg = [
    'Apparently we don\'t speak the same language',
    'I don\'t understand what you say??',
    'Try something else',
    'Ask for Help'
]

def findCars(message):
    sender_phone = phoneNum(message)
    return [car for car in cars if car['sender_phone'] == sender_phone]
def findCar(message, car_id):
    sender_phone = phoneNum(message)
    return [car for car in cars if car['sender_phone'] == sender_phone and car['id'] == car_id]
def findCarByName(message, name):
    sender_phone = phoneNum(message)
    return [car for car in cars if car['sender_phone'] == sender_phone and car['name'].lower() == name.lower()]
def findCarByModel(message, model):
    sender_phone = phoneNum(message)
    return [car for car in cars if car['sender_phone'] == sender_phone and car['model'].lower() == model.lower()]
def findCarBymatricule(message, matricule):
    sender_phone = phoneNum(message)
    return [car for car in cars if car['sender_phone'] == sender_phone and car['matricule'].lower() == matricule.lower()]

'''
Signals this module listents to:
1. When a message is received (signals.command_received)
==========================================================
'''
@signals.command_received.connect
def handle(message):
    #mac.send_message("Hello type `!help` for help", message.conversation)
    if message.command.lower() == "hi" or message.command.lower() == "hey" or message.command.lower() == "hello":
        hi(message)
    elif message.command.lower() == "login":
        mac.send_message("You don't need to login", message.conversation)
    elif message.command.lower() == 'car':
        msg = ""
        if re.compile('!car id \d*').match(message.message.lower()):
            id = message.message.lower().replace("!car id ", "").strip()
            mycars = findCar(message, id)
        if re.compile('!car brand \s*').match(message.message.lower()):
            brand = message.message.lower().replace("!car brand ", "").strip()
            mycars = findCarByName(message, brand)
        if re.compile('!car model \s*').match(message.message.lower()):
            model = message.message.lower().replace("!car model ", "").strip()
            mycars = findCarByModel(message, model)
        if re.compile('!car matricule \s*').match(message.message.lower()):
            model = message.message.lower().replace("!car matricule ", "").strip()
            mycars = findCarBymatricule(message, model)

        if len(mycars) == 0:
            mac.send_message("unfortunately you don't have any car yet!", message.conversation)

        if len(mycars) > 1:
            for car in mycars:
                msg = msg + "★ Brand: " + car['name'] + " | Model: " + car['model'] + "\n"
            mac.send_message(msg, message.conversation, False)
        else:
            mac.send_message("★ Brand: " + mycars[0]['name'] + ' | Model: ' + mycars[0]['model'], message.conversation)
            mac.send_image_url('https://maps.googleapis.com/maps/api/staticmap?size=764x400&center=' + mycars[0]['latitude'] + ',' + mycars[0]['longitude'] + '&zoom=13&markers=' + mycars[0]['latitude'] + ',' + mycars[0]['longitude'],
                           message.conversation,
                           "★ Brand: " + mycars[0]['name'] + ' | Model: ' + mycars[0]['model'])

    elif message.command.lower() == 'cars':
        mycars = findCars(message)
        if len(mycars) == 0:
            mac.send_message("unfortunately you don't have any car yet!", message.conversation)
        msg = ""
        for car in mycars:
            msg = msg + "★ Brand:" + car['name'] + " | Model: " + car['model'] + "\n"
        mac.send_message(msg, message.conversation, False)

    elif message.command == "help":
        help(message)
    else:
        mac.send_message(errMsg[math.floor(random.random() * len(errMsg))], message.conversation)

'''
Actual module code
==========================================================
'''
def phoneNum(message):
    return message.who.replace("@s.whatsapp.net", "").strip()
def hi(message):
    who_name = message.who_name

    answer = welcomeMsg[math.floor(random.random() * len(welcomeMsg))] + " " + who_name
    mac.send_message(answer, message.conversation)
    
def help(message):
    answer = "✧ Bot called Orpheus ✧ \n" \
             "☆ !car id {id) | Display car by id\n" \
             "☆ !car brand {name} | Display car(s) by brand name\n" \
             "☆ !car model {model} | Display car(s) by model\n" \
             "☆ !car matricule {matricule} | Display car by matricule\n" \
             "☆ !cars | List cars by page each page has 4 cars\n" \
             "☆ !help | Display help"
    mac.send_message(answer, message.conversation)
