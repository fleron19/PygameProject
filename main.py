import pygame
from random import randrange
from math import sqrt

font_name = pygame.font.match_font('arial')


def check_click(pos):
    for btn in buttons:
        if btn[0] < pos[0] < btn[2] and btn[1] < pos[1] < btn[3]:
            return buttons.index(btn)


class virus():
    def __init__(self, name, mortality, contagious, term, zona):
        self.name = name  # название вируса
        self.mortality = mortality  # летальность
        self.contagious = 100 / contagious  # заразность, шанс заражения
        self.term = term  # срок, после которого человек сам выздоравливает
        self.zona = zona  # зона вокруг заболевшего, в которой заражаются люди


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, 'WHITE')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class person():
    def __init__(self, name, color=False, vel=False):
        global v
        self.coord = [randrange(radius + 50, width - radius),
                      randrange(radius + 50, height - radius)]  # задаём случайные начальные координаты
        self.direction = 0
        self.rand_dir()  # задаём направление
        self.velocity = 0
        if not vel:
            self.velocity = v

        else:
            self.velocity = vel
        if not color:
            a = randrange(20)
            self.color = "GREEN"
            if a == 1:
                self.color = "RED"
            if a == 2:
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
            a = randrange(20)
            self.color = "GREEN"
            if a == 1 or a == 3:
                self.color = "RED"
            if a == 2:
                self.color = "BLUE"
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
            elif self.coord[1] + self.direction[1] * self.velocity / 1000 > height - radius - 50:
                self.direction[1] = -1
        self.coord[1] = self.coord[1] + self.direction[1] * self.velocity / 1000
        self.coord[0] = self.coord[0] + self.direction[0] * self.velocity / 1000
        self.renderman()

    def check_airport(self):
        if airport[0] < self.coord[0] < airport[2] and airport[1] < self.coord[1] < airport[3] and self.passenger == 0 and border == 0:
            self.passenger = 1
        if (airport[0] + airport[2]) // 2 - 2 < self.coord[0] < (airport[0] + airport[2]) // 2 + 2 and \
                (airport[1] + airport[3]) // 2 - 2 < self.coord[1] < (
                airport[1] + airport[3]) // 2 + 2 and border == 0 and self.passenger == 1:
            self.passenger = 2

    def rand_dir(self):  # функция, которая задаёт случайное направление
        self.xd, self.yd = randrange(-1, 2), randrange(-1, 2)
        self.direction = [self.xd, self.yd]

    def renderman(self):  # функция отрисовки
        pygame.draw.circle(screen, self.color, (self.coord[0], self.coord[1]), radius)


if __name__ == '__main__':
    virus = virus("простой вирус", 0.5, 50, 15, 1)
    pygame.init()
    slpress = False
    radius = 3
    buttons = [[5, 130, 45, 170, (0, 0, 100)], [5, 190, 45, 230, (100, 0, 0)],
               [5, 250, 45, 290, (0, 100, 0)], [5, 310, 45, 350, (0, 100, 100)]]  # левый верхний угол, правый нижний
    airport = [10, 0, 90, 90]  # левый верхний угол, правый нижний
    v = 200
    doctor_vel = 0
    x = 1870
    fl = 0
    border = 0
    died = 0
    doctor = 0
    doctor_vel_price = 10
    doctor_price = 10
    sick = 0
    money_change = 0
    y = 500
    xcd = 0
    ycd = 0
    money = 1
    size = width, height = 1920, 1050
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("игра вирус")
    running = True
    # img = pygame.image.load('interface.png')
    h = [0, 0]
    fps = 100
    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()
    people = [person(f"человек_{i}") for i in range(200)]
    pygame.display.update()
    while running:
        doctor = 0
        sick = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                h = event.pos
                if x < h[0] < x + 25 and y < h[1] < y + 25:
                    ycd = h[1] - y
                    slpress = True
                    pygame.draw.rect(screen, 'RED', (1863, 195, 40, 437))
                    pygame.draw.rect(screen, 'GREEN', (x, y, 25, 25))
                press = check_click(h)
                if press == 0:
                    border = (border + 1) % 2
                    buttons[0][4] = (0, 0, 100 - 50 * border)
                elif press == 2:
                    if money >= doctor_price:
                        money -= doctor_price
                        people.append(person(f"человек_{len(people) + 1}", 'BLUE'))
                elif press == 3:
                    if money >= doctor_price:
                        doctor_vel_price += 1
                        money -= doctor_vel_price
                        doctor_vel += 10
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
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, 'RED', (1863, 195, 40, 437))
        pygame.draw.rect(screen, 'GREEN', (x, y, 25, 25))
        pygame.draw.rect(screen, 'GRAY', (airport[0], airport[1], airport[2] - airport[0], airport[3] - airport[1]))
        pygame.draw.rect(screen, (0, 0, 189), (0, 0, 50, 1050))
        # screen.blit(img,(0,0))
        for btn in buttons:
            pygame.draw.rect(screen, btn[4], (btn[0], btn[1], btn[2] - btn[0], btn[3] - btn[1]))
        for man in people:
            man.change_coords()
            man.velocity = v
            if man.color == "RED":
                sick += 1
                man.count += 1
                if randrange(fps * virus.term * 0.2) / virus.mortality >= fps * virus.term - man.count * 0.5:
                    people.remove(man)
                    died += 1
                if man.count == fps * virus.term:
                    man.color = "GREEN"
                    fl += 1
                for elem in people:
                    if elem.color == "GREEN":
                        dl = sqrt((man.coord[0] - elem.coord[0]) ** 2 + (man.coord[1] - elem.coord[1]) ** 2)
                        if radius * 2 + virus.zona >= dl:
                            a = randrange(100)
                            # print(round(a % virus.contagious) != 0, a, virus.contagious, a % virus.contagious)
                            if round(a % virus.contagious) != 0:
                                elem.color = "RED"
                                #  elem.count = 0
            if man.color == "BLUE":
                doctor += 1
                man.velocity = doctor_vel + v
                for elem in people:
                    if elem.color == "RED":
                        dl = sqrt((man.coord[0] - elem.coord[0]) ** 2 + (man.coord[1] - elem.coord[1]) ** 2)
                        if radius * 2 >= dl:
                            elem.color = "GREEN"
        money_change = (len(people) - doctor - sick) / fps * v / 10000
        money_change -= ((len(people)) / fps / 50)
        money += money_change
        draw_text(screen, 'sick: ' + str(sick), 18, round(width / 1.3), 10)
        draw_text(screen, 'died: ' + str(died) + ' : ' + str(fl), 18, round(width / 1.6), 10)
        draw_text(screen, 'money: ' + str(round(money)) + ' ' + str(money_change)[:4], 18, round(width / 1.45), 10)
        draw_text(screen, 'doctor: ' + str(round(doctor)), 18, round(width / 1.75), 10)
        draw_text(screen, str(doctor_price), 18, 20, 290)
        draw_text(screen, str(doctor_vel_price), 18, 20, 350)
        pygame.draw.rect(screen, 'RED', (1863, 195, 40, 437))
        pygame.draw.rect(screen, 'GREEN', (x, y, 25, 25))
        pygame.display.flip()
        pygame.display.update()
        clock.tick(fps)
pygame.quit()
