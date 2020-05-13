import pygame
import sys
import random
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1000,650))
pygame.display.set_caption("Radish Farm")
clock = pygame.time.Clock()

timer = 0
new_card = 0
system_pause = 0
last_card = 0
now_card = 0
action = 0

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
FONT = pygame.font.SysFont("arial",40) #字體
SIZE_CONSTANT = 2 #卡牌大小常數
CARD_SIZE = (int(63*SIZE_CONSTANT),int(88*SIZE_CONSTANT)) #卡牌的大小
GARDEN_SIZE = (250,200) #田的大小
PERIOD_SIZE = (int(GARDEN_SIZE[0]/15),10) 
BUTTON_SIZE = (100,60)
CARD_BACK = pygame.image.load("back.png").convert()
CARD_BACK = pygame.transform.scale(CARD_BACK,CARD_SIZE)
RADISH_PICTURE = pygame.image.load("radish.png").convert_alpha()
RADISH_PICTURE = pygame.transform.scale(RADISH_PICTURE,(CARD_SIZE[0]*5,CARD_SIZE[1]))
SPECIAL_CARD_PICTURE = pygame.image.load("special_card.png").convert_alpha()
SPECIAL_CARD_PICTURE = pygame.transform.scale(SPECIAL_CARD_PICTURE,(CARD_SIZE[0]*6,CARD_SIZE[1]))
opp1 = pygame.image.load("period1.png").convert_alpha()
opp2 = pygame.image.load("period2.png").convert_alpha()
opp1 = pygame.transform.scale(opp1,PERIOD_SIZE)
opp2 = pygame.transform.scale(opp2,PERIOD_SIZE)
PERIOD_PICTURE = [[]]
for i in range(1,6):
    PERIOD_PICTURE.append([])
    for j in range(i+1):
        PERIOD_PICTURE[i].append(pygame.Surface((PERIOD_SIZE[0]*i,PERIOD_SIZE[1])).convert())
        for k in range(j):
            PERIOD_PICTURE[i][j].blit(opp2,(PERIOD_SIZE[0]*k,0),(0,0,PERIOD_SIZE[0],PERIOD_SIZE[1]))
        for k in range(i-j):
            PERIOD_PICTURE[i][j].blit(opp1,(PERIOD_SIZE[0]*(k+j),0),(0,0,PERIOD_SIZE[0],PERIOD_SIZE[1]))

class Supply_station(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.picture = CARD_BACK
        self.situation = "show"
        self.position = position
        self.prepare = self.create_list()
        self.waste = []
        self.used_weather = []
    def create_list(self):
        primitive = []
        for i in range(5):
            primitive.append("櫻桃蘿蔔")
        for i in range(4):
            primitive.append("胡蘿蔔")
        for i in range(4):
            primitive.append("白蘿蔔")
        for i in range(3):
            primitive.append("藍蘿蔔")
        for i in range(3):
            primitive.append("甜菜根")
        for i in range(4):
            primitive.append("兔子")
        for i in range(3):
            primitive.append("柵欄")
        for i in range(3):
            primitive.append("澆水桶")
        for i in range(2):
            primitive.append("雜草")
        for i in range(3):
            primitive.append("蟲子")
        for i in range(2):
            primitive.append("殺蟲劑")
        # primitive.append("龍捲風")
        # primitive.append("播種季節")
        # primitive.append("蘿蔔大PK")
        # primitive.append("收成季節")
        # primitive.append("寒冬將近")
        return primitive
    def translate(self,name):
        if name == "櫻桃蘿蔔":
            return Cherry_radish(self.position)
        if name == "胡蘿蔔":
            return Carrot(self.position)
        if name == "白蘿蔔":
            return White_radish(self.position)
        if name == "藍蘿蔔":
            return Blue_radish(self.position)
        if name == "甜菜根":
            return Beet(self.position)
        if name == "兔子":
            return Rabbit(self.position)
        if name == "柵欄":
            return Fence(self.position)
        if name == "澆水桶":
            return Watering_can(self.position)
        if name == "雜草":
            return Weeds(self.position)
        if name == "蟲子":
            return Worm(self.position)
        if name == "殺蟲劑":
            return Insecticide(self.position)
        if name == "龍捲風":
            return Tornado(self.position)
        if name == "播種季節":
            return Spring(self.position)
        if name == "蘿蔔大PK":
            return Summer(self.position)
        if name == "收成季節":
            return Autumn(self.position)
        if name == "寒冬將近":
            return Winter(self.position)
        return name
    def next(self):
        if len(self.prepare) == 0:
            while len(self.waste) > 0:
                self.prepare.append(self.waste.pop())
        random.shuffle(self.prepare)
        n = self.prepare.pop()
        if type(n) == str:
            new_card = self.translate(n)
        else :
            new_card = n
        new_card.situation = "back"
        new_card.position = self.position
        all_sprite_list.add(new_card)
        return new_card
    def update(self):
        if self.situation == "show":
            screen.blit(self.picture,self.position)

class Pattern(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.money_button = Money_button((650,500))
        self.discard_button = Discard_button((780,500))
        self.ok_button = OK_button((780,580))
        self.station = Supply_station((800,250))
        all_sprite_list.add(self.money_button)
        all_sprite_list.add(self.discard_button)
        all_sprite_list.add(self.ok_button)
        all_sprite_list.add(self.station)
    def create_farmer(self,kind):
        if kind == "Player":
            new_farmer = Farmer()
            new_farmer.card_position = [(200,450),(350,450),(500,450)]
            new_farmer.garden = Garden((100,225))
            new_farmer.coin = Coin((650,580))
            new_farmer.harvest = Harvest((20,550))
            all_sprite_list.add(new_farmer.garden)
            all_sprite_list.add(new_farmer.coin)
            all_sprite_list.add(new_farmer.harvest)
            return new_farmer
        elif kind == "Computer":
            new_farmer = Farmer()
            new_farmer.card_position = [(200,20),(350,20),(500,20)]
            new_farmer.garden = Garden((400,225))
            new_farmer.coin = Coin((650,50))
            new_farmer.harvest = Harvest((20,50))
            all_sprite_list.add(new_farmer.garden)
            all_sprite_list.add(new_farmer.coin)
            all_sprite_list.add(new_farmer.harvest)
            return new_farmer

class Farmer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.situation = "遊戲開始"
        # self.score = 0
        self.card = [0,0,0] #手中的牌
        self.weeds = 0 #農場中的雜草數
        self.fence = 0 #農場中的柵欄數
        self.insecticide = 0 #農場中的殺蟲劑數
        self.waste = []
    def routine(self): #蘿蔔生長and收成
        # mature = []
        if self.weeds >= 1: #檢查是否有雜草
            self.weeds = self.weeds - 1
        else :
            for i in range(9):
                if self.garden.radishs[i] != 0:
                    self.garden.radishs[i].grow()
                    if self.garden.radishs[i].time == self.garden.radishs[i].period:
                        self.score.number = self.score.number + self.garden.radishs[i].score
                        if self.score.number < 0:
                            self.score.number = 0
                        self.coin.number = self.coin.number + self.garden.radishs[i].earn
                        if self.coin.number < 0:
                            self.coin.number = 0
                        self.harvest.number = self.harvest.number + 1
                        self.garden.radishs[i].clean()
                        self.waste.append(self.garden.radishs[i])
                        self.garden.radishs[i] = 0
    def plant(self,target,radish,place=0): #種植蘿蔔
        if target.garden.radishs[place] != 0:
            place = 0
        while target.garden.radishs[place] != 0:
            place = place + 1
        if place < 9:
            #將蘿蔔加入田中
            target.garden.radishs[place] = radish
            radish.position = target.garden.radish_position[place]
            #將蘿蔔卡從手中移除
            for i in range(3): 
                if self.card[i] == radish:
                    self.card[i] = 0
            self.coin.number = self.coin.number - radish.cost
            radish.situation = "radish"
    def need_card(self):
        for i in range(3):
            if self.card[i] == 0:
                return True
        return False
    def draw_card(self,new_card): #抽卡
        place = 0
        for i in range(2,-1,-1):
            if self.card[i] == 0:
                place = i
        self.card[place] = new_card
        self.card[place].position = self.card_position[place]
    def discard(self,c): #棄牌
        c.clean()
        place = self.card.index(c)
        self.waste.append(c)
        self.card[place] = 0
    def recycle(self,station): #將廢棄的牌回收
        while len(self.waste) > 0:
            station.waste.append(self.waste.pop())
    def take_money(self): #領錢
        print("金額加2")
        self.coin.number = self.coin.number + 2
    def use_Special_card(self,s_card,target): #使用功能卡
        self.coin.number = self.coin.number - s_card.cost
        s_card.use(target)
        self.discard(s_card)
    def attack(self,s_card,target,radish): #使用兔子or蟲子
        self.coin.number = self.coin.number - s_card.cost
        if s_card.name == "兔子":
            self.score.number = self.score.number + 1
        s_card.use(target,radish)
        self.discard(s_card)

class Player(Farmer):
    def __init__(self):
        Farmer.__init__(self)
        self.card_position = [(200,450),(350,450),(500,450)]
        self.coin = Coin((650,580))
        all_sprite_list.add(self.coin)
        self.garden = Garden((100,225))
        all_sprite_list.add(self.garden)
        self.money_button = Money_button((650,500))
        all_sprite_list.add(self.money_button)
        self.discard_button = Discard_button((780,500))
        all_sprite_list.add(self.discard_button)
        self.ok_button = OK_button((780,580))
        all_sprite_list.add(self.ok_button)
        self.harvest = Harvest((20,550))
        all_sprite_list.add(self.harvest)
        self.score = Score((20,470))
        all_sprite_list.add(self.score) 
        self.billboard = My_billboard((10,230))
        all_sprite_list.add(self.billboard) 
class Computer(Farmer):
    def __init__(self):
        Farmer.__init__(self)
        self.card_position = [(200,20),(350,20),(500,20)]
        self.coin = Coin((650,50))
        all_sprite_list.add(self.coin)
        self.garden = Garden((400,225))
        all_sprite_list.add(self.garden)
        self.harvest = Harvest((20,130))
        all_sprite_list.add(self.harvest)
        self.score = Score((20,40))
        all_sprite_list.add(self.score) 
        self.billboard = Opponent_billboard((650,230))
        all_sprite_list.add(self.billboard) 
    def Garden_is_empty(self):
        for i in self.garden.radishs:
            if i != 0:
                return False
        return True
    def Money_not_enough(self):
        for c in self.card:
            if c != 0:
                if c.cost <= self.coin.number:
                    return False
        return True
    def Radish_sum(self):
        total = 0
        for c in self.card:
            if c != 0:
                if c.sort == "radish":
                    total = total + 1
        return total
    def Special_card_sum(self):
        total = 0
        for c in self.card:
            if c != 0:
                if c.sort == "special_card":
                    total = total + 1
        return total
    def Card_can_use(self,c):
        if c == 0:
            return False
        if c.cost > self.coin.number:
            return False
        return True
    def Can_plant(self):
        if self.Radish_sum() > 0:
            for c in self.card:
                if c != 0:
                    if c.sort == "radish":
                        if c.cost <= self.coin.number:
                            return True
        return False
    def Can_use_special_card(self):
        if self.Special_card_sum() > 0:
            for c in self.card:
                if c != 0:
                    if c.sort == "special_card":
                        if c.cost <= self.coin.number:
                            return True
        return False

class Coin(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.position = position
        self.number = 2
        self.size = (50,50)
        self.picture = pygame.image.load("coin.png").convert_alpha()
        self.picture = pygame.transform.scale(self.picture,self.size)
        self.text = FONT.render("x5",True,WHITE,BLACK)
    def update(self):
        screen.blit(self.picture,self.position)
        self.text = FONT.render("X"+str(self.number),True,WHITE,BLACK)
        screen.blit(self.text,(self.position[0]+53,self.position[1]+5))

class Garden(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.position = position
        self.size = (250,200)
        self.radishs = [0,0,0,0,0,0,0,0,0]
        self.picture = pygame.image.load("farm.png").convert_alpha()
        self.picture = pygame.transform.scale(self.picture,self.size)
        self.radish_position = []
        for i in range(3):
            for j in range(3):
                self.radish_position.append((self.position[0]+int(self.size[0]/3)*j,self.position[1]+int(self.size[1]/3)*i))
    def Radish_sum(self):
        total = 0
        for r in self.radishs:
            if r != 0:
                total = total + 1
        return total
    def Calculate(self,name):
        total = 0
        for r in self.radishs:
            if r != 0:
                if r.name == name:
                    total = total + 1
        return total
        for i in range(3):
            for j in range(3):
                self.radish_position.append((self.position[0]+int(self.size[0]/3)*j,self.position[1]+int(self.size[1]/3)*i))
    def update(self):
        screen.blit(self.picture,self.position)

class Harvest(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.position = position
        self.number = 0
        self.size = (80,80)
        self.picture = pygame.image.load("harvest.png").convert_alpha()
        self.picture = pygame.transform.scale(self.picture,self.size)
        self.text = FONT.render("x0",True,WHITE,BLACK)
    def update(self):
        screen.blit(self.picture,self.position)
        self.text = FONT.render("X"+str(self.number),True,WHITE,BLACK)
        screen.blit(self.text,(self.position[0]+83,self.position[1]+35))

class Score(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.position = position
        self.number = 0
        self.size = (80,80)
        self.picture = pygame.image.load("score.png").convert_alpha()
        self.picture = pygame.transform.scale(self.picture,self.size)
        self.text = FONT.render("x0",True,WHITE,BLACK)
    def update(self):
        screen.blit(self.picture,self.position)
        self.text = FONT.render("X"+str(self.number),True,WHITE,BLACK)
        screen.blit(self.text,(self.position[0]+80,self.position[1]+30))

class Button(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.position = position
        self.size = BUTTON_SIZE
    def update(self):
        screen.blit(self.picture,self.position)
class OK_button(Button):
    def __init__(self,position):
        Button.__init__(self,position)
        self.picture = pygame.image.load("OK.png").convert_alpha()
        self.picture = pygame.transform.scale(self.picture,self.size)
class Discard_button(Button):
    def __init__(self,position):
        Button.__init__(self,position)
        self.picture = pygame.image.load("discard.png").convert_alpha()
        self.picture = pygame.transform.scale(self.picture,self.size)
class Money_button(Button):
    def __init__(self,position):
        Button.__init__(self,position)
        self.picture = pygame.image.load("take_money.png").convert_alpha()
        self.picture = pygame.transform.scale(self.picture,self.size)

class Billboard(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.position = position
        self.size = (80,85)
    def update(self):
        screen.blit(self.picture,self.position)
class My_billboard(Billboard):
    def __init__(self,position):
        Billboard.__init__(self,position)
        self.picture = pygame.image.load("billboard.png").convert_alpha()
        self.picture = pygame.transform.scale(self.picture,self.size)
class Opponent_billboard(Billboard):
    def __init__(self,position):
        Billboard.__init__(self,position)
        self.picture = pygame.image.load("billboard2.png").convert_alpha()
        self.picture = pygame.transform.scale(self.picture,self.size)

class Card(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.situation = "back"
        self.position = position
    def amplify(self):
        self.card_picture =  pygame.transform.scale(self.card_picture,(CARD_SIZE[0]+20,CARD_SIZE[1]+20))
        self.situation = "amplify"
    def narrow(self):
        self.card_picture = pygame.Surface(CARD_SIZE).convert()
        if self.sort == "radish":
            self.card_picture.blit(RADISH_PICTURE,(0,0),(CARD_SIZE[0]*self.origin_place,0,CARD_SIZE[0],CARD_SIZE[1]))
        elif self.sort == "special_card":
            self.card_picture.blit(SPECIAL_CARD_PICTURE,(0,0),(CARD_SIZE[0]*self.origin_place,0,CARD_SIZE[0],CARD_SIZE[1]))
        self.situation = "card"
    def update(self):
        if self.situation == "card":
            screen.blit(self.card_picture,self.position)
        elif self.situation == "amplify":
            # screen.blit(self.card_picture,self.position)
            screen.blit(self.card_picture,(self.position[0]-10,self.position[1]-10))
        elif self.situation == "back":
            screen.blit(CARD_BACK,self.position)
        elif self.situation == "radish":
            screen.blit(self.radish_picture,(self.position[0]+20,self.position[1]+10))
            screen.blit(self.period_picture,self.position)

class Radish(Card):
    def __init__(self,position):
        Card.__init__(self,position)
        self.sort = "radish"
        self.time = 0
    def grow(self):
        self.time = self.time + 1 
        self.period_picture = PERIOD_PICTURE[self.period][self.time] 
    def clean(self):
        self.situation = "hide"
        self.card_picture = pygame.transform.scale(self.card_picture,CARD_SIZE)
        self.time = 0
        self.period_picture = PERIOD_PICTURE[self.period][self.time]
class Cherry_radish(Radish):
    def __init__(self,position):
        Radish.__init__(self,position)
        self.name = "櫻桃蘿蔔"
        self.origin_place = 0
        self.card_picture = pygame.Surface(CARD_SIZE).convert()
        self.card_picture.blit(RADISH_PICTURE,(0,0),(CARD_SIZE[0]*self.origin_place,0,CARD_SIZE[0],CARD_SIZE[1]))
        self.radish_picture = pygame.image.load("cherry_radish.png").convert_alpha()
        self.radish_picture = pygame.transform.scale(self.radish_picture,(50,50))
        self.period_picture = PERIOD_PICTURE[1][0]
        self.period = 1
        self.cost = 0
        self.earn = 2
        self.score = 1
class Blue_radish(Radish):
    def __init__(self,position):
        Radish.__init__(self,position)
        self.name = "藍蘿蔔"
        self.origin_place = 1
        self.card_picture = pygame.Surface(CARD_SIZE).convert()
        self.card_picture.blit(RADISH_PICTURE,(0,0),(CARD_SIZE[0]*self.origin_place,0,CARD_SIZE[0],CARD_SIZE[1]))
        self.radish_picture = pygame.image.load("blue_radish.png").convert_alpha()
        self.radish_picture = pygame.transform.scale(self.radish_picture,(50,50))
        self.period_picture = PERIOD_PICTURE[2][0]
        self.period = 2
        self.cost = 1
        self.earn = -1
        self.score = -1
class Carrot(Radish):
    def __init__(self,position):
        Radish.__init__(self,position)
        self.name = "胡蘿蔔"
        self.origin_place = 2
        self.card_picture = pygame.Surface(CARD_SIZE).convert()
        self.card_picture.blit(RADISH_PICTURE,(0,0),(CARD_SIZE[0]*self.origin_place,0,CARD_SIZE[0],CARD_SIZE[1]))
        self.radish_picture = pygame.image.load("carrot.png").convert_alpha()
        self.radish_picture = pygame.transform.scale(self.radish_picture,(50,50))
        self.period_picture = PERIOD_PICTURE[2][0]
        self.period = 2
        self.cost = 1
        self.earn = 4
        self.score = 2
class White_radish(Radish):
    def __init__(self,position):
        Radish.__init__(self,position)
        self.name = "白蘿蔔"
        self.origin_place = 3
        self.card_picture = pygame.Surface(CARD_SIZE).convert()
        self.card_picture.blit(RADISH_PICTURE,(0,0),(CARD_SIZE[0]*self.origin_place,0,CARD_SIZE[0],CARD_SIZE[1]))
        self.radish_picture = pygame.image.load("white_radish.png").convert_alpha()
        self.radish_picture = pygame.transform.scale(self.radish_picture,(50,50))
        self.period_picture = PERIOD_PICTURE[3][0]
        self.period = 3
        self.cost = 2
        self.earn = 6
        self.score = 3
class Beet(Radish):
    def __init__(self,position):
        Radish.__init__(self,position)
        self.name = "甜菜根"
        self.origin_place = 4
        self.card_picture = pygame.Surface(CARD_SIZE).convert()
        self.card_picture.blit(RADISH_PICTURE,(0,0),(CARD_SIZE[0]*self.origin_place,0,CARD_SIZE[0],CARD_SIZE[1]))
        self.radish_picture = pygame.image.load("beet.png").convert_alpha()
        self.radish_picture = pygame.transform.scale(self.radish_picture,(50,50))
        self.period_picture = PERIOD_PICTURE[4][0]
        self.period = 4
        self.cost = 3
        self.earn = 8
        self.score = 4


class Special_card(Card):
    def __init__(self,position):
        Card.__init__(self,position)
        self.sort = "special_card"
        self.score = 0
    def clean(self):
        self.situation = "hide"
        self.card_picture = pygame.transform.scale(self.card_picture,CARD_SIZE)
class Watering_can(Special_card):
    def __init__(self,position):
        Special_card.__init__(self,position)
        self.name = "澆水桶"
        self.origin_place = 0
        self.cost = 2
        self.card_picture = pygame.Surface(CARD_SIZE).convert()
        self.card_picture.blit(SPECIAL_CARD_PICTURE,(0,0),(CARD_SIZE[0]*self.origin_place,0,CARD_SIZE[0],CARD_SIZE[1]))
    def use(self,target):
        target.routine()
class Weeds(Special_card):
    def __init__(self,position):
        Special_card.__init__(self,position)
        self.name = "雜草"
        self.origin_place = 1
        self.cost = 1
        self.card_picture = pygame.Surface(CARD_SIZE).convert()
        self.card_picture.blit(SPECIAL_CARD_PICTURE,(0,0),(CARD_SIZE[0]*self.origin_place,0,CARD_SIZE[0],CARD_SIZE[1]))
    def use(self,target):
        target.weeds = target.weeds + 1
class Rabbit(Special_card):
    def __init__(self,position):
        Special_card.__init__(self,position)
        self.name = "兔子"
        self.origin_place = 2
        self.cost = 3
        self.score = 1
        self.card_picture = pygame.Surface(CARD_SIZE).convert()
        self.card_picture.blit(SPECIAL_CARD_PICTURE,(0,0),(CARD_SIZE[0]*self.origin_place,0,CARD_SIZE[0],CARD_SIZE[1]))
    def use(self,target,radish):
        if target.fence >= 1:
            target.fence = target.fence - 1
        else :
            #拔掉蘿蔔
            radish.clean()
            i = target.garden.radishs.index(radish)
            target.waste.append(radish)
            target.garden.radishs[i] = 0
class Fence(Special_card):
    def __init__(self,position):
        Special_card.__init__(self,position)
        self.name = "柵欄"
        self.origin_place = 3
        self.cost = 2
        self.card_picture = pygame.Surface(CARD_SIZE).convert()
        self.card_picture.blit(SPECIAL_CARD_PICTURE,(0,0),(CARD_SIZE[0]*self.origin_place,0,CARD_SIZE[0],CARD_SIZE[1]))
    def use(self,target):
        target.fence = target.fence + 1
class Worm(Special_card):
    def __init__(self,position):
        Special_card.__init__(self,position)
        self.name = "蟲子"
        self.origin_place = 4
        self.cost = 2
        self.card_picture = pygame.Surface(CARD_SIZE).convert()
        self.card_picture.blit(SPECIAL_CARD_PICTURE,(0,0),(CARD_SIZE[0]*self.origin_place,0,CARD_SIZE[0],CARD_SIZE[1]))
    def use(self,target,radish):
        if target.insecticide >= 1:
            target.insecticide = target.insecticide - 1
        else :
            #拔掉蘿蔔
            radish.clean()
            i = target.garden.radishs.index(radish)
            target.waste.append(radish)
            target.garden.radishs[i] = 0
class Insecticide(Special_card):
    def __init__(self,position):
        Special_card.__init__(self,position)
        self.name = "殺蟲劑"
        self.origin_place = 5
        self.cost = 0
        self.score = -1
        self.card_picture = pygame.Surface(CARD_SIZE).convert()
        self.card_picture.blit(SPECIAL_CARD_PICTURE,(0,0),(CARD_SIZE[0]*self.origin_place,0,CARD_SIZE[0],CARD_SIZE[1]))
    def use(self,target):
        target.insecticide = target.insecticide + 1
        target.score.number = target.score.number + self.score 

class Weather(pygame.sprite.Sprite):
    def __init__(self,position):
        Card.__init__(self,position)
        self.sort = "weather"
        self.next_weather = "播種季節"
        self.order = ["播種季節","蘿蔔大PK","收成季節","寒冬將近"]
    def go_by(self,w_card):
        #刪除station中的天氣卡
        self.next_weather = self.order[self.order.index(w_card)+1]
    def update(self):
        if self.situation == "card":
            screen.blit(self.picture,self.position)
class Tornado(Weather):
    def __init__(self,position):
        Weather.__init__(self,position)
        self.name = "龍捲風"
        #self.picture = ???
    #def 所有人失去一個蘿蔔
class Spring(Weather):
    def __init__(self,position):
        Weather.__init__(self,position)
        self.name = "播種季節"
        #self.picture = ???
    #def 所有人免費種下手中所有的蘿蔔
class Summer(Weather):
    def __init__(self,position):
        Weather.__init__(self,position)
        self.name = "蘿蔔大PK"
        #self.picture = ???
    #def 比誰收成的蘿蔔最多
class Autumn(Weather):
    def __init__(self,position):
        Weather.__init__(self,position)
        self.name = "收成季節"
        #self.picture = ???
    #def 所有人收成所種的所有蘿蔔
class Winter(Weather):
    def __init__(self,position):
        Weather.__init__(self,position)
        self.name = "寒冬將近"
        #self.picture = ???
    #def 結束遊戲

def Mouse_in_range(mouse,position,size):
    if (position[0] <= mouse[0] and mouse[0] <= position[0]+size[0]) and (position[1] <= mouse[1] and mouse[1] <= position[1]+size[1]):
        return True
    return False
def Mouse_in_garden(mouse,garden_position):
    x = mouse[0] - garden_position[0]
    y = mouse[1] - garden_position[1]
    unit_x = GARDEN_SIZE[0]/3
    unit_y = GARDEN_SIZE[1]/3
    x = int(x/unit_x)
    y = int(y/unit_y)
    return y*3+x



all_sprite_list = pygame.sprite.Group()

station = Supply_station((800,250))
# pattern = Pattern() #
all_sprite_list.add(station)

me = Player()
opponent = Computer()

# me = pattern.create_farmer("Player")
# opponent = pattern.create_farmer("Computer")
# station = pattern.station

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if system_pause == 0:
            if me.situation == "行動":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    now_mouse = pygame.mouse.get_pos()
                    now_card = 0
                    #選擇出牌
                    if action == 0 or action == "use":
                        if last_card != 0:
                            last_card = me.card[int(last_card[-1])-1]
                            #金額充足
                            if last_card.cost <= me.coin.number:
                                #點選的是蘿蔔卡
                                if last_card.sort == "radish":
                                    #自己的田被點擊
                                    if Mouse_in_range(now_mouse,me.garden.position,me.garden.size):
                                        place = Mouse_in_garden(now_mouse,me.garden.position)
                                        me.plant(me,last_card,place)
                                        action = "use"
                                    #對方的田被點擊
                                    elif Mouse_in_range(now_mouse,opponent.garden.position,opponent.garden.size):
                                        place = Mouse_in_garden(now_mouse,opponent.garden.position)
                                        me.plant(opponent,last_card,place)
                                        action = "use"
                                #點選的是功能卡
                                elif last_card.sort == "special_card":
                                    #使用兔子or蟲子
                                    if last_card.name == "兔子" or last_card.name == "蟲子":
                                        #自己的田被點擊
                                        if Mouse_in_range(now_mouse,me.garden.position,me.garden.size):
                                            place = Mouse_in_garden(now_mouse,me.garden.position)
                                            if me.garden.radishs[place] != 0:
                                                me.attack(last_card,me,me.garden.radishs[place])
                                                action = "use"
                                        #對方的田被點擊
                                        elif Mouse_in_range(now_mouse,opponent.garden.position,opponent.garden.size):
                                            place = Mouse_in_garden(now_mouse,opponent.garden.position)
                                            if opponent.garden.radishs[place] != 0:
                                                me.attack(last_card,opponent,opponent.garden.radishs[place])
                                                action = "use"
                                    #使用澆水桶or雜草or柵欄or殺蟲劑
                                    else :
                                        #自己的田被點擊
                                        if Mouse_in_range(now_mouse,me.garden.position,me.garden.size):
                                            me.use_Special_card(last_card,me)
                                            action = "use"
                                        #對方的田被點擊
                                        elif Mouse_in_range(now_mouse,opponent.garden.position,opponent.garden.size):
                                            me.use_Special_card(last_card,opponent)
                                            action = "use"
                    #發牌機被點擊
                    if Mouse_in_range(now_mouse,station.position,CARD_SIZE):
                        me.situation = "抽牌"
                    #第一張牌被點擊
                    elif Mouse_in_range(now_mouse,me.card_position[0],CARD_SIZE): 
                        if me.card[0] != 0:
                            now_card = "card1"
                            if me.card[0].situation == "card":
                                me.card[0].amplify()
                            elif me.card[0].situation == "amplify":
                                me.card[0].narrow()
                    #第二張牌被點擊
                    elif Mouse_in_range(now_mouse,me.card_position[1],CARD_SIZE): 
                        if me.card[1] != 0:
                            now_card = "card2"
                            if me.card[1].situation == "card":
                                me.card[1].amplify()
                            elif me.card[1].situation == "amplify":
                                me.card[1].narrow()
                    #第三張牌被點擊
                    elif Mouse_in_range(now_mouse,me.card_position[2],CARD_SIZE): 
                        if me.card[2] != 0:
                            now_card = "card3"
                            if me.card[2].situation == "card":
                                me.card[2].amplify()
                            elif me.card[2].situation == "amplify":
                                me.card[2].narrow()
                    #按下"完成"按鈕
                    elif Mouse_in_range(now_mouse,me.ok_button.position,BUTTON_SIZE): 
                        me.situation = "抽牌"
                    #按下"領錢"按鈕
                    elif Mouse_in_range(now_mouse,me.money_button.position,BUTTON_SIZE): 
                        if action == 0:
                            me.coin.number = me.coin.number + 2
                            me.situation = "抽牌"
                    #按下"棄牌"按鈕
                    elif Mouse_in_range(now_mouse,me.discard_button.position,BUTTON_SIZE):
                        if action == 0 or action == "discard":
                            action = "discard"
                            for i in range(3):
                                if me.card[i] != 0:
                                    if me.card[i].situation == "amplify":
                                        me.discard(me.card[i])
                    #還原放大的卡片
                    for i in range(3):
                        if me.card[i] != 0:
                            if me.card[i].situation == "amplify" and now_card != "card"+str(i+1):
                                me.card[i].narrow()
                    last_card = now_card
    #狀態列
    if system_pause == 0:
        if me.situation == "遊戲開始":
            if new_card == 0:
                if me.need_card():
                    new_card  = station.next()
                    new_card.situation = "card"
                    timer = pygame.time.get_ticks()
                    system_pause = 1
        # if me.situation == "等待中":
        elif me.situation == "收成":
            me.routine()
            me.situation = "行動"
            action = 0
        elif me.situation == "抽牌":
            if new_card == 0:
                if me.need_card():
                    new_card  = station.next()
                    new_card.situation = "card"
                    timer = pygame.time.get_ticks()
                    system_pause = 1
                else :
                    me.situation = "清除廢牌"
        elif me.situation == "清除廢牌":
            me.recycle(station)
            me.situation = "等待中"
            opponent.situation = "收成"

        if opponent.situation == "遊戲開始":
            if new_card == 0:
                if opponent.need_card():
                    new_card  = station.next()
                    timer = pygame.time.get_ticks()
                    system_pause = 1
        # if opponent.situation == "等待中":
        elif opponent.situation == "收成":
            opponent.routine()
            opponent.situation = "行動"
            action = 0
        elif opponent.situation == "行動":
            #還未決定要如何行動
            if action == 0:
                #棄牌
                if opponent.Garden_is_empty() and opponent.Radish_sum == 0:
                    for i in range(3):
                        opponent.discard(opponent.card[i])
                    opponent.situation = "抽牌"
                #領錢
                elif opponent.Money_not_enough():
                    opponent.coin.number = opponent.coin.number + 2
                    opponent.situation = "抽牌"
                #出牌
                else :
                    action = "use"
            #決定要出牌
            if action == "use":
                #手中有蘿蔔,且可以種
                if opponent.Can_plant() :
                    #將可以種的蘿蔔的位置找出來
                    order = []
                    for i in range(3):
                        if opponent.Card_can_use(opponent.card[i]):
                            if opponent.card[i].sort == "radish":
                                order.append(i)
                    random.shuffle(order)
                    for c in order:
                        if opponent.card[c].cost <= opponent.coin.number:
                            #種在自己的田(不是藍蘿蔔)
                            if opponent.card[c].name != "藍蘿蔔":
                                opponent.plant(opponent,opponent.card[c])
                            #種在對手的田(藍蘿蔔)
                            else :
                                opponent.plant(me,opponent.card[c])
                    opponent.situation = "抽牌"
                #手中有功能卡,且可以用
                if opponent.Can_use_special_card() :
                    order = []
                    #將可以用的功能卡的位置找出來
                    for i in range(3):
                        if opponent.Card_can_use(opponent.card[i]):
                            if opponent.card[i].sort == "special_card":
                                order.append(i)
                    random.shuffle(order)
                    for c in order:
                        if opponent.card[c].cost <= opponent.coin.number:
                            if opponent.card[c].name == "兔子" or opponent.card[c].name == "蟲子":
                                #向對手使用
                                if me.garden.Radish_sum() - me.garden.Calculate("藍蘿蔔") > 0:
                                    sequence = [0,1,2,3,4,5,6,7,8]
                                    random.shuffle(sequence)
                                    for i in sequence:
                                        if me.garden.radishs[i] != 0:
                                            if me.garden.radishs[i].name != "藍蘿蔔":
                                                opponent.attack(opponent.card[c],me,me.garden.radishs[i])
                                                break
                                #向自己使用
                                elif opponent.garden.Calculate("藍蘿蔔") > 0:
                                    sequence = [0,1,2,3,4,5,6,7,8]
                                    random.shuffle(sequence)
                                    for i in sequence:
                                        if me.garden.radishs[i] != 0:
                                            if me.garden.radishs[i].name == "藍蘿蔔":

                                                opponent.attack(opponent.card[c],me,me.garden.radishs[i])
                            elif opponent.card[c].name == "澆水桶":
                                opponent.use_Special_card(opponent.card[c],opponent)
                            elif opponent.card[c].name == "雜草":
                                opponent.use_Special_card(opponent.card[c],me)
                            elif opponent.card[c].name == "柵欄":
                                opponent.use_Special_card(opponent.card[c],me)
                            elif opponent.card[c].name == "殺蟲劑":
                                opponent.use_Special_card(opponent.card[c],me)
                    if opponent.Radish_sum() + opponent.Special_card_sum() == 3:
                        #棄牌
                        for i in range(3):
                            opponent.discard(opponent.card[i])
                    opponent.situation = "抽牌"               

            opponent.situation = "抽牌"
        elif opponent.situation == "抽牌":
            if new_card == 0:
                if opponent.need_card():
                    new_card  = station.next()
                    timer = pygame.time.get_ticks()
                    system_pause = 1
                else :
                    opponent.situation = "清除廢牌"
        elif opponent.situation == "清除廢牌":
                opponent.recycle(station)
                opponent.situation = "等待中"
                me.situation = "收成"

    #有人在抽牌
    if system_pause == 1:
        if new_card != 0:
            if pygame.time.get_ticks() - timer >= 300:
                #我在抽牌
                if me.situation == "抽牌":
                    me.draw_card(new_card)
                    new_card = 0
                    system_pause = 0
                    if me.need_card():
                        new_card  = station.next()
                        new_card.situation = "card"
                        timer = pygame.time.get_ticks()
                        system_pause = 1
                    else :
                        me.situation = "清除廢牌"
                #對手在抽牌
                elif opponent.situation == "抽牌":
                    opponent.draw_card(new_card)
                    new_card = 0
                    system_pause = 0
                    if opponent.need_card():
                        new_card  = station.next()
                        timer = pygame.time.get_ticks()
                        system_pause = 1
                    else :
                        opponent.situation = "清除廢牌"
                #遊戲開始的抽牌
                elif me.situation == "遊戲開始":
                    me.draw_card(new_card)
                    new_card = 0
                    system_pause = 0
                    if me.need_card():
                        new_card  = station.next()
                        new_card.situation = "card"
                        timer = pygame.time.get_ticks()
                        system_pause = 1
                    else :
                        me.situation = "行動"
                elif opponent.situation == "遊戲開始":
                    opponent.draw_card(new_card)
                    new_card = 0
                    system_pause = 0
                    if opponent.need_card():
                        new_card  = station.next()
                        timer = pygame.time.get_ticks()
                        system_pause = 1
                    else :
                        opponent.situation = "等待中"
    #兔子出沒

    
    screen.fill(BLACK)
    all_sprite_list.update()
    pygame.display.update()
    clock.tick(60)
