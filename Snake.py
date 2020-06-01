import pygame, random, time

__author__ = "21fernando"
# initialize py game module
pygame.init()

# create the screen
Screen_Length = 600
Screen_Height = 600
screen = pygame.display.set_mode((Screen_Length, Screen_Height))
pygame.display.set_caption("SNAKE")

Grid_Width = 30
Grid_Height = 30

Snake_Width = Grid_Width-1
Snake_Height = Grid_Height-1
snakeTail = []

direction = "left"

Apple_Width = Snake_Width
Apple_Height = Snake_Height
Apple_Cor = [0, 0]

Start_Len = 4

lengthening = False
addCount = 0

clock = pygame.time.Clock()

def genSnake():
    global snakeTail
    for i in range(Start_Len):
        snakeTail.append([Screen_Length // 2 + i * Grid_Width, Screen_Height // 2, direction])


def drawSnake():
    global snakeTail, Snake_Width, Snake_Height, screen
    for i in range(len(snakeTail)):
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(snakeTail[i][0], snakeTail[i][1], Snake_Height, Snake_Width))


def checkDeath():
    if snakeTail[0][0] < 0 or snakeTail[0][0] >= Screen_Length or snakeTail[0][1] < 0 or snakeTail[0][1] >= Screen_Height:
        return True
    for i in range(1, len(snakeTail)):
        if snakeTail[i][0] == snakeTail[0][0] and snakeTail[i][1] == snakeTail[0][1]:
            print("on itself")
            return True
    return False


def genApple():
    global Apple_Cor
    Apple_Cor[0] = (Grid_Width * random.randint(1, (Screen_Length - Grid_Width) // Grid_Width))
    Apple_Cor[1] = (Grid_Height * random.randint(1, (Screen_Height - Grid_Height) // Grid_Height))


def drawApple():
    global Apple_Cor
    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(Apple_Cor[0], Apple_Cor[1], Apple_Height, Apple_Width))


def checkEat():
    global lengthening, addCount
    if snakeTail[0][0] == Apple_Cor[0] and snakeTail[0][1] == Apple_Cor[1]:
        lengthening = True
        addCount = 0
        return True


def moveSnake(d):
    global snakeTail, lengthening, addCount
    if lengthening and addCount <= 2:
        addCount += 1
    else:
        snakeTail = snakeTail[:len(snakeTail) - 1]
    if d == "up":
        snakeTail.insert(0, [snakeTail[0][0], snakeTail[0][1] - Grid_Height, "up"])
    elif d == "down":
        snakeTail.insert(0, [snakeTail[0][0], snakeTail[0][1] + Grid_Height, "down"])
    elif d == "left":
        snakeTail.insert(0, [snakeTail[0][0] - Grid_Width, snakeTail[0][1], "left"])
    elif d == "right":
        snakeTail.insert(0, [snakeTail[0][0] + Grid_Width, snakeTail[0][1], "right"])


def main():
    running = True
    genSnake()
    genApple()
    for i in range(3,0,-1):
        print(i ,"...")
        time.sleep(0.2)
    print("GO!")
    time.sleep(0.8)
    while running:
        global direction, movingDirection
        pygame.display.update()
        userInput = ""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    userInput = "right"
                elif event.key == pygame.K_LEFT:
                    userInput = "left"
                elif event.key == pygame.K_DOWN:
                    userInput = "down"
                elif event.key == pygame.K_UP:
                    userInput = "up"
        if (userInput == "right" and direction != "left" or userInput == "left" and direction != "right" or userInput == "down" and direction != "up" or userInput == "up" and direction != "down"):
            direction = userInput
        moveSnake(direction)
        screen.fill((0, 0, 0))
        drawSnake()
        drawApple()
        if checkDeath():
            break
        if checkEat():
            genApple()
        clock.tick(10)
    pygame.quit()


if __name__ == "__main__":
    main()
