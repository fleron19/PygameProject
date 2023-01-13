import pygame
from random import randrange
from math import sqrt

font_name = pygame.font.match_font('arial')


class virus():
    def __init__(self, name, mortality, contagious, term, zona):
        self.name = name  # название вируса
        self.mortality = mortality  # летальность
        self.contagious = contagious  # заразность, шанс заражения
        self.term = term  # срок, после которого человек сам выздоравливает
        self.zona = zona  # зона вокруг заболевшего, в которой заражаются люди


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, 'WHITE')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class person():
    def __init__(self, name):
        self.coord = [randrange(radius, width - radius),
                      randrange(radius, height - radius)]  # задаём случайные начальные координаты
        self.direction = self.rand_dir()  # задаём направление
        a = randrange(20)
        self.color = "GREEN"
        if a == 1:
            self.color = "RED"
        if a == 2:
            self.color = "BLUE"
        self.name = name
        self.count = 0
        self.passenger = 0

    def change_coords(self):  # функция, просчитывающая движение и изменяющая направление
        global v
        self.cheak_airport()
        if self.passenger == 1:
            self.direction = [((0 + 40) // 2 - self.coord[0]) // abs((0 + 40) // 2 - self.coord[0]),
                              ((0 + 40) // 2 - self.coord[1]) // abs((0 + 40) // 2 - self.coord[1])]
        if self.passenger == 2:
            self.direction = [5, 0]
        else:
            r, r1 = randrange(0, 101), randrange(0, 101)
            if r % 33 == 0 and r1 % 15 == 0 or (self.direction[0] == 0 and self.direction[1] == 0 and r % 50 == 0):
                self.direction = self.rand_dir()
            if self.coord[0] + self.direction[0] * v / 1000 < radius:
                self.direction[0] = 1
            elif self.coord[0] + self.direction[0] * v / 1000 > width - radius:
                self.direction[0] = -1
            if self.coord[1] + self.direction[1] * v / 1000 < radius + 15:
                self.direction[1] = 1
            elif self.coord[1] + self.direction[1] * v / 1000 > height - radius:
                self.direction[1] = -1
        self.coord[1] = self.coord[1] + self.direction[1] * v / 1000
        self.coord[0] = self.coord[0] + self.direction[0] * v / 1000
        self.renderman()

    def cheak_airport(self):
        if self.coord[0] > 0 and self.coord[0] < 40 and self.coord[1] > 0 and self.coord[
            1] < 40 and self.passenger == 0:
            self.passenger = 1
        if self.coord[0] > (0 + 40) // 2 - 2 and self.coord[0] < (0 + 40) // 2 + 2 and self.coord[1] > (
                0 + 40) // 2 - 2 and self.coord[1] < (0 + 40) // 2 + 2:
            self.passenger = 2

    def rand_dir(self):  # функция, которая задаёт случайное направление
        self.xd, self.yd = randrange(-1, 2), randrange(-1, 2)
        return [self.xd, self.yd]

    def renderman(self):  # функция отрисовки
        pygame.draw.circle(screen, self.color, (self.coord[0], self.coord[1]), radius)


if __name__ == '__main__':
    virus = virus("простой вирус", 50, 50, 15, 0)
    pygame.init()
    slpress = False
    radius = 3
    v = 200
    x = 1870
    fl = 0
    died = 0
    y = 500
    xcd = 0
    ycd = 0
    size = width, height = 1920, 1050
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("игра вирус")
    running = True
    h = [0, 0]
    fps = 100
    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()
    people = [person(f"человек_{i}") for i in range(200)]
    pygame.display.update()
    while running:
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
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, 'RED', (1863, 195, 40, 437))
        pygame.draw.rect(screen, 'GREEN', (x, y, 25, 25))
        pygame.draw.rect(screen, 'GRAY', (0, 0, 40, 40))
        for man in people:
            man.change_coords()
            if man.color == "RED":
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
                            print(round(a % virus.contagious) != 0, a, virus.contagious, a % virus.contagious)
                            if round(a % virus.contagious) != 0:
                                elem.color = "RED"
            if man.color == "BLUE":
                for elem in people:
                    if elem.color == "RED":
                        dl = sqrt((man.coord[0] - elem.coord[0]) ** 2 + (man.coord[1] - elem.coord[1]) ** 2)
                        if radius * 2 >= dl:
                            elem.color = "GREEN"
        draw_text(screen, 'died:' + str(died) + ' : ' + str(fl), 18, round(width / 1.5), 10)
        pygame.draw.rect(screen, 'RED', (1863, 195, 40, 437))
        pygame.draw.rect(screen, 'GREEN', (x, y, 25, 25))
        pygame.display.flip()
        pygame.display.update()
        clock.tick(fps)
pygame.quit()