import pygame
import random
import serial


class items(object):
    def __init__(self, window, winsize, font, col, sizes, select, PLAYER, SETUP):
        self.onepw = winsize[0]/100
        self.oneph = winsize[1]/100
        self.window = window
        self.sel = [0, 10]
        self.font = font
        self.col = col
        self.sizes = sizes
        self.player = PLAYER
        self.select = select
        self.font2 = pygame.font.Font(SETUP['font'], int(
            ((winsize[0]/100)*self.sizes['text_h'])//1.4))
        rawIcons = {}
        for element in SETUP["icons"]:
            rawIcons[element] = [pygame.image.load(
                SETUP["icons"][element][0]), SETUP["icons"][element][1]]
        self.icons = rawIcons
        # print((self.icons)
        self.cycles = 0
        self.raw = []
        self.conf = []
        self.comp = []
        self.options = [["delete", "add item"],  # weapons
                        ["(un)equip", "delete item", "add item"],  # Apparel
                        ["use", "add item"],  # Aid
                        ["use", "add item"],  # Misc
                        ["use", "add item"]]  # Ammo
        self.opt = [15, 20]
        self.osel = 0

        f = open('gui/items.conf', 'r')
        self.conf = []
        for line in f:
            if line[0] != "#":
                ln = line.split(";")
                obj = {}
                # #print((ln)
                for elem in ln[0].split(","):
                    keyval = elem.split(":")
                    key = keyval[0]
                    val = keyval[1]
                    obj[key] = val
                keyval = ln[1].split(":")
                key = keyval[0]
                val = []
                if keyval[1] != "NONE\n":
                    for elem in keyval[1].split(","):
                        val.append(elem.strip("\n"))
                obj[key] = val
                self.conf.append(obj)
        # print((self.conf)

        f.close()
        self.conf = sorted(self.conf, key=lambda k: k['name'])
        self.compile()

    def update(self, select, conf, PLAYER):
        if len(PLAYER) > 0:
            self.player = PLAYER
        if len(conf) > 0:
            self.conf = conf
        if self.cycles > 0:
            self.cycles += 1
        if self.cycles > 5000:
            self.cycles = 0

        if self.cycles == 0:
            # self.add()
            # self.compile()
            self.cycles += 1
            f = open('gui/itemlist.comp', 'r')
            self.itemlist = []
            PLAYER["carrying"] = 0
            for line in f:
                if line[0] != "#":
                    if line[0] != "#":
                        ln = line.split(";")
                        obj = {}
                        for elem in ln[0].split(","):
                            keyval = elem.split(":")
                            key = keyval[0]
                            val = keyval[1]
                            obj[key] = val
                            if key == "weight":
                                PLAYER["carrying"] += int(val)
                        keyval = ln[1].split(":")
                        key = keyval[0]
                        val = []
                        if keyval[1] != "NONE\n":
                            for elem in keyval[1].split(","):
                                val.append(elem.strip("\n"))
                        obj[key] = val
                        self.itemlist.append(obj)
            # print((self.itemlist)
            # self.consume(select)
            f.close()
            self.itemlist = sorted(self.itemlist, key=lambda k: k['name'])
            self.visible = []
            if select['knob'] == 0:
                selected = "Weapons"
            if select['knob'] == 1:
                selected = "Apparel"
            if select['knob'] == 2:
                selected = "Aid"
            if select['knob'] == 3:
                selected = "Misc"
            if select['knob'] == 4:
                selected = "Ammo"
            for items in self.itemlist:
                if items['type'] == selected:
                    self.visible.append(items)
            # #print((self.itemlist,"\n\n\n\n\ntest\n")

        if select['knob'] == 0:
            selected = "Weapons"
            dmg = self.font.render("DAM", 1, self.col)
            self.window.blit(
                dmg, (self.onepw*(self.sizes['end_title']+2), self.oneph*55))
            pygame.draw.line(self.window, self.col, (self.onepw*(self.sizes['end_HP']+2), self.oneph*63), (
                self.onepw*self.sizes['end_header_w'], self.oneph*63), int(self.oneph*self.sizes["header_line_thick"]))
            pygame.draw.line(self.window, self.col, (self.onepw*self.sizes['end_header_w'], self.oneph*63), (
                self.onepw*self.sizes['end_header_w'], self.oneph*68), int(self.oneph*self.sizes["header_line_thick"]))

        if select['knob'] == 0 or select['knob'] == 1:
            # dam
            pygame.draw.line(self.window, self.col, (self.onepw*(self.sizes['end_title']+2), self.oneph*55), (self.onepw*(
                self.sizes['end_HP']), self.oneph*55), int(self.oneph*self.sizes["header_line_thick"]))
            pygame.draw.line(self.window, self.col, (self.onepw*(self.sizes['end_HP']), self.oneph*55), (self.onepw*(
                self.sizes['end_HP']), self.oneph*60), int(self.oneph*self.sizes["header_line_thick"]))
            # CND
            pygame.draw.line(self.window, self.col, (self.onepw*(self.sizes['end_title']+2), self.oneph*63), (self.onepw*(
                self.sizes['end_HP']), self.oneph*63), int(self.oneph*self.sizes["header_line_thick"]))
            pygame.draw.line(self.window, self.col, (self.onepw*(self.sizes['end_HP']), self.oneph*63), (self.onepw*(
                self.sizes['end_HP']), self.oneph*68), int(self.oneph*self.sizes["header_line_thick"]))
            # WG
            pygame.draw.line(self.window, self.col, (self.onepw*(self.sizes['end_HP']+2), self.oneph*55), (self.onepw*(
                self.sizes['end_AP']), self.oneph*55), int(self.oneph*self.sizes["header_line_thick"]))
            pygame.draw.line(self.window, self.col, (self.onepw*(self.sizes['end_AP']), self.oneph*55), (self.onepw*(
                self.sizes['end_AP']), self.oneph*60), int(self.oneph*self.sizes["header_line_thick"]))
            #
            pygame.draw.line(self.window, self.col, (self.onepw*(self.sizes['end_AP']+2), self.oneph*55), (
                self.onepw*self.sizes['end_header_w'], self.oneph*55), int(self.oneph*self.sizes["header_line_thick"]))
            pygame.draw.line(self.window, self.col, (self.onepw*self.sizes['end_header_w'], self.oneph*55), (
                self.onepw*self.sizes['end_header_w'], self.oneph*60), int(self.oneph*self.sizes["header_line_thick"]))
            cnd = self.font.render("CND", 1, self.col)
            wg = self.font.render("WG", 1, self.col)
            val = self.font.render("VAL", 1, self.col)
            self.window.blit(
                cnd, (self.onepw*(self.sizes['end_title']+2), self.oneph*63))
            self.window.blit(
                wg, (self.onepw*(self.sizes['end_HP']+2), self.oneph*55))
            self.window.blit(
                val, (self.onepw*(self.sizes['end_AP']+2), self.oneph*55))
            pygame.draw.rect(self.window, (0, 30, 0, 1), (self.onepw*(
                self.sizes['end_title']+7), self.oneph*64.5, self.onepw*9, self.oneph*3.4))

        if select['knob'] == 1:
            selected = "Apparel"
            damred = self.font.render("DR", 1, self.col)
            self.window.blit(
                damred, (self.onepw*(self.sizes['end_title']+2), self.oneph*55))
        if select['knob'] == 2:
            selected = "Aid"
            effects = self.font.render("EFFECTS", 1, self.col)
            self.window.blit(
                effects, (self.onepw*(self.sizes['end_title']+2), self.oneph*65.5))
            # WG
            wg = self.font.render("WG", 1, self.col)
            self.window.blit(
                wg, (self.onepw*(self.sizes['end_HP']+2), self.oneph*55))
            pygame.draw.line(self.window, self.col, (self.onepw*(self.sizes['end_HP']+2), self.oneph*55), (self.onepw*(
                self.sizes['end_AP']), self.oneph*55), int(self.oneph*self.sizes["header_line_thick"]))
            pygame.draw.line(self.window, self.col, (self.onepw*(self.sizes['end_AP']), self.oneph*55), (self.onepw*(
                self.sizes['end_AP']), self.oneph*60), int(self.oneph*self.sizes["header_line_thick"]))
            # Val
            val = self.font.render("VAL", 1, self.col)
            self.window.blit(
                val, (self.onepw*(self.sizes['end_AP']+2), self.oneph*55))
            pygame.draw.line(self.window, self.col, (self.onepw*(self.sizes['end_AP']+2), self.oneph*55), (
                self.onepw*self.sizes['end_header_w'], self.oneph*55), int(self.oneph*self.sizes["header_line_thick"]))
            pygame.draw.line(self.window, self.col, (self.onepw*self.sizes['end_header_w'], self.oneph*55), (
                self.onepw*self.sizes['end_header_w'], self.oneph*60), int(self.oneph*self.sizes["header_line_thick"]))
            # Effects
            pygame.draw.line(self.window, self.col, (self.onepw*(self.sizes['end_title']+2), self.oneph*64.9), (
                self.onepw*self.sizes['end_header_w'], self.oneph*64.9), int(self.oneph*self.sizes["header_line_thick"]))
            pygame.draw.line(self.window, self.col, (self.onepw*self.sizes['end_header_w'], self.oneph*64.9), (
                self.onepw*self.sizes['end_header_w'], self.oneph*70), int(self.oneph*self.sizes["header_line_thick"]))
        if select['knob'] == 3:
            selected = "Misc"
        if select['knob'] == 4:
            selected = "Ammo"

        # options
        pos = (15, 21, 27, 32)
        num = self.font2.render("WG "+str(self.player["carrying"])+"/"+str(
            (self.player["STR"]["base"]+self.player["STR"]["amount"]+self.player["STR"]["armor"])*self.player["STR"]["multiplier"]), 1, self.col)
        for index, items in enumerate(self.options[select["knob"]]):
            thing = self.font.render(str(items), 1, self.col)
            if index == select['selectors'][1]:
                pygame.draw.rect(self.window, (0, 50, 0, 1), (self.onepw*(self.sizes['end_AP']+5), self.oneph*(
                    pos[index]-0.15), self.onepw*16, thing.get_height()+(self.oneph*0.5)))
                pygame.draw.rect(self.window, self.col, (self.onepw*(self.sizes['end_AP']+5), self.oneph*(
                    pos[index]-0.15), self.onepw*16, thing.get_height()+(self.oneph*0.5)), int(self.oneph*self.sizes["header_line_thick"]))
            self.window.blit(
                thing, (self.onepw*(self.sizes['end_AP']+5.5), self.oneph*pos[index]))
        self.window.blit(num, ((self.onepw*(self.sizes['end_title']-1))-num.get_width(
        ), self.oneph*(self.sizes['start_header_h']+2)))
        itempos = [15.4, 22.8, 29.8, 36.8, 43.8, 50.8, 57.9, 64.9, 71.9, 79]
        n = 0
        self.visible = []
        for items in self.itemlist:
            if items['type'] == selected:
                self.visible.append(items)
        self.screenlist = self.visible[self.sel[0]:self.sel[1]]
        # #print((len(self.screenlist))
        for index, items in enumerate(self.screenlist):
            thing = self.font.render(str(items['name']), 1, self.col)
            if select['wheel'] == index:
                if selected == "Apparel":
                    try:
                        img = self.icons[items['name']]
                        surf = pygame.transform.smoothscale(
                            img[0], (int(self.onepw*img[1][0]), int(self.oneph*img[1][1])))
                        self.window.blit(
                            surf, (self.onepw*(self.sizes['end_AP'])-surf.get_width(), self.oneph*15))
                    except Exception as e:
                        pass
                if selected == "Weapons":
                    try:
                        img = self.icons[items['name']]
                        surf = pygame.transform.smoothscale(
                            img[0], (int(self.onepw*img[1][0]), int(self.oneph*img[1][1])))
                        self.window.blit(
                            surf, (self.onepw*(self.sizes['end_AP'])-surf.get_width(), self.oneph*15))
                    except Exception as e:
                        pass
                pygame.draw.rect(self.window, (0, 30, 0, 1), (self.onepw*(self.sizes['start_header_w']+1), self.oneph*(
                    itempos[index]-0.5), (self.onepw*self.sizes['end_title'])-(self.onepw*(self.sizes['start_header_w']+1)), thing.get_height()+(self.oneph*1)))
                pygame.draw.rect(self.window, self.col, (self.onepw*(self.sizes['start_header_w']+1), self.oneph*(itempos[index]-0.5), (self.onepw*self.sizes['end_title'])-(
                    self.onepw*(self.sizes['start_header_w']+1)), thing.get_height()+(self.oneph*1)), int(self.oneph*(self.sizes['header_line_thick'])))

                if selected == "Weapons" or selected == "Apparel":
                    # display stuff that is specific to weapons XOR apparel
                    if selected == "Weapons":
                        dam = self.font.render(items['dmg'], 1, self.col)
                        self.window.blit(
                            dam, (self.onepw*(self.sizes['end_HP']-2)-dam.get_width(), self.oneph*55))
                        ammo = self.font.render(items['ammotype'], 1, self.col)
                        self.window.blit(
                            ammo, (self.onepw*(self.sizes['end_HP']+2.5), self.oneph*63.25))
                    if selected == "Apparel":
                        dam = self.font.render(items['dmg'], 1, self.col)
                        self.window.blit(
                            dam, (self.onepw*(self.sizes['end_HP']-2)-dam.get_width(), self.oneph*55))

                    # display stuff that is specific to weapons OR apparel
                    wg = self.font.render(str(items['weight']), 1, self.col)
                    self.window.blit(
                        wg, (self.onepw*(self.sizes['end_AP']-2)-wg.get_width(), self.oneph*55))
                    val = self.font.render(str(items['value']), 1, self.col)
                    self.window.blit(
                        val, (self.onepw*(self.sizes['end_header_w']-2)-val.get_width(), self.oneph*55))
                    cnd = (self.onepw*9)/100
                    pygame.draw.rect(self.window, self.col, (self.onepw*(
                        self.sizes['end_title']+7), self.oneph*64.5, cnd*int(items['cnd']), self.oneph*3.4))

                    # Stuff Specific to Aid
                elif selected == "Aid":
                    try:
                        img = self.icons[items['name']]
                        surf = pygame.transform.smoothscale(
                            img[0], (int(self.onepw*img[1][0]), int(self.oneph*img[1][1])))
                        self.window.blit(
                            surf, (self.onepw*(self.sizes['end_AP'])-surf.get_width(), self.oneph*15))
                    except Exception as e:
                        pass
                    wg = self.font.render(str(items['weight']), 1, self.col)
                    self.window.blit(
                        wg, (self.onepw*(self.sizes['end_AP']-2)-wg.get_width(), self.oneph*55))
                    val = self.font.render(str(items['value']), 1, self.col)
                    self.window.blit(
                        val, (self.onepw*(self.sizes['end_header_w']-2)-val.get_width(), self.oneph*55))
                    FX = []
                    line = []
                    fxlist = ["RES", "STR", "HP",
                              "RAD", "AP", "CH", "IN", "DAM"]
                    n = 0
                    for name in fxlist:
                        effect = {}
                        value = items[name]
                        effect = {name: value}
                        if int(value.split(" ")[0]) != 0:
                            FX.append(effect)

                    ls = ""
                    for effect in FX:
                        for key in effect:
                            if int(effect[key].split(" ")[0]) > 0:
                                if len(effect[key].split(" ")) == 1:
                                    ls += str(key+" "+"+"+effect[key]+", ")
                                elif len(effect[key].split(" ")) > 1:
                                    percent = effect[key].split(" ")
                                    ls += str(percent[1]+" "+key +
                                              " "+"+"+percent[0]+"% "+", ")
                            elif int(effect[key].split(" ")[0]) < 0:
                                ls += str(key+" "+effect[key]+", ")

                    ls = ls[0:len(ls)-2]
                    list = self.font.render(ls, 1, self.col)
                    self.window.blit(
                        list, (self.onepw*(self.sizes['end_header_w']-1)-list.get_width(), self.oneph*65.5))

                elif selected == "Misc":
                    pass
                    # fill code and design for Misc here
                elif selected == "Ammo":
                    pass
                    # fill code and design for Ammo here

            if eval(items['multiple']):
                otherthing = self.font.render(
                    "("+str(items['number'])+")", 1, self.col)
                self.window.blit(otherthing, ((self.onepw*(self.sizes['end_title']-0.5))-(
                    otherthing.get_width()), self.oneph*itempos[index]))

            # Armor equip status
            if selected == "Apparel":
                self.window.blit(
                    thing, (self.onepw*(self.sizes['start_header_w']+4.5), self.oneph*itempos[index]))
                pygame.draw.rect(
                    self.window,
                    self.col, (
                        self.onepw *
                        (self.sizes['start_header_w']+1.5),
                        (self.oneph*itempos[index]) +
                        (thing.get_height()-self.onepw*2)/2,
                        self.onepw*2,
                        self.onepw*2
                    ),
                    int(self.onepw*self.sizes["header_line_thick"]//1.5)
                )
                # #print((PLAYER["equipped"]["armor"] and PLAYER["equipped"]["items"]["armor"]==items["idlist"][0])
                if (PLAYER["equipped"]["armor"] and PLAYER["equipped"]["items"]["armor"] == items["idlist"][0]) or (PLAYER["equipped"]["helmet"] and PLAYER["equipped"]["items"]["helmet"] == items["idlist"][0]):
                    pygame.draw.rect(
                        self.window,
                        self.col, (
                            self.onepw *
                            (self.sizes['start_header_w']+1.5),
                            (self.oneph*itempos[index]) +
                            (thing.get_height()-self.onepw*2)/2,
                            self.onepw*2,
                            self.onepw*2
                        )
                    )
            else:
                self.window.blit(
                    thing, (self.onepw*(self.sizes['start_header_w']+1.5), self.oneph*itempos[index]))
        return PLAYER

    def compile(self):
        file1 = open("gui/itemlist.comp", "w")
        file3 = open("gui/items.raw", "r")

        self.raw = []
        for lines in file3:
            self.raw.append(str(lines).strip("\n"))
        self.comp = []
        # print((self.conf)
        for id in self.raw:
            # print((id)
            for element in self.conf:
                elem = {}
                for stuff in element["idlist"]:
                    if id == stuff:
                        # print((element)
                        if eval(element["multiple"]):

                            found = False
                            for thing in self.comp:
                                if element["name"] == thing["name"]:
                                    # print(("test1")
                                    # print((thing["name"])
                                    thing["number"] += 1
                                    found = True
                                    thing["idlist"].append(id)
                            if found == False:
                                elem = element.copy()
                                # print((elem)
                                elem.pop("idlist")
                                elem["number"] = 1
                                elem["cnd"] = 100
                                elem["idlist"] = [id]
                                self.comp.append(elem)
                        else:
                            elem = element.copy()
                            # print((elem)
                            elem.pop("idlist")
                            elem["cnd"] = random.randint(0, 100)
                            elem["idlist"] = [id]
                            self.comp.append(elem)
        # print((self.comp)
        lines = []
        for obj in self.comp:
            string = ""

            for key in obj:
                if key != "idlist":
                    string += key+":"+str(obj[key])+","
            string = string[0:len(string)-1]
            string += ";idlist:"
            for id in obj["idlist"]:
                string += id+","
            string = string[0:len(string)-1]
            # print((string)
            lines.append(string+"\n")

        for string in lines:
            file1.write(string)
            # print((string)

        file1.close()
        file3.close()

    def add(self, id=""):
        file3 = open("gui/items.raw", "r")
        self.raw = []
        for lines in file3:
            self.raw.append(str(lines).strip("\n"))
        # print((self.raw)
        file3.close()

        # if id=="":
        #     id = input("enter IDs (separated by ','): ")

        if id != "exit" and id != "":
            idlist = id.split(",")
            for element in idlist:
                try:
                    self.raw.index(element)
                except Exception as e:
                    if type(e) == type(ValueError()):
                        self.raw.append(element)
            file = open("gui/items.raw", "w")
            for element in self.raw:
                file.write(element+"\n")
            file.close()
            self.compile()
            self.cycles = 0

    def consume(self, select, armordel=False):
        if select["knob"] == 2 or select["knob"] == 0 or (select["knob"] == 1 and armordel):
            file3 = open("gui/items.raw", "r")
            self.raw = []
            for lines in file3:
                self.raw.append(str(lines).strip("\n"))
            # print((self.raw)
            file3.close()
            if(len(self.itemlist) > 0):
                item = self.visible[self.sel[0]+select["wheel"]]
                # consuming and deleting consumables and weapons
                id = self.visible[self.sel[0]+select["wheel"]]["idlist"][len(
                    self.visible[self.sel[0]+select["wheel"]]["idlist"])-1]
                ix = 0
                for index, element in enumerate(self.itemlist):
                    elemID = element["idlist"][len(element["idlist"])-1]
                    if elemID == id:
                        element["idlist"].pop(len(element["idlist"])-1)
                        ix = index

                # self.itemlist[self.sel[0]+select["wheel"]]["idlist"] =self.itemlist[self.sel[0]+select["wheel"]]["idlist"][0:len(self.itemlist[self.sel[0]+select["wheel"]]["idlist"])-1]
                # print((self.itemlist[self.sel[0]+select["wheel"]]["idlist"])
                # print((id)
                if(eval(self.itemlist[ix]["multiple"])):
                    self.itemlist[ix]["number"] = int(
                        self.itemlist[ix]["number"])-1
                    item = self.itemlist[ix]
                    if item["type"] == "Aid":
                        self.player["HP"] += int(item["HP"])
                        self.player["AP"] += int(item["AP"])
                        self.player["RAD"] += int(item["RAD"])

                        if int(item["STR"]) > 0:
                            self.player["STR"]["amount"] += int(item["STR"])
                            # set Timeouts
                            self.player["STR"]["timeout"] = 100000
                        if int(item["IN"]) > 0:
                            self.player["IN"]["amount"] += int(item["IN"])
                            self.player["IN"]["timeout"] = 100000
                        if int(item["CH"]) > 0:
                            self.player["CH"]["timeout"] = 100000
                            self.player["CH"]["amount"] += int(item["IN"])
                    # self.itemlist[self.sel[0]+select["wheel"]]["number"]
                if(len(self.itemlist[ix]["idlist"]) == 0):
                    self.itemlist.pop(ix)

                # print((len(self.itemlist))
                # print((self.raw)
                self.raw.remove(id)
                # print((self.raw)
                file = open("gui/items.raw", "w")
                for element in self.raw:
                    file.write(element+"\n")
            file.close()
        elif select["knob"] == 1 and armordel == False:
            # Armor (un)equipping with a thousand unnecessary tests to make sure we only delete or add what is meant to be deleted or added
            item = self.visible[self.sel[0]+select["wheel"]]
            if self.player["equipped"]["armor"] and item["armortype"] == "ARMOR" and self.player["equipped"]["items"]["armor"] == item["idlist"][0]:
                self.player["equipped"]["armor"] = False
                self.player["equipped"]["items"]["armor"] = ""
                self.player["STR"]["armor"] = 0
            elif self.player["equipped"]["helmet"] == True and item["armortype"] == "HELMET" and self.player["equipped"]["items"]["helmet"] == item["idlist"][0]:
                self.player["equipped"]["helmet"] = False
                self.player["equipped"]["items"]["helmet"] = ""
            elif self.player["equipped"]["armor"] and item["armortype"] == "ARMOR" and self.player["equipped"]["items"]["armor"] != item["idlist"][0]:
                self.player["equipped"]["armor"] = True
                self.player["equipped"]["items"]["armor"] = item["idlist"][0]
                self.player["STR"]["armor"] = int(item["STR"])
            elif self.player["equipped"]["helmet"] == True and item["armortype"] == "HELMET" and self.player["equipped"]["items"]["helmet"] != item["idlist"][0]:
                self.player["equipped"]["helmet"] = True
                self.player["equipped"]["items"]["helmet"] = item["idlist"][0]
            elif self.player["equipped"]["armor"] == False and item["armortype"] == "ARMOR" and self.player["equipped"]["items"]["armor"] == "":
                self.player["equipped"]["armor"] = True
                self.player["equipped"]["items"]["armor"] = item["idlist"][0]
                self.player["STR"]["armor"] = int(item["STR"])
            elif self.player["equipped"]["helmet"] == False and item["armortype"] == "HELMET" and self.player["equipped"]["items"]["helmet"] == "":
                self.player["equipped"]["helmet"] = True
                self.player["equipped"]["items"]["helmet"] = item["idlist"][0]
        self.rewrite()
        self.cycles = 0

    def rewrite(self):
        file1 = open("gui/itemlist.comp", "w")
        lines = []
        for obj in self.itemlist:
            string = ""

            for key in obj:
                if key != "idlist":
                    string += key+":"+str(obj[key])+","
            string = string[0:len(string)-1]
            string += ";idlist:"
            for id in obj["idlist"]:
                string += id+","
            string = string[0:len(string)-1]
            # print((string)
            lines.append(string+"\n")

        for string in lines:
            file1.write(string)
            # print((string)
        file1.close()
