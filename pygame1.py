
import pygame
import threading
import telebot
from telebot import types
import time
import os
import random
import math
import sys
import shutil

Chat = "C:/Users/roma_/OneDrive/Рабочий стол/bots/Pygame_game/1/Chat.txt"

runing = True
Speed = 40
ChatBox = [[0, 600], [600, 600], [600, 800], [0, 800]]
Lederboard = [[605, 600], [800, 600], [800, 800], [605, 800]]
INSIDE_COMMAND = ["<", ">", "^", "v", "/start"] 

Point = [[random.randint(90, 500), random.randint(90, 500)], [random.randint(90, 500), random.randint(90, 500)]]

#distance = math.sqrt( (x2-x1)**2 + (y2-y1)**2 )
 
 
def TelegramController():
    tbot = telebot.TeleBot("Token")
 
    @tbot.message_handler(commands=["start"])
    def sendData(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
        RIGHT = types.KeyboardButton(">")
        LEFT = types.KeyboardButton("<")
        UP = types.KeyboardButton("^")
        DOWN = types.KeyboardButton("v")
        markup.row(UP)
        markup.row(LEFT, RIGHT)
        markup.row(DOWN)
        time.sleep(0.2)
        tbot.send_message(message.chat.id, "Панель управления запущенна", reply_markup=markup)

        if len(os.listdir("C:/Users/roma_/OneDrive/Рабочий стол/bots/Pygame_game/1/UsersInfo")) <  3:
            print("good")
            with open(f"C:/Users/roma_/OneDrive/Рабочий стол/bots/Pygame_game/1/UsersInfo/{message.chat.id}.txt", "w") as file:
                file.write(f"{random.randint(50, 750)}x{random.randint(30, 550)}${str(message.from_user.first_name)}${random.randint(0, 250)}x{random.randint(0, 250)}x{random.randint(0, 250)}$0$")
        else: 
            tbot.send_message(message.chat.id, "Server is full. Wait until it will be restarted")

    @tbot.message_handler()
    def DataController(message):
        global Speed, INSIDE_COMMAND, Chat, Point, runing

        if message.text in INSIDE_COMMAND:

            UserInfo = f"C:/Users/roma_/OneDrive/Рабочий стол/bots/Pygame_game/1/UsersInfo/{message.chat.id}.txt"
            try:
                with open(UserInfo, "r+") as UI:
                    fileR = UI.read().split("$")
                    read =  fileR[0].split("x")

                    if message.text == ">" and int(read[0]) < 760:
                        UI.seek(0)
                        UI.write(f"{str(int(read[0]) + Speed)}x{read[1]}${fileR[1]}${fileR[2]}${fileR[3]}")

                    elif message.text == "<" and int(read[0]) > 40:
                        UI.seek(0)
                        UI.write(f"{str(int(read[0]) - Speed)}x{read[1]}${fileR[1]}${fileR[2]}${fileR[3]}")

                    elif message.text == "^" and int(read[1]) > 20:
                        UI.seek(0)
                        UI.write(f"{read[0]}x{str(int(read[1]) - Speed)}${fileR[1]}${fileR[2]}${fileR[3]}")

                    elif message.text == "v" and int(read[1]) < 560:
                        UI.seek(0)
                        UI.write(f"{read[0]}x{str(int(read[1]) + Speed)}${fileR[1]}${fileR[2]}${fileR[3]}")

                    else:
                        pass

                tbot.delete_message(message.chat.id, message.message_id)
            except FileNotFoundError:
                pass


        listInfo = os.listdir("C:/Users/roma_/OneDrive/Рабочий стол/bots/Pygame_game/1/UsersInfo")

        if runing == False:
            print("False")
            Top = []
            Nick = []
            tomes = []
            
            for el in listInfo:
                with open(f"C:/Users/roma_/OneDrive/Рабочий стол/bots/Pygame_game/1/UsersInfo/{el}") as file:
                    UseI = file.read().split("$")
                    Top =  Top + [UseI[3]]
                    Nick = Nick + [UseI[1]]
                    tomes = tomes + [el[:-4]]


            Top.sort(reverse=True)

            TopRes = (
                f"Топ 1:  {Nick[0] if len(Nick) > 0 else 'N/A'} -- {Top[0] if len(Top) > 0 else 'N/A'}\n",
                f"Топ 2:  {Nick[1] if len(Nick) > 1 else 'N/A'} -- {Top[1] if len(Top) > 1 else 'N/A'}\n",
                f"Топ 3:  {Nick[2] if len(Nick) > 2 else 'N/A'}  -- {Top[2] if len(Top) > 2 else 'N/A'}"
                )

            print(f"Top = {Top}^^{len(Top)}\nNick = {Nick}^^{len(Nick)}\ntomes = {tomes}")

            for i in tomes:
                if len(Nick) == 3 and len(Top) == 3:
                    tbot.send_message(int(i), f"{TopRes[0]}{TopRes[1]}{TopRes[2]}")
                elif len(Nick) == 2 and len(Top) == 2:
                    tbot.send_message(int(i), f"{TopRes[0]}, {TopRes[1]}")
                elif len(Nick) == 1 and len(Top) == 1:
                    tbot.send_message(int(i), TopRes[0])
                else:
                    print(len(Nick), len(Top))

            #os.remove(os.path.join("C:/Users/roma_/OneDrive/Рабочий стол/bots/Pygame_game/1/UsersInfo", el))




        if os.path.exists(f"C:/Users/roma_/OneDrive/Рабочий стол/bots/Pygame_game/1/UsersInfo/{message.chat.id}.txt"):
            if  "#" not in message.text:
                if message.text not in INSIDE_COMMAND:
                    if len(message.text) < 25:
                        with open(Chat, "a") as file:
                            file.write(f"[{message.from_user.first_name}]: {message.text}#")
                    else:
                        tbot.send_message(message.chat.id, "Max text lenth is 25")
            else:
                tbot.send_message(message.chat.id, 'Enter text without "#"')
        else:
            tbot.send_message(message.chat.id, "Enter the game for write messages")

 
    print("Telegram bot start")
    tbot.polling()
 
def PyGameController():
    pygame.init()

    screenController = [800, 800]
    screen = pygame.display.set_mode((screenController[0], screenController[1]))
    pygame.display.set_caption("Online game")

    def Update():
        global runing, Chat, ChatBox, Y_TEXT_POS, Point

        while runing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runing = False
        
            screen.fill((0, 0, 0))

            listInfo = os.listdir("C:/Users/roma_/OneDrive/Рабочий стол/bots/Pygame_game/1/UsersInfo")

            for el in range(0, len(Point)):
                pygame.draw.circle(screen, (200, 0, 0), (Point[el][0], Point[el][1]), 10)
                for i in listInfo:
                    with open(f"C:/Users/roma_/OneDrive/Рабочий стол/bots/Pygame_game/1/UsersInfo/{i}", "r+") as file:

                        UseI = file.read().split("$")
                        Pos = UseI[0].split("x")

                        distance = math.sqrt( ( Point[el][0]-int(Pos[0]) )**2 + ( Point[el][1]-int(Pos[1]) )**2 )

                        if distance <= 35:
                            print("1")
                            Point[el] = [random.randint(50, 550), random.randint(50, 550)]
                            file.seek(0)
                            file.write(f"{UseI[0]}${UseI[1]}${UseI[2]}${str(int(UseI[3])+1)}$")

                        if int(UseI[3]) >= 100:
                            runing = False



            pygame.draw.polygon(screen, (255, 255, 255), Lederboard)
            leadPos = 765
            pygame.draw.polygon(screen, (255, 255, 255), ChatBox)
            Chat_text = 765    

            for el in listInfo:
                with open(f"C:/Users/roma_/OneDrive/Рабочий стол/bots/Pygame_game/1/UsersInfo/{el}", "r") as file:

                    UseI = file.read().split("$")
                    Pos = UseI[0].split("x")
                    colors = UseI[2].split("x")
                    nick = UseI[1]

                    
                
                    font = pygame.font.Font(None, 24)
                    text = font.render(nick, True, (255, 255, 255))
                    screen.blit(text, (int(Pos[0]) - 40, int(Pos[1]) - 40))

                    pygame.draw.circle(screen, (int(colors[0]), int(colors[1]), int(colors[2][:3])), (int(Pos[0]), int(Pos[1])), 20)


                    

                    font = pygame.font.Font(None, 24)
                    text = font.render(f"{nick}  ---  {UseI[3]}", True, (0, 0, 0))
                    screen.blit(text, (615, leadPos))
                    leadPos -= 30

                    

            with open(Chat, "r") as messages:
                messagesR = messages.read().split("#")
                for el in range(1, 7):
                    try:
                        #AimMes = messagesR[(len(messagesR) - 1) - el]

                        if len(messagesR[(len(messagesR) - 1) - el]) > 0:
                           
                            font = pygame.font.Font(None, 24)
                            text = font.render(messagesR[(len(messagesR) - 1) - el], True, (0, 0, 0))
                            screen.blit(text, (10, Chat_text))
                            Chat_text -= 30

                            
                    except Exception as e:
                        print(e)
                            

            pygame.display.flip()
        
        with open(Chat, "w") as file:
            file.write(" # # # # #")

        pygame.quit()
    Update()
    print("Py game close")
 
thread = threading.Thread(target=TelegramController)
thread2 = threading.Thread(target=PyGameController)
 
thread.start()
thread2.start() 