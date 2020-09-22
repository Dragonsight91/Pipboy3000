from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os
import sys
import pygame
import gui
from gui import *
import json
import socket
from time import sleep
import serial
import platform

# read the config file
SETUP = json.loads(open("configs/config.JSON", "r").read())

OS = ""
raw = platform.platform(terse=True).split("-")
for element in raw:
    OS += element+" "
OS = OS.split(" ")[0]
print(OS)
print(SETUP["port"][OS])


#print("\nCONFIG:\n", json.dumps(SETUP, indent=4), "\n")


def initTeensy(state=0):
    try:
        conn = serial.Serial(SETUP["port"][OS], timeout=20)
        conn.write(b"con_init\n")
        answer = conn.readline()
        answer = answer[:len(answer)-len(b"\r\n")].decode("UTF-8")
        print(answer)
        if answer == "Ready":
            print(("con_setup:"+str(state)+"\n").encode("UTF-8"))
            conn.write(("con_setup:"+str(state)+"\n").encode("UTF-8"))
            answer = conn.readline()
            answer = answer[:len(answer)-len(b"\r\n")].decode("UTF-8")
            print(answer)
        conn.close()
    except Exception as e:
        print("connection failed!!\n")
        print(e)


def testSerial():
    try:
        conn = serial.Serial(SETUP["port"][OS], timeout=20)

        conn.write(b"con_test\n")
        answer = conn.readline()
        answer = answer[:len(answer)-len(b"\r\n")].decode("UTF-8")
        print(answer)
        if answer == "success":
            SETUP["Serial"] = True
        else:
            SETUP["Serial"] = False
        conn.close()
    except Exception as e:
        SETUP["Serial"] = False
        print(e)


# DO NOT CHANGE SCOPES VARIABLE
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'


def is_connected(hostname):
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False


def calendar():
    # Uses the Google Calendar API and the calendarId from main.conf to load the upcoming 10 events from specified calendar.

    store = file.Storage(SETUP["token"])
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(SETUP["cliSecret_G"], SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId=SETUP["calID"],
                                          timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(event)
    with open(SETUP["events"], "w") as f:
        f.write(json.dumps(events, indent=4))


testSerial()
# get info, wether or not the calendar should be loaded and wether or not it actually can be loaded
user = "n"
if is_connected("www.google.com"):
    print("\ninternet connection works")
if not is_connected("www.google.com"):
    print("Loading from google calendar not possible, no internet connection.")
    user = "noconnect"
elif SETUP["loadCal"] and SETUP["autoload"] == False:
    print("To enable autoload, check file configs/main.conf")
    user = input("Do you want to load from Calendar? (y,yes/n,no)")
elif SETUP["loadCal"] == False:
    user = "disconf"
elif SETUP["autoload"]:
    print("autoloading enabled, to disable check the file configs/main.conf")
    user = "y"
print(user)
# test connection, config and or user input
if is_connected("www.google.com") and (user == "y" or user == "yes"):
    print("writing events to configs/events.json\n")

    calendar()
elif user == "noconnect":
    print("no connection, calendar not loaded")

elif user == "n" or user == "no" or user == "":
    print("Calendar not loaded")

elif user == "disconf":
    print("loading Calendar disabled in configs/main.conf")

# get info from SETUP (SETUP takes the main.conf file as JSON input)
color = SETUP["color"]
header_draw = SETUP["header_draw"]

# initialize the window
ver = SETUP["version"]
pygame.init()
pygame.font.init()
# set window size
info = pygame.display.Info()
if SETUP["fullscreen"]:
    winsize = (info.current_w, info.current_h)
else:
    winsize = (info.current_w//2, info.current_h//2)

font = pygame.font.Font(SETUP["font"], int(
    ((winsize[0]/100)*header_draw['text_h'])/1.09))
icon = pygame.image.load(SETUP["icon_path"])
pygame.display.set_icon(icon)
pygame.display.set_caption("Pip-Boy 3000 " + ver)

if SETUP["fullscreen"]:
    win = pygame.display.set_mode(winsize, pygame.FULLSCREEN)
else:
    win = pygame.display.set_mode(winsize)

pygame.mouse.set_visible(False)

# base variables
run = True
# this is used to hold information about the button inputs
select = {
    'knob': 0,
    'wheel': 0,
    'buttons': 1,
    'selectors': [0, 0]
}
initTeensy(select["buttons"])

# this is the setup part, here i create the tabs
head = gui.header.head(win, winsize, header_draw, color, font, SETUP["player"])
SETUP["player"] = head.player
items = gui.items.items(win, winsize, font, color,
                        header_draw, select, SETUP["player"], SETUP)
stats = gui.stats.stats(win, winsize, font, color, header_draw, SETUP)

# TIMEOUT VARIABLES
scroll = 0
switch = 0
settings = 0
selScroll = 0
opt = 0
set = 0
delay = 75
serialTest = 0
#REDRAW (inefficient)


def redraw():
    win.fill(SETUP["background"])
    if select['buttons'] == 0:
        stats.update(select, SETUP["player"])
    if select['buttons'] == 1:
        SETUP["player"] = items.update(select, stats.itemlist, SETUP["player"])
    if select['buttons'] == 2:
        pass
    head.update(select, SETUP, SETUP["player"])
    pygame.display.update()


# MAIN LOOP
while run:
    if serialTest == 0:
        testSerial()
        serialTest = 100000000
    else:
        serialTest -= 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # print(SETUP["player"]["STR"]["timeout"])
    for name in SETUP["effectlist"]:
        if SETUP["player"][name]["timeout"] > 0:
            SETUP["player"][name]["timeout"] -= 1
        if SETUP["player"][name]["amount"] > 0 and SETUP["player"][name]["timeout"] == 0:
            SETUP["player"][name]["amount"] = 0
    # Spam protection/input timeout (in cycles)
    if scroll > 0:
        scroll += 1
    if scroll > delay:
        scroll = 0
    if set > 0:
        set += 1
    if set > delay:
        set = 0
    if switch > 0:
        switch += 1
    if switch > delay:
        switch = 0
    # if settings > 0:
    #     settings +=1
    # if settings > delay:
    #     settings = 0
    if selScroll > 0:
        selScroll += 1
    if selScroll > delay:
        selScroll = 0
    if opt > 0:
        opt += 1
    if opt > delay:
        opt = 0

    if keys[pygame.K_1]:
        select['buttons'] = 0
        select['wheel'] = 0
        select['selectors'][0] = 0
        select['selectors'][1] = 0
        stats.selid[0] = 0
        stats.selid[1] = 5
    if keys[pygame.K_2]:
        select['buttons'] = 1
        select['wheel'] = 0
        select['selectors'][0] = 0
        select['selectors'][1] = 0
        stats.selid[0] = 0
        stats.selid[1] = 5
    if keys[pygame.K_3]:
        select['buttons'] = 2
        select['wheel'] = 0
        select['selectors'][0] = 0
        select['selectors'][1] = 0
        stats.selid[0] = 0
        stats.selid[1] = 5
    if keys[pygame.K_RIGHT] and select['knob']+1 < 5 and switch == 0:
        select['knob'] += 1
        select['wheel'] = 0
        switch += 1
        select['selectors'][0] = 0
        select['selectors'][1] = 0
        stats.selid[0] = 0
        stats.selid[1] = 5
    if keys[pygame.K_LEFT] and select['knob']-1 > -1 and switch == 0:
        select['knob'] -= 1
        select['wheel'] = 0
        switch += 1
        select['selectors'][0] = 0
        select['selectors'][1] = 0
        stats.selid[0] = 0
        stats.selid[1] = 5
    if keys[pygame.K_DOWN] and scroll == 0:
        if select['buttons'] == 1:
            if select['wheel']+1 < len(items.screenlist):
                select['wheel'] += 1
                scroll += 1
            elif items.sel[1] < len(items.visible):
                items.sel[0] += 1
                items.sel[1] += 1
        elif select['knob'] == 4 and select['buttons'] == 0:
            if select['wheel']+1 < len(stats.screenlist) and select['knob'] == 4 and select['buttons'] == 0:
                select['wheel'] += 1
            elif stats.sel[1] < len(stats.visible):
                stats.sel[0] += 1
                stats.sel[1] += 1

            select['selectors'][0] = 0
            select['selectors'][1] = 0
            stats.selid[0] = 0
            stats.selid[1] = 5
        scroll += 1
    if keys[pygame.K_UP] and scroll == 0:
        if select['buttons'] == 1:
            if select['wheel']-1 > -1:
                select['wheel'] -= 1
            elif items.sel[0] > 0:
                items.sel[0] -= 1
                items.sel[1] -= 1
        elif select['knob'] == 4 and select['buttons'] == 0:
            if select['wheel']-1 > -1:
                select['wheel'] -= 1
            elif stats.sel[0] > 0:
                stats.sel[0] -= 1
                stats.sel[1] -= 1
            select['selectors'][0] = 0
            select['selectors'][1] = 0
            stats.selid[0] = 0
            stats.selid[1] = 5
        scroll += 1

    if keys[pygame.K_s] and selScroll == 0:

        if select['knob'] == 4 and select['buttons'] == 0:
            if select['selectors'][0]+1 < len(stats.idvisible) and select['knob'] == 4 and select['buttons'] == 0:
                select['selectors'][0] += 1
                if stats.selid[1] < len(stats.idvisible):
                    print("S")
                    stats.selid[0] += 1
                    stats.selid[1] += 1
                    selScroll += 1
    if keys[pygame.K_w] and selScroll == 0:

        if select['knob'] == 4 and select['buttons'] == 0:
            if select['selectors'][0]-1 > -1 and select['knob'] == 4 and select['buttons'] == 0:
                select['selectors'][0] -= 1
                if stats.selid[0] > 0:
                    print("W")
                    stats.selid[0] -= 1
                    stats.selid[1] -= 1
                    selScroll += 1
    if keys[pygame.K_d] and opt == 0:
        if select['knob'] == 4 and select['buttons'] == 0 and select['selectors'][1]+1 < len(stats.options[select["knob"]]):
            select['selectors'][1] += 1
        if select["buttons"] == 1 and select['selectors'][1]+1 < len(items.options[select["knob"]]):
            select["selectors"][1] += 1
        opt += 1
    if keys[pygame.K_e] and opt == 0:
        if select['knob'] == 4 and select['buttons'] == 0 and select['selectors'][1]-1 > -1:
            select['selectors'][1] -= 1
        if select["buttons"] == 1 and select['selectors'][1]-1 > -1:
            select['selectors'][1] -= 1
        opt += 1

    if keys[pygame.K_RETURN] and set == 0:
        if select['knob'] == 4 and select['buttons'] == 0 and select['selectors'][1] == 0 and SETUP["Serial"]:
            size = [int(winsize[0]//2), int(winsize[1]//5)]
            pos = [int((winsize[0]-size[0])//2), int((winsize[1]-size[1])//2)]
            pygame.draw.rect(win, SETUP['background'],
                             (pos[0], pos[1], size[0], size[1]))
            pygame.draw.rect(win, (0, 255, 0), (pos[0], pos[1], size[0], size[1]), int(
                items.oneph*header_draw["header_line_thick"]*1.5))
            text = font.render(
                "connecting to RFID reader...", 1, SETUP["color"])
            win.blit(text, (pos[0]+(items.oneph*4), pos[1]+(items.oneph*4)))
            pygame.display.update()
            import serial
            conn = serial.Serial(SETUP["port"][OS], timeout=20)

            conn.write(b"con_start\n")
            answer = conn.readline()
            answer = answer[:len(answer)-len(b"\r\n")].decode("UTF-8")
            if answer == "Ready":

                conn.write(b"req_ID\n")
                answer = conn.readline()
                answer = answer[:len(answer)-len(b"\r\n")].decode("UTF-8")
                if answer == "req_ID-READ:START":
                    pygame.draw.rect(
                        win, SETUP['background'], (pos[0], pos[1], size[0], size[1]))
                    pygame.draw.rect(win, (0, 255, 0), (pos[0], pos[1], size[0], size[1]), int(
                        items.oneph*header_draw["header_line_thick"]*1.5))
                    text = font.render(
                        "Place Card on RFID reader...", 1, SETUP["color"])
                    win.blit(text, (pos[0]+(items.oneph*4),
                                    pos[1]+(items.oneph*4)))
                    pygame.display.update()
                    status = ""
                    answer = ""
                    while status != "SUCCESS":
                        answer = conn.readline()
                        print(answer)
                        if len(answer) > 0:
                            answer = answer[:len(
                                answer)-len(b"\r\n")].decode("UTF-8")
                            status = answer.split("-")[1].split(":")[0]
                            print(answer)
                            print(status)
                        if(status == "ERROR"):
                            print(answer)
                        elif len(answer) > 0:
                            id = answer.split("-")[1].split(":")[1].strip(" ")
                            print(id)
                            stats.add(select, id)
                            sleep(.5)
                            items.compile()
            conn.close()
        elif select['knob'] == 4 and select['buttons'] == 0 and select['selectors'][1] == 2 and SETUP["Serial"]:
            size = [int(winsize[0]//2), int(winsize[1]//5)]
            pos = [int((winsize[0]-size[0])//2), int((winsize[1]-size[1])//2)]
            pygame.draw.rect(win, SETUP['background'],
                             (pos[0], pos[1], size[0], size[1]))
            pygame.draw.rect(win, (0, 255, 0), (pos[0], pos[1], size[0], size[1]), int(
                items.oneph*header_draw["header_line_thick"]*1.5))
            text = font.render(
                "connecting to RFID reader...", 1, SETUP["color"])
            win.blit(text, (pos[0]+(items.oneph*4), pos[1]+(items.oneph*4)))
            pygame.display.update()
            print(select)
            import serial
            conn = serial.Serial(SETUP["port"][OS], timeout=20)

            conn.write(b"con_start\n")
            answer = conn.readline()
            print(answer)
            answer = answer[:len(answer)-len(b"\r\n")].decode("UTF-8")
            print(answer)
            # print("test1")
            if answer == "Ready":
                pygame.draw.rect(
                    win, SETUP['background'], (pos[0], pos[1], size[0], size[1]))
                pygame.draw.rect(win, (0, 255, 0), (pos[0], pos[1], size[0], size[1]), int(
                    items.oneph*header_draw["header_line_thick"]*1.5))
                text = font.render(
                    "Place Card on RFID reader...", 1, SETUP["color"])
                win.blit(text, (pos[0]+(items.oneph*4),
                                pos[1]+(items.oneph*4)))
                pygame.display.update()
                # print("test")

                conn.write(b"req_write\n")
                answer = conn.readline()
                answer = answer[:len(answer)-len(b"\r\n")].decode("UTF-8")
                print(answer)
                pygame.display.update()
                if answer == "req_write-WRITE:START":
                    id = (" "+stats.generateID()+"#").encode("UTF-8")
                    print(id)
                    conn.write(id)
                    answer = conn.readline()
                    print(answer)
                    answer = answer[:len(answer)-len(b"\r\n")].decode("UTF-8")
                    status = answer.split("-")[1].split(":")[0]
                    print(answer)

            conn.close()
        elif select['knob'] == 4 and select['buttons'] == 0 and select['selectors'][1] == 1 and SETUP["Serial"]:
            size = [int(winsize[0]//2), int(winsize[1]//5)]
            pos = [int((winsize[0]-size[0])//2), int((winsize[1]-size[1])//2)]
            pygame.draw.rect(win, SETUP['background'],
                             (pos[0], pos[1], size[0], size[1]))
            pygame.draw.rect(win, (0, 255, 0), (pos[0], pos[1], size[0], size[1]), int(
                items.oneph*header_draw["header_line_thick"]*1.5))
            text = font.render(
                "connecting to RFID reader...", 1, SETUP["color"])
            win.blit(text, (pos[0]+(items.oneph*4), pos[1]+(items.oneph*4)))
            pygame.display.update()

            print(select)
            import serial
            conn = serial.Serial(SETUP["port"][OS], timeout=20)

            conn.write(b"con_start\n")
            answer = conn.readline()
            print(answer)
            answer = answer[:len(answer)-len(b"\r\n")].decode("UTF-8")
            print(answer)
            print("test1")
            if answer == "Ready":
                print("test")

                conn.write(b"req_ID\n")
                answer = conn.readline()
                answer = answer[:len(answer)-len(b"\r\n")].decode("UTF-8")
                print(answer)
                if answer == "req_ID-READ:START":
                    pygame.draw.rect(
                        win, SETUP['background'], (pos[0], pos[1], size[0], size[1]))
                    pygame.draw.rect(win, (0, 255, 0), (pos[0], pos[1], size[0], size[1]), int(
                        items.oneph*header_draw["header_line_thick"]*1.5))
                    text = font.render(
                        "Place Card on RFID reader...", 1, SETUP["color"])
                    win.blit(text, (pos[0]+(items.oneph*4),
                                    pos[1]+(items.oneph*4)))
                    pygame.display.update()
                    status = ""
                    answer = ""
                    while status != "SUCCESS":
                        answer = conn.readline()
                        print(answer)
                        if len(answer) > 0:
                            answer = answer[:len(
                                answer)-len(b"\r\n")].decode("UTF-8")
                            status = answer.split("-")[1].split(":")[0]
                            print(answer)
                            print(status)
                        if(status == "ERROR"):
                            print(answer)
                        elif len(answer) > 0:
                            id = answer.split("-")[1].split(":")[1].strip(" ")
                            print(id)
                            stats.delete(select, id)
                            sleep(.5)
                            items.compile()
            conn.close()
        elif select['buttons'] == 1 and select['selectors'][1] == 0 and len(items.screenlist) > 0:
            items.consume(select)
            if select["wheel"] > len(items.screenlist)-2 and select["wheel"]-1 >= 0 and select["knob"] != 1:
                select["wheel"] -= 1
        elif select['buttons'] == 1 and select['selectors'][1] == 1 and select["knob"] == 1 and len(items.screenlist) > 0:
            items.consume(select, True)
            if select["wheel"] > len(items.screenlist)-2 and select["wheel"]-1 >= 0 and select["knob"] == 1:
                select["wheel"] -= 1
        elif select['buttons'] == 1 and select['selectors'][1] == 2 and select["knob"] == 1 and SETUP["Serial"]:
            size = [int(winsize[0]//2), int(winsize[1]//5)]
            pos = [int((winsize[0]-size[0])//2), int((winsize[1]-size[1])//2)]
            pygame.draw.rect(win, SETUP['background'],
                             (pos[0], pos[1], size[0], size[1]))
            pygame.draw.rect(win, (0, 255, 0), (pos[0], pos[1], size[0], size[1]), int(
                items.oneph*header_draw["header_line_thick"]*1.5))
            text = font.render(
                "connecting to RFID reader...", 1, SETUP["color"])
            win.blit(text, (pos[0]+(items.oneph*4), pos[1]+(items.oneph*4)))
            pygame.display.update()
            print(select)
            import serial
            conn = serial.Serial(SETUP["port"][OS], timeout=20)

            conn.write(b"con_start\n")
            answer = conn.readline()
            print(answer)
            answer = answer[:len(answer)-len(b"\r\n")].decode("UTF-8")
            print(answer)
            print("test1")
            if answer == "Ready":
                print("test")

                conn.write(b"req_ID\n")
                answer = conn.readline()
                answer = answer[:len(answer)-len(b"\r\n")].decode("UTF-8")
                print(answer)
                if answer == "req_ID-READ:START":
                    pygame.draw.rect(
                        win, SETUP['background'], (pos[0], pos[1], size[0], size[1]))
                    pygame.draw.rect(win, (0, 255, 0), (pos[0], pos[1], size[0], size[1]), int(
                        items.oneph*header_draw["header_line_thick"]*1.5))
                    text = font.render(
                        "Place Card on RFID reader...", 1, SETUP["color"])
                    win.blit(text, (pos[0]+(items.oneph*4),
                                    pos[1]+(items.oneph*4)))
                    pygame.display.update()
                    status = ""
                    answer = ""
                    while status != "SUCCESS":
                        answer = conn.readline()
                        if len(answer) > 0:
                            answer = answer[:len(
                                answer)-len(b"\r\n")].decode("UTF-8")
                            status = answer.split("-")[1].split(":")[0]
                            print(answer)
                            print(status)
                        if(status == "ERROR"):
                            print(answer)
                        elif len(answer) > 0:
                            id = answer.split("-")[1].split(":")[1].strip(" ")
                            print(answer)
                            items.add(id=id)
            conn.close()
        elif select['buttons'] == 1 and select['selectors'][1] == 1 and select["knob"] != 1 and SETUP["Serial"]:
            size = [int(winsize[0]//2), int(winsize[1]//5)]
            pos = [int((winsize[0]-size[0])//2), int((winsize[1]-size[1])//2)]
            pygame.draw.rect(win, SETUP['background'],
                             (pos[0], pos[1], size[0], size[1]))
            pygame.draw.rect(win, (0, 255, 0), (pos[0], pos[1], size[0], size[1]), int(
                items.oneph*header_draw["header_line_thick"]*1.5))
            text = font.render(
                "connecting to RFID reader...", 1, SETUP["color"])
            win.blit(text, (pos[0]+(items.oneph*4), pos[1]+(items.oneph*4)))
            pygame.display.update()
            print(select)
            import serial
            conn = serial.Serial(SETUP["port"][OS], timeout=20)

            conn.write(b"con_start\n")
            answer = conn.readline()
            print(answer)
            answer = answer[:len(answer)-len(b"\r\n")].decode("UTF-8")
            print(answer)
            print("test1")
            if answer == "Ready":
                print("test")

                conn.write(b"req_ID\n")
                answer = conn.readline()
                answer = answer[:len(answer)-len(b"\r\n")].decode("UTF-8")
                print(answer)
                if answer == "req_ID-READ:START":
                    pygame.draw.rect(
                        win, SETUP['background'], (pos[0], pos[1], size[0], size[1]))
                    pygame.draw.rect(win, (0, 255, 0), (pos[0], pos[1], size[0], size[1]), int(
                        items.oneph*header_draw["header_line_thick"]*1.5))
                    text = font.render(
                        "Place Card on RFID reader...", 1, SETUP["color"])
                    win.blit(text, (pos[0]+(items.oneph*4),
                                    pos[1]+(items.oneph*4)))
                    pygame.display.update()
                    answer = b""
                    status = ""
                    while status != "SUCCESS":
                        answer = conn.readline()
                        print(len(answer))
                        if len(answer) > 0:
                            print(answer)
                            print(len(answer))
                            answer = answer[:len(
                                answer)-len(b"\r\n")].decode("UTF-8")
                            status = answer.split("-")[1].split(":")[0]
                            print(answer)
                            print(status)
                        if(status == "ERROR"):
                            print(answer)
                        elif len(answer) > 0:
                            id = answer.split("-")[1].split(":")[1].strip(" ")
                            print(answer)
                            items.add(id=id)
            conn.close()
            # print(len(items.screenlist))
        elif SETUP["Serial"] == False:
            print("No Serial Connection possible")
        set += 1
    if keys[pygame.K_4]:
        select["knob"] = 0
    if keys[pygame.K_5]:
        select["knob"] = 1
    if keys[pygame.K_6]:
        select["knob"] = 2
    if keys[pygame.K_7]:
        select["knob"] = 3
    if keys[pygame.K_8]:
        select["knob"] = 4

    if select['buttons'] == 0:
        head.title = "STATS"
    if select['buttons'] == 1:
        head.title = "ITEMS"
    if select['buttons'] == 2:
        head.title = "DATA"
    # print(select)
    redraw()

pygame.quit()
