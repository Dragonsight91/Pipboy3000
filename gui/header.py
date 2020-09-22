import pygame
from datetime import datetime
from random import randint


class head(object):
    def __init__(self, window, winsize, headerdraw, col, font, PLAYER, title='ITEMS'):
        self.onepw = winsize[0]/100
        self.oneph = winsize[1]/100
        self.winsize = winsize
        self.sizes = headerdraw
        PLAYER["HP"] = self.health = randint(0, PLAYER["maxHP"])
        PLAYER["AP"] = self.ap = randint(0, PLAYER["maxAP"])
        self.window = window
        self.col = col
        self.healthmax = PLAYER["maxHP"]
        self.apmax = PLAYER["maxAP"]
        self.font = font
        self.title = title
        self.player = PLAYER

    def update(self, select, SETUP, PLAYER={}):
        if len(PLAYER) > 0:
            self.player = PLAYER

        # title
        TITLE = self.font.render(self.title, 1, self.col, SETUP["background"])
        pygame.draw.line(self.window, self.col, (self.onepw*self.sizes["start_header_w"], self.oneph*self.sizes["start_header_h"]), (
            self.onepw*self.sizes['end_title'], self.oneph*self.sizes["start_header_h"]), int(self.oneph*self.sizes["header_line_thick"]))
        pygame.draw.line(self.window, self.col, (self.onepw*self.sizes['end_title'], self.oneph*self.sizes["start_header_h"]), (
            self.onepw*self.sizes['end_title'], self.onepw*self.sizes["end_header_h"]), int(self.oneph*self.sizes["header_line_thick"]))
        pygame.draw.line(self.window, self.col, (self.onepw*self.sizes["start_header_w"], self.oneph*self.sizes["start_header_h"]), (
            self.onepw*self.sizes["start_header_w"], self.onepw*self.sizes["end_header_h"]), int(self.oneph*self.sizes["header_line_thick"]))
        pygame.draw.rect(self.window, (0, 0, 0), (self.onepw*(self.sizes["start_header_w"]+3.5), self.oneph*(
            self.sizes["start_header_h"]-2.7), TITLE.get_width()+(self.onepw*2), TITLE.get_height()))
        self.window.blit(
            TITLE, (self.onepw*(self.sizes["start_header_w"]+4.5), self.oneph*(self.sizes["start_header_h"]-2.7)))

        # hp
        HP = self.font.render(
            str(self.player["HP"])+"/"+str(self.player["maxHP"])+" HP", 1, self.col)
        pygame.draw.line(self.window, self.col, (self.onepw*(self.sizes['end_title']+2), self.oneph*self.sizes["start_header_h"]), (self.onepw*(
            self.sizes['end_HP']), self.oneph*self.sizes["start_header_h"]), int(self.oneph*self.sizes["header_line_thick"]))
        pygame.draw.line(self.window, self.col, (self.onepw*(self.sizes['end_HP']), self.oneph*(self.sizes["start_header_h"])), (self.onepw*(
            self.sizes['end_HP']), self.onepw*self.sizes["end_header_h"]), int(self.oneph*self.sizes["header_line_thick"]))
        self.window.blit(HP, ((self.onepw*(self.sizes['end_HP']-0.5))-HP.get_width(
        ), self.oneph*(self.sizes["start_header_h"]+0.5)))

        # ap
        AP = self.font.render(
            str(self.player["AP"])+"/"+str(self.player["maxAP"])+" AP", 1, self.col)
        pygame.draw.line(self.window, self.col, (self.onepw*(self.sizes['end_HP']+2), self.oneph*self.sizes["start_header_h"]), (self.onepw*(
            self.sizes['end_AP']), self.oneph*self.sizes["start_header_h"]), int(self.oneph*self.sizes["header_line_thick"]))
        pygame.draw.line(self.window, self.col, (self.onepw*(self.sizes['end_AP']), self.oneph*(self.sizes["start_header_h"])), (self.onepw*(
            self.sizes['end_AP']), self.onepw*self.sizes["end_header_h"]), int(self.oneph*self.sizes["header_line_thick"]))
        self.window.blit(AP, ((self.onepw*(self.sizes['end_AP']-0.5))-AP.get_width(
        ), self.oneph*(self.sizes["start_header_h"]+0.5)))

        # xp/time
        TIME = self.font.render(
            str(datetime.now().strftime('%I:%M %p')), 1, self.col)
        pygame.draw.line(self.window, self.col, (self.onepw*(self.sizes['end_AP']+2), self.oneph*self.sizes["start_header_h"]), (self.onepw*(
            self.sizes['end_header_w']), self.oneph*self.sizes["start_header_h"]), int(self.oneph*self.sizes["header_line_thick"]))
        pygame.draw.line(self.window, self.col, (self.onepw*(self.sizes['end_header_w']), self.oneph*(self.sizes["start_header_h"])), (self.onepw*(
            self.sizes['end_header_w']), self.onepw*self.sizes["end_header_h"]), int(self.oneph*self.sizes["header_line_thick"]))
        self.window.blit(TIME, ((self.onepw*(self.sizes['end_header_w']-1))-TIME.get_width(
        ), self.oneph*(self.sizes["start_header_h"]+0.5)))

        # tabs
        pygame.draw.line(self.window, self.col, (self.onepw*self.sizes['start_header_w'], self.oneph*self.sizes['start_select']), (
            self.onepw*self.sizes['start_header_w'], self.oneph*self.sizes['end_select']), int(self.oneph*self.sizes["header_line_thick"]))
        pygame.draw.line(self.window, self.col, (self.onepw*self.sizes['end_header_w'], self.oneph*self.sizes['start_select']), (
            self.onepw*self.sizes['end_header_w'], self.oneph*self.sizes['end_select']), int(self.oneph*self.sizes["header_line_thick"]))
        pygame.draw.line(self.window, self.col, (self.onepw*self.sizes['start_header_w'], self.oneph*self.sizes['end_select']), (
            self.onepw*self.sizes['end_header_w'], self.oneph*self.sizes['end_select']), int(self.oneph*self.sizes["header_line_thick"]))

        tabs = []
        positioning = (
            (self.onepw*self.sizes['start_header_w'])-(self.onepw*self.sizes['start_header_w']))/10
        # Stats
        if select['buttons'] == 0:
            tabs.append([self.font.render("Status", 1, self.col), 0])
            tabs.append([self.font.render("S.P.E.C.I.A.L", 1, self.col), 0])
            tabs.append([self.font.render("Skills", 1, self.col), 0])
            tabs.append([self.font.render("Perks", 1, self.col), 0])
            tabs.append([self.font.render("General", 1, self.col), 0])
            tabs[0][1] = self.onepw*11
            tabs[1][1] = self.onepw*27.5
            tabs[2][1] = self.onepw*52.5
            tabs[3][1] = self.onepw*67.5
            tabs[4][1] = self.onepw*80
        # items
        if select['buttons'] == 1:
            tabs.append([self.font.render("Weapons", 1, self.col), 0])
            tabs.append([self.font.render("Apparel", 1, self.col), 0])
            tabs.append([self.font.render("Aid", 1, self.col), 0])
            tabs.append([self.font.render("Misc", 1, self.col), 0])
            tabs.append([self.font.render("Ammo", 1, self.col), 0])
            tabs[0][1] = self.onepw*12.5
            tabs[1][1] = self.onepw*32.5
            tabs[2][1] = self.onepw*52.5
            tabs[3][1] = self.onepw*67.5
            tabs[4][1] = self.onepw*82.5
        # data
        if select['buttons'] == 2:
            tabs.append([self.font.render("Local Map", 1, self.col), 0])
            tabs.append([self.font.render("World Map", 1, self.col), 0])
            tabs.append([self.font.render("Quests", 1, self.col), 0])
            tabs.append([self.font.render("Notes", 1, self.col), 0])
            tabs.append([self.font.render("Radio", 1, self.col), 0])
            tabs[0][1] = self.onepw*12.5
            tabs[1][1] = self.onepw*32.5
            tabs[2][1] = self.onepw*52.5
            tabs[3][1] = self.onepw*67.5
            tabs[4][1] = self.onepw*80.5

        for i in range(len(tabs)):
            if select['knob'] == i:
                pygame.draw.rect(self.window, (0, 35, 0, 1), (tabs[i][1]-self.onepw*1, (self.oneph*self.sizes['end_select']-5)-(
                    tabs[i][0].get_height()/2), tabs[i][0].get_width()+(self.onepw*2), tabs[i][0].get_height()+(self.oneph*0.5)))
                pygame.draw.rect(self.window, self.col, (tabs[i][1]-self.onepw*1, (self.oneph*self.sizes['end_select']-5)-(tabs[i][0].get_height(
                )/2), tabs[i][0].get_width()+(self.onepw*2), tabs[i][0].get_height()+(self.oneph*0.5)), int(self.oneph*self.sizes["header_line_thick"]))
            else:
                pygame.draw.rect(self.window, SETUP["background"], (tabs[i][1]-self.onepw*1, (self.oneph*self.sizes['end_select']-5)-(
                    tabs[i][0].get_height()/2), tabs[i][0].get_width()+(self.onepw*2), tabs[i][0].get_height()+(self.oneph*1)))
            self.window.blit(tabs[i][0], (tabs[i][1], (self.oneph *
                                                       self.sizes['end_select']-5)-(tabs[i][0].get_height()/2)))
