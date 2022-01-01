import pygame as pg

pg.init()
pg.display.set_caption("Space Shooter")
display = pg.display.set_mode((960, 640))

background = pg.image.load("background.jpg")
background = pg.transform.scale(background, (960, 9600))

x = 0; y = 0

running = True

while running:
    y += 1

    if y == 9600:
        y = 0

    display.blit(background, (x, y))
    display.blit(background, (0, y - 9600))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    pg.display.update()

pg.quit()