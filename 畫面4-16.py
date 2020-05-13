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

timer = 0
new_card = 0
system_pause = 0

RADISH_PICTURE = pygame.image.load("蘿蔔卡牌150dpi.png").convert_alpha()
RADISH_PICTURE = pygame.transform.scale(RADISH_PICTURE,(CARD_SIZE[0]*7,CARD_SIZE[1]))


class Supply_station(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.picture = pygame.image.load("back.png").convert() #這裡沒去背
        self.picture = pygame.transform.scale(self.picture,CARD_SIZE)
        self.situation = "show"
        self.position = position
        self.prepare = self.create_list()
        self.waste = []
        self.used_weather = []
    def create_list(self):
        primitive = []
        # for i in range(5):
        #     primitive.append("櫻桃蘿蔔")
        for i in range(4):
            primitive.append("胡蘿蔔")
        for i in range(4):
            primitive.append("白蘿蔔")
        for i in range(3):
            primitive.append("藍蘿蔔")
        for i in range(3):
            primitive.append("甜菜根")
        # for i in range(4):
        #     primitive.append("兔子")
        # for i in range(3):
        #     primitive.append("柵欄")
        # for i in range(3):
        #     primitive.append("澆水桶")
        # for i in range(2):
        #     primitive.append("雜草")
        # for i in range(3):
        #     primitive.append("蟲子")
        # for i in range(2):
        #     primitive.append("殺蟲劑")
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
        random.shuffle(self.prepare)
        n = self.prepare.pop()
        if type(n) == str:
            new_card = self.translate(n)
        else :
            new_card = n
        all_sprite_list.add(new_card)
        if len(self.prepare) == 0:
            while len(self.waste) > 0:
                self.prepare.append(self.waste.pop())
        return new_card
    def update(self):
        if self.situation == "show":
            screen.blit(self.picture,self.position)

class Farmer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.card = [0,0,0] #手中的牌
        self.garden_picture = pygame.image.load("farm.png").convert_alpha()
        self.garden_picture = pygame.transform.scale(self.garden_picture,(250,200))
        self.garden = [0,0,0,0,0,0,0,0,0] #目前正在種植的蘿蔔
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
        place = self.card.index(c)
        self.waste.append(c)
        self.card[place] = 0
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
    def update(self):
        screen.blit(self.garden_picture,self.garden_position)
class Player(Farmer):
    def __init__(self):
        Farmer.__init__(self)
        self.money = Coin((650,580))
        all_sprite_list.add(self.money)
        self.card_position = [(100,450),(300,450),(500,450)]
        self.garden_position = (100,200)



class Coin(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.picture = pygame.image.load("coin.png").convert_alpha()
        self.picture = pygame.transform.scale(self.picture,(50,50))
        self.position = position
        self.number = 5
        self.font = pygame.font.SysFont("arial",40)
        self.text = self.font.render("x5",True,WHITE,BLACK)
    def update(self):
        for i in range(self.number):
            screen.blit(self.picture,(self.position[0]+60*i,self.position[1]))
        # screen.blit(self.picture,self.position)
        # self.text = self.font.render("X"+str(self.number),True,WHITE,BLACK)
        # screen.blit(self.text,(self.position[0]+53,self.position[1]+5))

class Radish(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.situation = "card"
        self.position = position
        self.time = 1
    def grow(self):
        self.time = self.time + 1    
    def clean(self):
        self.situation = "hide"
        self.time = 1 
    def update(self):
        if self.situation == "card":
            screen.blit(self.card_picture,self.position)
        elif self.situation == "amplify":
            screen.blit(self.card_picture,self.position)
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
        self.card_picture = pygame.Surface(CARD_SIZE).convert()
        self.card_picture.blit(RADISH_PICTURE,(0,0),(CARD_SIZE[0]*4,0,CARD_SIZE[0],CARD_SIZE[1]))
        self.period = 3
        self.cost = 1
        self.earn = 4
        self.score = 2
class White_radish(Radish):
    def __init__(self,position):
        Radish.__init__(self,position)
        self.name = "白蘿蔔"
        self.card_picture = pygame.Surface(CARD_SIZE).convert()
        self.card_picture.blit(RADISH_PICTURE,(0,0),(CARD_SIZE[0]*6,0,CARD_SIZE[0],CARD_SIZE[1]))
        self.period = 4
        self.cost = 2
        self.earn = 6
        self.score = 3
class Beet(Radish):
    def __init__(self,position):
        Radish.__init__(self,position)
        self.name = "甜菜根"
        self.card_picture = pygame.Surface(CARD_SIZE).convert()
        self.card_picture.blit(RADISH_PICTURE,(0,0),(CARD_SIZE[0]*0,0,CARD_SIZE[0],CARD_SIZE[1]))
        self.period = 5
        self.cost = 3
        self.earn = 8
        self.score = 4
class Blue_radish(Radish):
    def __init__(self,position):
        Radish.__init__(self,position)
        self.name = "藍蘿蔔"
        self.card_picture = pygame.Surface(CARD_SIZE).convert()
        self.card_picture.blit(RADISH_PICTURE,(0,0),(CARD_SIZE[0]*2,0,CARD_SIZE[0],CARD_SIZE[1]))
        self.period = 3
        self.cost = 1
        self.earn = -1
        self.score = -1

class Special_card(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.situation = "card"
        self.position = position
        self.score = 0
    def clean(self):
        self.situation = "hide"
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

station = Supply_station((800,250))
all_sprite_list.add(station)

me = Player()
all_sprite_list.add(me)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if system_pause == 0:
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_p = pygame.mouse.get_pos()
                #發牌機被點擊
                if (station.position[0] <= m_p[0] and m_p[0] <= station.position[0]+CARD_SIZE[0]) and (station.position[1] <= m_p[1] and m_p[1] <= station.position[1]+CARD_SIZE[1]):
                    if me.need_card():
                        new_card  = station.next()
                        timer = pygame.time.get_ticks()
                        system_pause = 1
                #第一張牌被點擊
                if (me.card_position[0][0] <= m_p[0] and m_p[0] <= me.card_position[0][0]+CARD_SIZE[0]) and (me.card_position[0][1] <= m_p[1] and m_p[1] <= me.card_position[0][1]+CARD_SIZE[1]):
                    if me.card[0] != 0:
                        if me.card[0].situation == "card":
                            me.card[0].position = (me.card_position[0][0]-10,me.card_position[0][1]-10)
                            me.card[0].card_picture =  pygame.transform.scale(me.card[0].card_picture,(CARD_SIZE[0]+20,CARD_SIZE[1]+20))
                            me.card[0].situation = "amplify"
                        else :
                            me.card[0].position = (me.card_position[0])
                            me.card[0].card_picture =  pygame.transform.scale(me.card[0].card_picture,CARD_SIZE)
                            me.card[0].situation = "card"
                #第二張牌被點擊
                if (me.card_position[1][0] <= m_p[0] and m_p[0] <= me.card_position[1][0]+CARD_SIZE[0]) and (me.card_position[1][1] <= m_p[1] and m_p[1] <= me.card_position[1][1]+CARD_SIZE[1]):
                    if me.card[1] != 0:
                        if me.card[1].situation == "card":
                            me.card[1].position = (me.card_position[1][0]-10,me.card_position[1][1]-10)
                            me.card[1].card_picture =  pygame.transform.scale(me.card[1].card_picture,(CARD_SIZE[0]+20,CARD_SIZE[1]+20))
                            me.card[1].situation = "amplify"
                        else :
                            me.card[1].position = (me.card_position[1])
                            me.card[1].card_picture =  pygame.transform.scale(me.card[1].card_picture,CARD_SIZE)
                            me.card[1].situation = "card"
                #第三張牌被點擊
                if (me.card_position[2][0] <= m_p[0] and m_p[0] <= me.card_position[2][0]+CARD_SIZE[0]) and (me.card_position[2][1] <= m_p[1] and m_p[1] <= me.card_position[2][1]+CARD_SIZE[1]):
                    if me.card[2] != 0:
                        if me.card[2].situation == "card":
                            me.card[2].position = (me.card_position[2][0]-10,me.card_position[2][1]-10)
                            me.card[2].card_picture =  pygame.transform.scale(me.card[2].card_picture,(CARD_SIZE[0]+20,CARD_SIZE[1]+20))
                            me.card[2].situation = "amplify"
                        else :
                            me.card[2].position = (me.card_position[2])
                            me.card[2].card_picture =  pygame.transform.scale(me.card[2].card_picture,CARD_SIZE)
                            me.card[2].situation = "card"

    #有人在抽牌
    if new_card != 0:
        if pygame.time.get_ticks() - timer >= 500:
            me.draw_card(new_card)
            new_card = 0
            system_pause = 0
            if me.need_card():
                new_card  = station.next()
                timer = pygame.time.get_ticks()
                system_pause = 1

                
                

    screen.fill(BLACK)
    all_sprite_list.update()
    pygame.display.update()
    clock.tick(60)
