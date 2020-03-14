import pygame, math, random

__author__ = "21fernando"
# initialize pygame module
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# Player declaration
playerImg = pygame.image.load("SpaceInvaders/spaceship.png")
playerX = 370
playerY = 480
playerXSpeed = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Background declaration
background = pygame.image.load("SpaceInvaders/galaxy.jpg")

# Invader declaration
invaderImg = []
invaderX = []
invaderY = []
invaderYSpeed = []
invaderXSpeed = []
numInvaders = 6
for i in range(numInvaders):
    invaderImg.append(pygame.image.load("SpaceInvaders/invader.png"))
    invaderX.append(random.randint(200, 500))
    invaderY.append(50)
    invaderYSpeed.append(20)
    invaderXSpeed.append(5)


def invader(x, y, i):
    screen.blit(invaderImg[i], (x, y))


# Bullet delcaration
bulletImg = pygame.image.load("SpaceInvaders/laser.png")
bulletX = 0
bulletY = playerY
bulletXSpeed = 0
bulletYSpeed = 13
bulletShot = False


def fireBullet(x, y):
    global bulletShot
    bulletShot = True
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(ix, iy, bx, by):
    return math.sqrt(math.pow((ix - bx), 2) + math.pow((iy - by), 2)) < 27


def main():
    global playerX, playerY, playerXSpeed, playerYSpeed, invaderX, invaderY, invaderXSpeed, invaderYSpeed, screen, bulletX, bulletY, bulletXSpeed, bulletYSpeed, bulletShot
    running = True
    while running:
        screen.fill((0, 0, 0))
        # screen.blit(background,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerXSpeed = -10
                if event.key == pygame.K_RIGHT:
                    playerXSpeed = 10
                if event.key == pygame.K_SPACE:
                    if (not bulletShot):
                        fireBullet(playerX, bulletY)
                        bulletX = playerX
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    playerXSpeed = 0
        # player movement
        playerX += playerXSpeed
        if (playerX >= 740):
            playerX = 740
        elif (playerX <= 0):
            playerX = 0
        player(playerX, playerY)

        # bullet movement
        if (bulletShot):
            fireBullet(bulletX, bulletY)
            bulletY -= bulletYSpeed
        if bulletY <= 0:
            bulletY = 480
            bulletShot = False
        pygame.display.update()

        # invader movement
        for i in range(numInvaders):
            invaderX[i] += invaderXSpeed[i]
            if (invaderX[i] >= 740 or invaderX[i] <= 0):
                invaderXSpeed[i] *= -1
                invaderY[i] += invaderYSpeed[i]
            # Collision
            collision = isCollision(invaderX[i], invaderY[i], bulletX, bulletY)
            if (collision):
                bulletY = 480
                bulletShot = False
                invaderX[i] = random.randint(200, 500)
                invaderY[i] = 50
                invaderXSpeed[i] = -1 * abs(invaderXSpeed[i])
            invader(invaderX[i], invaderY[i], i)
    pygame.quit()

if __name__ == "__main__":
    main()