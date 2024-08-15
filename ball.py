import pymunk,pygame,math,sys
import pymunk.pygame_util

pygame.init()

width,height=900,700
screen=pygame.display.set_mode((width,height))
clock=pygame.time.Clock()

def calc_distance(p1,p2):
     return math.sqrt((p2[1]-p1[1])**2 + (p2[0]-p1[0])**2)
     
def calc_angle(p1,p2):
     return math.atan2(p2[1]-p1[1],p2[0]-p1[0])   #angle in radins

def draw(space,screen,draw_options,line):  #help in drawing on the screen stuff calc by pymunk
     screen.fill("black")

     if line:
         pygame.draw.line(screen,"yellow",line[0],line[1],3)

     space.debug_draw(draw_options)


def obstacles(shape,width,height):
    RED=(225,0,0,100)
    rects=[
        [(220,height-150),(40,200),RED,10],   #left
        [(400,height-150),(40,200),RED,10],  #right
        [(300,height-240),(250,40),RED,10],   #top
        ]
    for pos,size,color,mass in rects :
        body=pymunk.Body()
        body.position=pos
        shape=pymunk.Poly.create_box(body,size)
        shape.color=color
        shape.mass=mass
        shape.elasticity=0.8
        shape.friction=0.4
        space.add(body,shape)
    

def create_boundaries(space,width,height):   #making sqaure boundaries
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
          shape.elasticity=0.9
          shape.friction=0.3
          space.add(body,shape)


def create_ball(space,radius,mass,pos):
     body=pymunk.Body(body_type=pymunk.Body.STATIC)
     body.position=pos
     shape=pymunk.Circle(body,radius)
     shape.elasticity=1.2
     shape.friction=0.4
     shape.mass=mass
     shape.color=(255,255,255,255)
     space.add(body,shape)   #here the shapeis attach to body and will act acc to body
     return shape

space=pymunk.Space()
space.gravity=(0,981)
draw_options=pymunk.pygame_util.DrawOptions(screen)  #pymunk calculate and drw stuff through pygame on screen

pressed_pos=None
ball=None
create_boundaries(space,width,height)
obstacles(space,width,height)

while True:
    
    line=None
    if ball and pressed_pos:
        line=[pressed_pos,pygame.mouse.get_pos()]

    for event in pygame.event.get():
            if event.type==pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
               if not ball:
                pressed_pos=pygame.mouse.get_pos()
                ball=create_ball(space,5,10 ,pressed_pos)
               elif pressed_pos:
                ball.body.body_type=pymunk.Body.DYNAMIC
                angle=calc_angle(*line)
                force=calc_distance(*line) *700
                fx=math.cos(angle)*force      #watch tech with tim pymunk tutorial (46:00)
                fy=math.sin(angle)*force
                ball.body.apply_impulse_at_local_point((-fx,-fy),(0,0))  #apllyin force of 10000 in x direction  at center of the ball
                pressed_pos=None
               else:
                   space.remove(ball,ball.body)
                   ball=None
                   pressed_pos=None

    draw(space,screen,draw_options,line)   #just this draws all the shape and body
    space.step(1/60) # how fast the simulation will run in 1 sec
    pygame.display.update()
    clock.tick(60) 
