import pymunk,pygame,pymunk.pygame_util,sys
pygame.init()

width,height=900,700
FPS=60
GRAVITY=(0,0)
screen=pygame.display.set_mode((width,height))
clock=pygame.time.Clock()

def draw(space,screen,draw_options):
    screen.fill('black')
    space.debug_draw(draw_options)

def add_ball(space,radius,mass,pos):
    global body
    body=pymunk.Body()
    body.position=pos
    body.velocity=200,-350
    shape=pymunk.Circle(body,radius)
    shape.friction=0
    shape.elasticity=1
    shape.mass=mass
    shape.color=(255,255,255,255)
    space.add(body,shape)
    return shape


def boundaries(space,width,height):
    rects=[                     #rects=((position),(size))
          [(width/2,height-10),(width,20)],
          [(width/2,10),(width,20)],
          [(10,height/2),(20,height)],
          [(width-10,height/2),(20,height)]
        
          ]
    for pos,size in rects:
          body=pymunk.Body(body_type=pymunk.Body.STATIC)  #static doent need body mass
          body.position=pos
          shape=pymunk.Poly.create_box(body,size)
          shape.elasticity=1
          shape.friction=0
          shape.color=(255,255,255,255)
          space.add(body,shape)

space=pymunk.Space()
draw_options=pymunk.pygame_util.DrawOptions(screen)
space.gravity=GRAVITY

ball=add_ball(space,7,10,(450,100))
boundaries(space,width,height)

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw(space,screen,draw_options)
    space.step(1/FPS)
    pygame.display.update()
    clock.tick(FPS)

