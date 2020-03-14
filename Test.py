import pygame, random, math

__author__ = "21fernando"

pygame.init()
Screen_Length = 600
Screen_Height = 600
screen = pygame.display.set_mode((Screen_Length, Screen_Height))
pygame.display.set_caption("RAYCASTING")
walls = []


class Wall:
    def __init__(self, screen: pygame.display, start: tuple, end: tuple):
        self.start = pygame.Vector2(start)
        self.end = pygame.Vector2(end)
        self.image = None

    def update(self, screen: pygame.display):
        self.image = pygame.draw.line(screen, pygame.Color('white'), self.start, self.end, 2)


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
            r = Ray(self.xCor, self.yCor, 1+ i * (360/self.numRays))
            self.rays.append(r)
            r = Ray(self.xCor, self.yCor, 1 + (-i * (360/self.numRays)))
            self.rays.append(r)

    def updateRays(self):
        for r in self.rays:
            r.updateOrigin(self.xCor, self.yCor)
            r.show()

    def showRays(self):
        self.updateRays()
        for r in self.rays:
            r.show()


class Ray:
    global screen, walls
    x1 = 0
    y1 = 0
    angle = 0
    slope = 0
    yint = 0
    length = 0

    def __init__(self, p1, p2, angle):
        self.x1 = p1
        self.y1 = p2
        self.angle = angle
        if angle == 90 or angle == 270:
            self.slope = 9999
        else:
            self.slope = math.tan(math.radians(self.angle))
        self.yint = int(self.y1 - self.slope * self.x1)
        self.calculate()

    def calculate(self):
        self.length = 100

    def updateOrigin(self, new1, new2):
        self.x1 = new1
        self.y1 = new2
        self.calculate()

    def show(self):
        xdist = math.sqrt(math.pow(self.length,2)/(1 + math.pow(self.slope,2)))
        ydist = math.sqrt(math.pow(self.length,2)/(1 + math.pow(1/self.slope,2)))
        pygame.draw.line(screen, (255, 0, 0), (self.x1, self.y1), (self.x1 + xdist, self.y1+ydist), 1)


def getIntersect(slope1, yint1, slope2, yint2):
    a = -slope1
    c = -slope2
    b = 1
    d = 1
    e = yint1
    f = yint2
    return [((e * d - b * f) / (a * d - b * c)), ((a * f - e * c) / (a * d - b * c))]

def onLine(point, wall: Wall):
    lowX = wall.x1 if wall.x1 < wall.x2 else wall.x2
    highX = wall.x1 if wall.x1 > wall.x2 else wall.x2
    lowY = wall.y1 if wall.y1 < wall.y2 else wall.y2
    highY = wall.y1 if wall.y1 > wall.y2 else wall.y2
    return lowX <= point[0] <= highX and lowY <=point[1] <= highY

def distance(p1, p2):
    return math.sqrt(math.pow((p2[0] - p1[0]),2) + math.pow((p2[1] - p1[1]),2))

def main():
    global screen
    global walls
    running = True
    while running:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        p = Wall(screen, (100,100), (200,200))
        p.update(screen)

    pygame.quit()


if __name__ == "__main__":
    main()
