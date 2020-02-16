import pygame, math, random
__author__ = "21fernando"
# initialize pygame module
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

playerImg = pygame.image.load("spaceship.png")
playerX = 370
playerY = 480
playerXSpeed = 0

def player(x,y):
    screen.blit(playerImg, (x, y))

invaderImg = pygame.image.load("invader.png")
invaderX= random.randint(64, 740)
invaderY = 50
invaderYSpeed = 0

def invader(x,y):
    screen.blit(invaderImg, (x,y))

def main():
    global playerX, playerY, playerXSpeed, playerYSpeed, invaderX, invaderY, invaderXSpeed, invaderYSpeed, screen
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                   playerXSpeed  = -5
                if event.key == pygame.K_RIGHT:
                    playerXSpeed = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    playerXSpeed = 0
        playerX += playerXSpeed
        if(playerX>740):
            playerX = 740
        elif(playerX<0):
            playerX = 0
        player(playerX, playerY)
        invader(invaderX, invaderY)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()