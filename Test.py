import pygame, math, random, matplotlib, gym, time

__author__ = "21fernando"
# initialize py game module
pygame.init()

# create the screen
Screen_Length = 600
Screen_Height = 600
screen = pygame.display.set_mode((Screen_Length, Screen_Height))
pygame.display.set_caption("TEST")

def drawGradientPoly(tl: tuple, tr: tuple, bl: tuple , br: tuple, maxrgb: tuple, minrgb:tuple):
    num = tr[0] - tl[0]
    diff = ((maxrgb[0]-minrgb[0])/num,(maxrgb[1]-minrgb[1])/num,(maxrgb[2]-minrgb[2])/num )
    leftLength = abs(tl[1]-bl[1])
    rightLength = abs(tr[1]-br[1])
    growing = ( rightLength > leftLength)
    prevcolor = minrgb if growing else maxrgb
    for i in range(num):
        ydiff  = (tl[1]-tr[1])/num
        color = tuple(map(lambda i, j: i + j, prevcolor, diff)) if growing else tuple(map(lambda i, j: i - j, prevcolor, diff))
        pygame.draw.line(screen, color, (tl[0] + i, tl[1]-i*ydiff), (bl[0] + i, bl[1]+i*ydiff) )
        prevcolor = color
def main():
    running = True
    while running:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        points = [(100,100),(100,200),(200,250), (200,50)]
        '''for i in range(100):
            pygame.draw.line(screen, (255-2*i,255-2*i,255-2*i), (100+i, 100-i), (100+i, 200+i))'''
        #drawGradientPoly((100,50), (200,100), (100,250), (200, 200), (255,255,255), (0,0,0))
        tl = (100,50)
        bl = (100,250)
        tr = (200,100)
        br = (200, 200)
        pygame.draw.polygon(screen,(255,255,255), [tl, tr, br, bl] )
    pygame.quit()


if __name__ == "__main__":
    main()
