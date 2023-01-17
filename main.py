from math import sqrt
from random import randrange

import pygame
import sqlite3

pygame.init()
CONST_DBNAME = 'virusDB.db'
font_name = pygame.font.match_font('arial')

button_sound = pygame.mixer.Sound('click.mp3')
hosp_sound = pygame.mixer.Sound('hospital.mp3')
vaccine_sound = pygame.mixer.Sound('vaccine.mp3')
error = pygame.mixer.Sound('error.mp3')


def check_click(pos, lis):
    for btn in lis:
        if btn[0] < pos[0] < btn[2] and btn[1] < pos[1] < btn[3]:
            return lis.index(btn)


class virus():
    def __init__(self, name, mortality, contagious, term, zona, period, time_vac):
        self.name = name  # название вируса
        self.mortality = mortality  # летальность
        self.contagious = contagious  # заразность, шанс заражения
        self.term = term  # срок, после которого человек сам выздоравливает
        self.zona = zona  # зона вокруг заболевшего, в которой заражаются люди
        self.period = period
        self.time_vac = time_vac


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, 'WHITE')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class hospital():
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.isOn = True


class person():
    def __init__(self, name, color=False, vel=False, pas=0):
        global v
        self.coord = [randrange(radius + 50, width - radius),
                      randrange(radius + 50, height - radius - 60)]  # задаём случайные начальные координаты
        self.direction = 0
        self.rand_dir()  # задаём направление
        self.velocity = 0
        self.pas = pas
        self.per = 0
        self.vaccine = 0
        self.time_vaccine = virus.time_vac + 1
        if pas == 3:
            self.coord[0] = 2300
            self.coord[1] = 50
        if not vel:
            self.velocity = v
        else:
            self.velocity = vel
        if not color:
            a = randrange(100)
            self.color = "GREEN"
            if 0 <= a <= 9:
                self.color = "RED"
            if 11 <= a <= 13:
                self.color = "BLUE"
        else:
            self.color = color

        self.name = name
        self.count = 0
        self.passenger = 0

    def change_coords(self):  # функция, просчитывающая движение и изменяющая направление
        self.check_airport()
        if (airport[2] - airport[0]) // 2 + airport[0] >= self.coord[0] and self.passenger == 3:
            self.passenger = 4
            self.direction = [0, 1]

        if (self.passenger == 4) and (airport[3] < self.coord[1] or airport[1] > self.coord[1]):
            self.passenger = 0

        if self.coord[0] >= 2300:
            self.coord[1] -= 10
            if not self.pas == 3:
                a = randrange(20)
                self.color = "GREEN"
                if a == 1 or a == 3:
                    self.color = "RED"
                if a == 2:
                    self.color = "BLUE"
            self.per = 0
            self.vaccine = 0
            self.time_vaccine = virus.time_vac + 1
            self.count = 0
            self.passenger = 3

        if self.passenger == 1:
            self.direction = [
                ((airport[0] + airport[2]) // 2 - self.coord[0]) // abs((airport[0] + airport[2]) // 2 - self.coord[0]),
                ((airport[1] + airport[3]) // 2 - self.coord[1]) // abs((airport[1] + airport[3]) // 2 - self.coord[1])]
        elif self.passenger == 2:
            self.direction = [10, 0]

        elif self.passenger == 3:
            self.direction = [-10, 0]

        else:
            r, r1 = randrange(0, 101), randrange(0, 101)
            if r % 33 == 0 and r1 % 15 == 0 or (self.direction[0] == 0 and self.direction[1] == 0 and r % 50 == 0):
                self.rand_dir()
            if self.coord[0] + self.direction[0] * self.velocity / 1000 < radius + 50:
                self.direction[0] = 1
            elif self.coord[0] + self.direction[0] * self.velocity / 1000 > width - radius - 50:
                self.direction[0] = -1
            if self.coord[1] + self.direction[1] * self.velocity / 1000 < radius + 50:
                self.direction[1] = 1
            elif self.coord[1] + self.direction[1] * self.velocity / 1000 > height - radius - 100:
                self.direction[1] = -1
        self.coord[1] = self.coord[1] + self.direction[1] * self.velocity / 1000
        self.coord[0] = self.coord[0] + self.direction[0] * self.velocity / 1000
        self.renderman()

    def check_airport(self):
        global money
        if airport[0] < self.coord[0] < airport[2] and airport[1] < self.coord[1] < airport[
            3] and self.passenger == 0 and border == 0:
            self.passenger = 1
        if (airport[0] + airport[2]) // 2 - 2 < self.coord[0] < (airport[0] + airport[2]) // 2 + 2 and \
                (airport[1] + airport[3]) // 2 - 2 < self.coord[1] < (
                airport[1] + airport[3]) // 2 + 2 and border == 0 and self.passenger == 1:
            self.passenger = 2
            money += 5

    def rand_dir(self):  # функция, которая задаёт случайное направление
        self.xd, self.yd = randrange(-1, 2), randrange(-1, 2)
        self.direction = [self.xd, self.yd]

    def renderman(self):  # функция отрисовки
        if self.vaccine == 1:
            pygame.draw.circle(screen, "YELLOW", (self.coord[0], self.coord[1]), radius + 5, 2)
        pygame.draw.circle(screen, self.color, (self.coord[0], self.coord[1]), radius)


if __name__ == '__main__':
    con = sqlite3.connect(CONST_DBNAME)
    cur = con.cursor()
    result = con.cursor().execute("""SELECT * FROM games where status = 'online'""").fetchone()
    virus = virus(result[3], result[4], result[5], result[6], result[7], result[8], result[9])
    Id = result[0]
    slpress = False
    radius = 3
    buttons = [[5, 130, 45, 170, (0, 0, 100)], [5, 190, 45, 230, (100, 0, 0)],
               [5, 250, 45, 290, (0, 100, 0)], [5, 310, 45, 350, (0, 100, 100)],
               [5, 370, 45, 410, (100, 100, 0)], [5, 430, 45, 470, (0, 200, 50)],
               [5, 490, 45, 530, (0, 200, 200)]]  # левый верхний угол, правый нижний
    more_buttons = [[55, 370, 95, 410, (100, 100, 0)], [55, 430, 95, 470, (100, 100, 0)],
                    [55, 500, 95, 540, (100, 100, 0)], [55, 560, 95, 600, (100, 100, 0)]]
    airport = [10, 0, 90, 90]  # левый верхний угол, правый нижний
    v = 200
    vaccine_pr = 0
    doctor_vel = 0
    x = 1870
    fl = 0
    vaccine_create = 0
    border = 0
    died = 0
    hosp_set = False
    open1 = 0
    mask = 0
    doctor = 0
    doctor_vel_price = 10
    doctor_price = 10
    hospital_price = 100
    hospitals = []
    sick = 0
    hx = 0
    hy = 0
    money_change = 0
    y = 500
    xcd = 0
    ycd = 0
    respirator = 0
    vitamins = 0
    medicines = 0
    money = 100
    clock = pygame.time.Clock()
    size = width, height = 1920, 1050
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    pygame.display.update()
    pygame.display.set_caption("игра вирус")
    running = True
    people = [person(f"человек_{i}") for i in range(200)]
    h = [0, 0]
    fps = 100
    while running:
        if died >= 100:
            print(1)
            cur = con.cursor()
            strQuery = "update games set status = 'поражение' WHERE status = 'online'"
            cur.execute(strQuery)    
            con.commit()    
            print(2)            
            running = False 
            print(3)
            #v = 200
            #vaccine_pr = 0
            #doctor_vel = 0
            #x = 1870
            #fl = 0
            #border = 0
            #died = 0
            #hosp_set = False
            #open1 = 0
            #mask = 0
            #doctor = 0
            #doctor_vel_price = 10
            #doctor_price = 10
            #hospital_price = 100
            #hospitals = []
            #people = [person(f"человек_{i}") for i in range(200)]
            #sick = 0
            #hx = 0
            #hy = 0
            #money_change = 0
            #y = 500
            #xcd = 0
            #ycd = 0
            #money = 100
        screen.fill((0, 0, 0))
        doctor = 0
        sick = 0
        if money >= 100 and vaccine_pr < 100:
            buttons[6][4] = (0, 200, 200)
        if vaccine_pr >= 100 or money < 100:
            buttons[6][4] = (0, 100, 100)
        if hosp_set:
            pygame.draw.rect(screen, (0, 50, 100), (hx - 25, hy - 25, 50, 50))
        for event in pygame.event.get():
            if event.type == 768 and hosp_set:
                hosp_set = False
            if hosp_set:
                hx, hy = pygame.mouse.get_pos()
                pygame.draw.rect(screen, (0, 50, 100), (hx - 25, hy - 25, 50, 50))
            if event.type == pygame.QUIT:
                cur = con.cursor()
                strQuery = "update games set status = 'прерванно' WHERE status = 'online'"
                cur.execute(strQuery)    
                con.commit()    
                running = False
                            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                h = event.pos
                for q in hospitals:
                    print(str(q.x) + ' ' + str(h[0]))
                    if q.x < h[0] < q.x + q.width and q.y < h[1] < q.y + q.height:
                        button_sound.play()
                        q.isOn = not q.isOn
                        print(q.isOn)
                if hosp_set:
                    hosp_sound.play()
                    slpress = False
                    hospitals.append(hospital(h[0] - 25, h[1] - 25, 50, 50))
                    money -= hospital_price
                    hospital_price += 25
                    hosp_set = False
                if x < h[0] < x + 25 and y < h[1] < y + 25:
                    ycd = h[1] - y
                    slpress = True
                    pygame.draw.rect(screen, 'RED', (1863, 195, 40, 437))
                    pygame.draw.rect(screen, 'GREEN', (x, y, 25, 25))
                press = check_click(h, buttons)
                if press == 0:
                    border = not border
                    buttons[0][4] = (0, 0, 100 - 50 * border)
                    button_sound.play()
                elif press == 2:
                    if money >= doctor_price:
                        button_sound.play()
                        money -= doctor_price
                        people.append(person(f"человек_{len(people) + 1}", vel=v + doctor_vel, color="BLUE", pas=3))
                        doctor_price += 1
                    else:
                        error.play()
                elif press == 3:
                    if money >= doctor_vel_price:
                        button_sound.play()
                        doctor_vel_price += 1
                        money -= doctor_vel_price
                        doctor_vel += 10
                    else:
                        error.play()

                elif press == 5:
                    if money >= hospital_price:
                        button_sound.play()
                        hosp_set = True
                    else:
                        error.play()
                elif press == 4:
                    button_sound.play()
                    open1 = not open1
                    buttons[4][4] = (100, 100 - 50 * open1, 0)
                elif press == 6:
                    if money >= 10:
                        button_sound.play()
                        vaccine_pr += 10
                        money -= 10
                    else:
                        error.play()
                if open1 == 1:
                    more_press = check_click(h, more_buttons)
                    if more_press == 0:
                        mask = not mask
                        button_sound.play()
                        more_buttons[0][4] = (100, 100 - 50 * mask, 0)
                    elif more_press == 1:           
                        vitamins = not vitamins
                        button_sound.play()
                        more_buttons[1][4] = (100, 100 - 50 * vitamins, 0)
                    elif more_press == 2:
                        respirator = not respirator
                        button_sound.play()
                        more_buttons[2][4] = (100, 100 - 50 * respirator, 0)
                    elif more_press == 3:
                        medicines = not medicines
                        button_sound.play()
                        more_buttons[3][4] = (100, 100 - 50 * medicines, 0)

            if event.type == pygame.MOUSEMOTION and slpress:
                screen.fill((0, 0, 0))
                drawing = True
                h = event.pos
                y = h[1] - ycd
                if y > 600:
                    y = 600
                elif y < 200:
                    y = 200
                v = (600 - y) * 2
                pygame.draw.rect(screen, 'GREEN', (x, y, 25, 25))
                pygame.draw.rect(screen, 'RED', (1863, 195, 40, 437))
                pygame.display.flip()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                slpress = False
        if money <= 0:
            slpress = False
            money = 0
            y = 200
            v = (600 - y) * 2
        pygame.draw.rect(screen, 'RED', (1863, 195, 40, 437))
        pygame.draw.rect(screen, 'GREEN', (x, y, 25, 25))
        for q in hospitals:
            if q.isOn:
                pygame.draw.rect(screen, (0, 50, 100), (q.x, q.y, q.width, q.height))
            else:
                pygame.draw.rect(screen, (0, 10, 20), (q.x, q.y, q.width, q.height))
        pygame.draw.rect(screen, 'GRAY', (airport[0], airport[1], airport[2] - airport[0], airport[3] - airport[1]))
        pygame.draw.rect(screen, 'GRAY', (100, 970, 400, 40))
        pygame.draw.rect(screen, (0, 0, 189), (0, 0, 50, 1050))
        # screen.blit(img,(0,0))
        for btn in buttons:
            pygame.draw.rect(screen, btn[4], (btn[0], btn[1], btn[2] - btn[0], btn[3] - btn[1]))
        for man in people:
            man.change_coords()
            man.velocity = v
            if man.color == "RED":
                for hosp in hospitals:
                    if hosp.x < man.coord[0] < hosp.x + hosp.width and hosp.y < man.coord[
                        1] < hosp.y + hosp.height and hosp.isOn:
                        man.time_vaccine = 0
                        man.color = 'GREEN'
                        if vaccine_pr == 100:
                            man.vaccine = 1
                sick += 1
                man.count += 1
                if randrange(fps * virus.term * 0.2) / virus.mortality >= fps * virus.term - man.count * 0.5:
                    if randrange(100) % 100 / 15 != 0 or vitamins == 0:
                        if randrange(100) % 100 / 15 != 0 or medicines == 0:
                            people.remove(man)
                            died += 1
                if man.count == fps * virus.term:
                    man.time_vaccine = 0
                    man.color = "GREEN"
                    fl += 1
                for elem in people:
                    if elem.color == "GREEN" and elem.vaccine == 0:
                        dl = sqrt((man.coord[0] - elem.coord[0]) ** 2 + (man.coord[1] - elem.coord[1]) ** 2)
                        if radius * 2 + virus.zona >= dl:
                            a = randrange(100)
                            # print(round(a % virus.contagious) != 0, a, virus.contagious, a % virus.contagious)
                            if round(a % virus.contagious) != 0:
                                if randrange(100) % (100 / 10) != 0 or vitamins == 0:
                                    if randrange(100) % (100 / 20) != 0 or medicines == 0:                                
                                        elem.color = "ORANGE"
                                        elem.per = 0                                
                                #  elem.count = 0
            if man.color == "ORANGE":
                for hosp in hospitals:
                    if hosp.x < man.coord[0] < hosp.x + hosp.width and hosp.y < man.coord[
                        1] < hosp.y + hosp.height and hosp.isOn:
                        man.color = 'GREEN'
                        man.time_vaccine = 0
                        if vaccine_pr == 100:
                            man.vaccine = 1
                man.per += 1 / fps
                if man.per >= virus.period:
                    man.color = "RED"
                for elem in people:
                    if elem.color == 'GREEN' and elem.vaccine == 0:
                        dl = sqrt((man.coord[0] - elem.coord[0]) ** 2 + (man.coord[1] - elem.coord[1]) ** 2)
                        if radius * 2 + virus.zona >= dl:
                            a = randrange(100)
                            # print(round(a % virus.contagious) != 0, a, virus.contagious, a % virus.contagious)
                            if round(a % virus.contagious) != 0:
                                if randrange(100) % (100 / 10) != 0 or vitamins == 0:
                                    if randrange(100) % (100 / 20) != 0 or medicines == 0:                                
                                        elem.color = "ORANGE"
                                        elem.per = 0          
                                #  elem.count = 0
            if man.color == "BLUE":
                doctor += 1
                man.velocity = doctor_vel + v
                for elem in people:
                    if elem.color == "RED":
                        dl = sqrt((man.coord[0] - elem.coord[0]) ** 2 + (man.coord[1] - elem.coord[1]) ** 2)

                        if radius * 2 >= dl:
                            if vaccine_pr == 100:
                                elem.vaccine = 1
                                elem.color = "GREEN"
                                elem.time_vaccine = 0
                            else:
                                vaccine_pr += 1
                                elem.color = "GREEN"
            else:
                if man.time_vaccine <= virus.time_vac:
                    man.time_vaccine += 1 / fps
            if man.time_vaccine < virus.time_vac and man.color == 'GREEN':
                man.vaccine = 1
            if man.time_vaccine >= virus.time_vac and vaccine_pr < 100:
                man.vaccine = 0
        money_change = (len(people) - doctor - sick) / fps * v / 10000
        money_change -= ((len(people)) / fps / 50)
        for h in hospitals:
            if h.isOn:
                money_change -= 0.01
        money_change = money_change - ((mask * 2) / fps) - ((respirator * 4) / fps) - ((vitamins * 2) / fps) - ((medicines * 4) / fps)
        money += money_change
        
        if open1 == 1:
            pygame.draw.rect(screen, (0, 0, 139), (50, 360, 250, 300))
            draw_text(screen, 'маски', 20, 135, 370)
            draw_text(screen, 'шанс заражения -10%', 15, 165, 390)
            draw_text(screen, 'витамины', 20, 145, 430)
            draw_text(screen, 'шанс смертность -10%', 15, 165, 450) 
            draw_text(screen, 'респиратор', 20, 155, 500)
            draw_text(screen, 'шанс заражения -25%', 15, 165, 520)
            draw_text(screen, 'лекарства', 20, 155, 560)
            draw_text(screen, 'шанс смертность -20%', 15, 165, 580)            
            for btn in more_buttons:
                pygame.draw.rect(screen, btn[4], (btn[0], btn[1], btn[2] - btn[0], btn[3] - btn[1]))
        if vaccine_pr >= 100:
            vaccine_pr = 100
            if vaccine_create == 0:
                vaccine_sound.play()
            vaccine_create = 1
        if sick == 0:
            cur = con.cursor()
            strQuery = "update games set status = 'победа' WHERE status = 'online'"
            cur.execute(strQuery)    
            con.commit()
            running = False
        draw_text(screen, 'sick: ' + str(sick), 18, round(width / 1.3), 10)
        draw_text(screen, 'died: ' + str(died) + ' : ' + str(fl), 18, round(width / 1.6), 10)
        draw_text(screen, 'money: ' + str(round(money)) + ' ' + str(money_change)[:4], 18, round(width / 1.45), 10)
        draw_text(screen, 'doctor: ' + str(round(doctor)), 18, round(width / 1.75), 10)
        draw_text(screen, str(doctor_price), 18, 20, 290)
        draw_text(screen, str(doctor_vel_price), 18, 20, 350)
        draw_text(screen, str(hospital_price), 18, 20, 470)
        pygame.draw.rect(screen, (0, 200, 200), (100, 970, vaccine_pr * 4, 40))
        pygame.draw.rect(screen, 'RED', (1863, 195, 40, 437))
        pygame.draw.rect(screen, 'GREEN', (x, y, 25, 25))
        draw_text(screen, str(vaccine_pr) + ' / 100', 18, 300, 980)
        pygame.display.update()
        clock.tick(fps)
pygame.quit()