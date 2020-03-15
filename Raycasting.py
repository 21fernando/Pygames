import pygame, random, math

__author__ = "21fernando"

pygame.init()
Screen_Length = 600
Screen_Height = 600
screen = pygame.display.set_mode((Screen_Length, Screen_Height))
pygame.display.set_caption("RAYCASTING")
walls = []


class Wall:
    global screen

    def __init__(self, p1, p2, p3, p4):
        self.start = pygame.math.Vector2((p1,p2))
        self.end = pygame.math.Vector2((p3,p4))

    def show(self):
        pygame.draw.line(screen, (255, 255, 255), self.start, self.end, 1)


class Avatar:
    global screen
    xCor = 0
    yCor = 0
    rays = []
    numRays = 20

    def __init__(self, num):
        self.updatePos()
        self.numRays = num
        self.genRays()

    def updatePos(self):
        self.xCor = pygame.mouse.get_pos()[0]
        self.yCor = pygame.mouse.get_pos()[1]

    def show(self):
        self.updatePos()
        pygame.draw.circle(screen, (0, 255, 0), (self.xCor, self.yCor), 10, 1)
        self.showRays()

    def genRays(self):
        for i in range(self.numRays):
            r = Ray(self.xCor, self.yCor, i * (360/self.numRays))
            self.rays.append(r)

    def updateRays(self):
        for r in self.rays:
            r.updateOrigin(self.xCor, self.yCor)

    def showRays(self):
        self.updateRays()
        for r in self.rays:
            r.show()


class Ray:
    global screen, walls

    def __init__(self, p1, p2, angle):
        self.start = pygame.math.Vector2((p1,p2))
        self.end = pygame.math.Vector2()
        self.angle = angle
        self.calculate()
    #https://github.com/meznak/ray_cast/blob/master/ray.py
    def calculate(self):
        self.end.from_polar((100000, self.angle))

        shortest = float("inf")
        intersect = pygame.math.Vector2()

        x3 = self.start.x
        x4 = self.end.x
        y3 = self.start.y
        y4 = self.end.y

        for w in walls:
            x1 = w.start.x
            x2 = w.end.x
            y1 = w.start.y
            y2 = w.end.y

            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if den == 0:
                return

            t_num = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
            t = t_num / den
            u_num = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3))
            u = u_num / den

            if u >= 0 and 0 <= t <= 1:
                x = x1 + t * (x2 - x1)
                y = y1 + t * (y2 - y1)
                dist = self.start.distance_to((x, y))
                if dist < shortest:
                    shortest = dist
                    intersect.xy = x, y

        self.end = intersect

    def updateOrigin(self, new1, new2):
        self.start.xy = new1, new2

    def show(self):
        self.calculate()
        pygame.draw.line(screen, (255, 0, 0), self.start, self.end, 1)


def main():
    global walls
    running = True
    for i in range(10):
        walls.append(Wall(random.randint(10, 590), random.randint(10, 590), random.randint(10, 590), random.randint(10, 590)))
    walls.append(Wall(-1, 0, -1, Screen_Height))
    walls.append(Wall(0, 0, Screen_Length, 0))
    walls.append(Wall(0, Screen_Height, Screen_Length, Screen_Height))
    walls.append(Wall(Screen_Length, 0, Screen_Length, Screen_Height))
    a = Avatar(50)
    while running:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        for w in walls:
            w.show()
        a.show()
        a.showRays()

    pygame.quit()


if __name__ == "__main__":
    main()
