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
    body=pymunk.Body()
    body.position=pos
    body.velocity=300,100
    shape=pymunk.Circle(body,radius)
    shape.friction=0
    shape.elasticity=1
    shape.mass=mass
    shape.color=(255,255,255,255)
    space.add(body,shape)
    return shape

def side_things(space,pos):
    body=pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position=pos
    
    shape=pymunk.Poly.create_box(body,(10,50))
    shape.elasticity=1
    shape.mass=100
    shape.color=(255,255,255,255)
    space.add(body,shape)
    return body



def boundaries(space,width,height):
    rects=[                     #rects=((position),(size))
          [(width/2,height-10),(width+30,20)],
          [(width/2,10),(width+30,20)],
          ]
    for pos,size in rects:
          body=pymunk.Body(body_type=pymunk.Body.KINEMATIC)  #static doent need body mass
          body.position=pos
          shape=pymunk.Poly.create_box(body,size)
          shape.elasticity=1
          shape.friction=0
          shape.color=(255,255,255,255)
          space.add(body,shape)

space=pymunk.Space()
draw_options=pymunk.pygame_util.DrawOptions(screen)
space.gravity=GRAVITY

ball=add_ball(space,7,1,(450,100))
boundaries(space,width,height)
body_left = side_things(space,(10, 100))
body_right = side_things(space,(890, 100))
left_move_up=False
left_move_down=False
right_move_up=False
right_move_down=False
speed=300
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_z:
                left_move_up=True
            if event.key==pygame.K_x:
                left_move_down=True
            if event.key==pygame.K_n:
                right_move_up=True
            if event.key==pygame.K_m:
                right_move_down=True
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_z:
                left_move_up=False
            if event.key==pygame.K_x:
                left_move_down=False
            if event.key==pygame.K_n:
                right_move_up=False
            if event.key==pygame.K_m:
                right_move_down=False
        
    left_speed=0
    right_speed=0

    if left_move_up:
        left_speed=-speed
    if left_move_down:
        left_speed=speed
    if right_move_up:
        right_speed=-speed
    if right_move_down:
        right_speed=speed
        

    body_left.velocity=(0,left_speed)
    body_right.velocity=(0,right_speed)

    if body_left.position.y<=0:
        body_left.position=(10,0)


    



    draw(space,screen,draw_options)
    space.step(1/FPS)
    pygame.display.update()
    clock.tick(FPS)

