import pygame
import sys
import random
from pygame.locals import *

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
SIZE_CONSTANT = 2
CARD_SIZE = (int(63*SIZE_CONSTANT),int(88*SIZE_CONSTANT))
pygame.init()
screen = pygame.display.set_mode((1000,650))
pygame.display.set_caption("Radish Farm")
clock = pygame.time.Clock()


class Supply_station(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.picture = pygame.image.load("back.png").convert()
        self.picture = pygame.transform.scale(self.picture,CARD_SIZE)
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
        primitive.append("龍捲風")
        primitive.append("播種季節")
        primitive.append("蘿蔔大PK")
        primitive.append("收成季節")
        primitive.append("寒冬將近")
        return primitive
    def translate(self,card):
        if card == "櫻桃蘿蔔":
            return Cherry_radish(self.position)
        if card == "胡蘿蔔":
            return Carrot(self.position)
        if card == "白蘿蔔":
            return White_radish(self.position)
        if card == "藍蘿蔔":
            return Blue_radish(self.position)
        if card == "甜菜根":
            return Beet(self.position)
        if card == "兔子":
            return Rabbit(self.position)
        if card == "柵欄":
            return Fence(self.position)
        if card == "澆水桶":
            return Watering_can(self.position)
        if card == "雜草":
            return Weeds(self.position)
        if card == "蟲子":
            return Worm(self.position)
        if card == "殺蟲劑":
            return Insecticide(self.position)
        if card == "龍捲風":
            return Tornado(self.position)
        if card == "播種季節":
            return Spring(self.position)
        if card == "蘿蔔大PK":
            return Summer(self.position)
        if card == "收成季節":
            return Autumn(self.position)
        if card == "寒冬將近":
            return Winter(self.position)
    def next(self):
        random.shuffle(self.prepare)
        n = self.prepare.pop()
        if len(self.prepare) == 0:
            while len(self.waste) > 0:
                self.prepare.append(self.waste.pop())
        return self.translate(n)
    def update(self):
        if self.situation == "show":
            screen.blit(self.picture,self.position)

class Farmer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.money = 5 #------不確定多少錢
        self.card = [] #手中的牌
        self.garden = [] #目前正在種植的蘿蔔
        self.product = 0 #已收成數
        self.weeds = 0 #農場中的雜草數
        self.fence = 0 #農場中的柵欄數
        self.insecticide = 0 #農場中的殺蟲劑數
        self.waste = []
    def data(self): #印出各項數值
        print("分數:%d" %self.score)
        print("錢:%d" %self.money)
        print("收成數:%d" %self.product)
        print("雜草數:%d" %self.weeds)
        print("柵欄數:%d" %self.fence)
        print("殺蟲劑數:%d" %self.insecticide)
        print("手中的牌:",end="")
        for i in self.card:
            print(i.name,end=" ")
        print()
        print("目前正在種植的蘿蔔:")
        for i in self.garden:
            print(i.name,end=" ")
        print()
    def routine(self): #蘿蔔生長and收成
        mature = []
        if self.weeds >= 1:
            self.weeds = self.weeds - 1
        else :
            for p in self.garden:
                p.grow()
                if p.time == p.period:
                    mature.append(p)
            for p in mature:
                print(p.name+"收成")
                print("金額加%d" %p.earn)
                print("分數加%d" %p.score)
                self.score = self.score + p.score
                self.money = self.money + p.earn
                self.product = self.product + 1
                p.clean()
                self.waste.append(p)
                self.garden.remove(p)
    def plant(self,target,radish): #種植蘿蔔
        if self.money >= radish.cost :
            target.garden.append(radish)
            self.card.remove(radish)
            self.money = self.money - radish.cost
            radish.situation = "grow"
            print(radish.name+"種植成功 "+"剩下%d元" %self.money)
        else :
            print("金額不足")
    def draw_card(self,station): #抽卡
        while len(self.card) < 3:
            new_card = station.next()
            self.card.append(new_card)
        print("手中有",end="")
        for i in self.card:
            print(" "+i.name,end="")
        print()
    def discard(self,c): #棄牌
        print("棄置"+c.name)
        self.card.remove(c)
        self.waste.append(c)
    def recycle(self,station): #將廢棄的牌回收
        while len(self.waste) > 0:
            station.waste.append(self.waste.pop())
    def take_money(self): #領錢
        print("金額加2")
        self.money = self.money + 2
    def use_Special_card(self,s_card,target,radish=0): #使用功能卡(兔子,蟲子需指定蘿蔔)
        if self.money >= s_card.cost:
            self.money = self.money - s_card.cost
            print("使用"+s_card.name)
            if radish == 0:
                s_card.use(target)
                self.discard(s_card)
            else :
                if s_card.name == "兔子":
                    s_card.use(self,target,radish)
                if s_card.name == "蟲子":
                    s_card.use(target,radish)
                self.discard(s_card)
        else :
            print("金額不足")

class Radish(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.radish_picture = pygame.image.load("蘿蔔卡牌150dpi.png").convert()
        self.radish_picture = pygame.transform.scale(self.radish_picture,(CARD_SIZE[0]*7,CARD_SIZE[1]))
        self.situation = "card"
        self.position = position
        self.time = 1
    def grow(self):
        self.time = self.time + 1    
    def clean(self):
        self.situation = "card"
        self.time = 1 
    def update(self):
        if self.situation == "card":
            screen.blit(self.picture,self.position)
class Cherry_radish(Radish):
    def __init__(self,position):
        Radish.__init__(self,position)
        self.name = "櫻桃蘿蔔"
        self.period = 2
        self.cost = 0
        self.earn = 2
        self.score = 1
        # self.picture = pygame.image.load(".png").convert()
class Carrot(Radish):
    def __init__(self,position):
        Radish.__init__(self,position)
        self.name = "胡蘿蔔"
        self.period = 3
        self.cost = 1
        self.earn = 4
        self.score = 2
        self.picture = pygame.image.load(".png").convert()
class White_radish(Radish):
    def __init__(self,position):
        Radish.__init__(self,position)
        self.name = "白蘿蔔"
        self.period = 4
        self.cost = 2
        self.earn = 6
        self.score = 3
        #self.picture = ???
class Beet(Radish):
    def __init__(self,position):
        Radish.__init__(self,position)
        self.name = "甜菜根"
        self.picture = pygame.Surface(CARD_SIZE).convert()
        self.picture.blit(self.radish_picture,(0,0),(CARD_SIZE[0],0,CARD_SIZE[0],CARD_SIZE[1]))
        self.period = 5
        self.cost = 3
        self.earn = 8
        self.score = 4
class Blue_radish(Radish):
    def __init__(self,position):
        Radish.__init__(self,position)
        self.name = "藍蘿蔔"
        self.period = 3
        self.cost = 1
        self.earn = -1
        self.score = -1
        #self.picture = ???

class Special_card(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.situation = "card"
        self.position = position
        self.score = 0
    def update(self):
        if self.situation == "card":
            screen.blit(self.picture,self.position)
class Watering_can(Special_card):
    def __init__(self,position):
        Special_card.__init__(self,position)
        self.name = "澆水桶"
        self.cost = 2
        #self.picture = pygame.image.load('.png')  # 載入圖片
    def use(self,target):
        target.routine()
class Weeds(Special_card):
    def __init__(self,position):
        Special_card.__init__(self,position)
        self.name = "雜草"
        self.cost = 1
        # self.picture = ???
    def use(self,target):
        target.weeds = target.weeds + 1
class Rabbit(Special_card):
    def __init__(self,position):
        Special_card.__init__(self,position)
        self.name = "兔子"
        self.cost = 3
        self.score = 1
        # self.picture = ???
    def use(self,owner,target,radish):
        if target.fence >= 1:
            target.fence = target.fence - 1
        else :
            #拔掉蘿蔔
            print("蘿蔔被吃掉了!")
            radish.clean()
            target.garden.remove(radish)
            target.waste.append(radish)
        owner.score = owner.score + 1
class Fence(Special_card):
    def __init__(self,position):
        Special_card.__init__(self,position)
        self.name = "柵欄"
        self.cost = 2
        # self.picture = ???
    def use(self,target):
        target.fence = target.fence + 1
class Worm(Special_card):
    def __init__(self,position):
        Special_card.__init__(self,position)
        self.name = "蟲子"
        self.cost = 2
        # self.picture = ???
    def use(self,target,radish):
        if target.insecticide >= 1:
            target.insecticide = target.insecticide - 1
        else :
            #拔掉蘿蔔
            print("蘿蔔被吃掉了!")
            radish.clean()
            target.garden.remove(radish)
            target.waste.append(radish)
class Insecticide(Special_card):
    def __init__(self,position):
        Special_card.__init__(self,position)
        self.name = "殺蟲劑"
        self.cost = 0
        self.score = -1
        # self.picture = ???
    def use(self,target):
        target.insecticide = target.insecticide + 1
        target.score = target.score + self.score 

class Weather(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.situation = "card"
        self.position = position
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

all_sprite_list = pygame.sprite.Group()

station = Supply_station((600,200))
all_sprite_list.add(station)
b = Beet((50,50))
all_sprite_list.add(b)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_p = pygame.mouse.get_pos()
            if (station.position[0] <= m_p[0] and m_p[0] <= station.position[0]+CARD_SIZE[0]) and (station.position[1] <= m_p[1] and m_p[1] <= station.position[1]+CARD_SIZE[1]):
                #發牌機被點擊
                if station.situation == "show":
                    station.situation = "hide"
                else :
                    station.situation = "show"
   

    screen.fill(BLACK)
    all_sprite_list.update()
    pygame.display.update()
    clock.tick(60)
