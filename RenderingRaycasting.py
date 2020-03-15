import pygame, random, math

__author__ = "21fernando"

pygame.init()
Screen_Length = 600
Screen_Height = 600
screen = pygame.display.set_mode((Screen_Length * 2, Screen_Height))

pygame.display.set_caption("RENDERING RAYCASTING")
walls = []


class Wall:
    global screen

    def __init__(self, p1, p2, p3, p4):
        self.start = pygame.math.Vector2((p1, p2))
        self.end = pygame.math.Vector2((p3, p4))

    def show(self):
        pygame.draw.line(screen, (255, 255, 255), self.start, self.end, 1)


class Avatar:
    global screen
    rays = []
    lengths = []
    angle = 0

    def __init__(self, num):
        self.pos = pygame.math.Vector2((Screen_Length // 2, Screen_Height // 2))
        self.fov = num
        self.genRays()
        for i in range(self.fov):
            self.lengths.append(0)

    def updatePos(self, x, y):
        self.pos.x = x
        self.pos.y = y

    def show(self):
        pygame.draw.circle(screen, (0, 255, 0), (int(self.pos.x), int(self.pos.y)), 10, 1)
        self.showRays()

    def genRays(self):
        for i in range(self.fov):
            r = Ray(self.pos.x, self.pos.y, i - self.fov // 2)
            self.rays.append(r)

    def updateRays(self):
        for r in self.rays:
            r.updateOrigin(self.pos.x, self.pos.y)

    def showRays(self):
        self.updateRays()
        for i in range(len(self.rays)):
            self.rays[i].show()
            self.lengths[i] = self.rays[i].length()

    def rotate(self, change):
        for i in range(len(self.rays)):
            self.rays[i].angle += change
        self.angle += change


class Ray:
    global screen, walls

    def __init__(self, p1, p2, angle):
        self.start = pygame.math.Vector2((p1, p2))
        self.end = pygame.math.Vector2()
        self.angle = angle
        self.calculate()

    # https://github.com/meznak/ray_cast/blob/master/ray.py
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

    def length(self):
        return math.sqrt(math.pow(self.start.x - self.end.x, 2) + math.pow(self.start.y - self.end.y, 2))


def mapVal(val, oldMin, oldMax, newMin, newMax):
    return ((val - oldMin) / (oldMax - oldMin)) * (newMax - newMin) + newMin


def main():
    global walls
    running = True
    for i in range(10):
        walls.append(
            Wall(random.randint(10, 590), random.randint(10, 590), random.randint(10, 590), random.randint(10, 590)))
    walls.append(Wall(-1, 0, -1, Screen_Height))
    walls.append(Wall(0, 0, Screen_Length, 0))
    walls.append(Wall(0, Screen_Height, Screen_Length, Screen_Height))
    walls.append(Wall(Screen_Length, 0, Screen_Length, Screen_Height))
    a = Avatar(60)
    speed = 0
    rotation = 0
    while running:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                #pygame.display.quit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    rotation = 5
                elif event.key == pygame.K_LEFT:
                    rotation = -5
                elif event.key == pygame.K_DOWN:
                    speed = -5
                elif event.key == pygame.K_UP:
                    speed = 5
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    rotation = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    speed = 0
        screen.fill((0, 0, 0))
        for w in walls:
            w.show()
        a.updatePos(a.pos.x + speed * math.cos(math.radians(a.angle)),
                    a.pos.y + speed * math.sin(math.radians(a.angle)))
        a.rotate(rotation)
        a.show()
        a.showRays()
        rectLength = Screen_Length / a.fov
        for i in range(len(a.lengths)):
            r = pygame.Rect(0, 0, 0, 0)
            r.height = mapVal(a.lengths[i]*2, 0, Screen_Length*2, Screen_Height - 40, 0)
            r.width = rectLength
            r.center = (Screen_Length + (i * rectLength) - (rectLength / 2), Screen_Height // 2)
            color = (mapVal(a.lengths[i], 0 , Screen_Height, 255,0), mapVal(a.lengths[i], 0 , Screen_Height, 255,0),mapVal(a.lengths[i], 0 , Screen_Height, 255,0))
            pygame.draw.rect(screen, color, r)
            pygame.draw.circle(screen, (255, 0, 0), (int(Screen_Length + (i * rectLength) - (rectLength / 2)), Screen_Height // 2), 1, 1)

    pygame.quit()


if __name__ == "__main__":
    main()
