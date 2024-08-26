import pygame,pymunk,pymunk.pygame_util,sys
pygame.init()

WIDTH,HEIGHT=1000,600
screen=pygame.display.set_mode((WIDTH,HEIGHT))
clock=pygame.time.Clock()
FPS=60
space=pymunk.Space()
draw_options=pymunk.pygame_util.DrawOptions(screen)


class Ball():
    def __init__(self):
        self.body=pymunk.Body()
        self.body.position=(500,300)
        self.shape=pymunk.Circle(self.body,8)
        self.body.velocity=(300,400)
        self.shape.density=1
        self.shape.elasticity=1
        space.add(self.body,self.shape)

    

def draw(space,screen,draw_options):
    screen.fill("black")

    space.debug_draw(draw_options)

ball=Ball()
    
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    

    draw(space,screen,draw_options)
    space.step(1/FPS)
    pygame.display.update()
    clock.tick(FPS)