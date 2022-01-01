import pygame as pg

pg.init()

pg.display.set_mode((1040, 680))
pg.display.set_caption("Space Shooter")

running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    pg.display.update()