import pygame,pymunk,pymunk.pygame_util,sys
pygame.init()

WIDTH,HEIGHT=1000,600
screen=pygame.display.set_mode((WIDTH,HEIGHT))
clock=pygame.time.Clock()
FPS=80
space=pymunk.Space()
draw_options=pymunk.pygame_util.DrawOptions(screen)
bricks_list=[]

left=-2
right=1000
top=-2
bottom=600
middlex=500
middley=300

class Ball():
    def __init__(self):
        self.body=pymunk.Body()
        self.body.position=(500,500)
        self.shape=pymunk.Circle(self.body,8)
        self.body.velocity=(300,-300)
        self.shape.density=1
        self.shape.elasticity=1
        self.shape.collision_type=1
        space.add(self.body,self.shape)

class Wall():
    def __init__(self,p1,p2):
        self.body=pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape=pymunk.Segment(self.body,p1,p2,1)
        space.add(self.body,self.shape)
        self.shape.elasticity=1

class Bricks():
    def __init__(self,x,y,size=(60,35)):
        self.body=pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position=x,y
        self.shape=pymunk.Poly.create_box(self.body,size)
        self.shape.elasticity=1
        self.shape.color=(0,0,0,0)
        space.add(self.body,self.shape)
        self.shape.collision_type=2

    def brick_setup(self,rows=10,cols=16,x_distance=63,y_distance=37,x_offset=28,y_offset=18):
        for index_row,row in enumerate(range(rows)):
            for index_col,col in enumerate(range(cols)):
                x=index_col*x_distance+x_offset
                y=index_row*y_distance+y_offset
                # bricks_list.append(Bricks(x,y))
                Bricks(x,y)

    def breaking_bricks(self,arbiter,space,data):
        brick_shape=arbiter.shapes[1]
        space.remove(brick_shape,brick_shape.body)
        return True



class Player():
    def __init__(self):
        self.body=pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position=500,593
        self.shape=pymunk.Segment(self.body,(-50,0),(50,0),5)
        self.shape.elasticity=1
        space.add(self.body,self.shape)

    def move(self,right):
        if right:
            self.body.velocity=500,0
        else:
            self.body.velocity=-500,0
    def stop(self):
        self.body.velocity=0,0


def draw(space,screen,draw_options):
    screen.fill("white")
    space.debug_draw(draw_options)


#ball
ball=Ball()

#bricks
bricks=Bricks(0,0,(0,0))
bricks.brick_setup()
#walls
wall_left=Wall((left,top),(left,bottom))
wall_right=Wall((right,top),(right,bottom))
wall_top=Wall((left,top),(right,top))
#player
player=Player()
#breaking bricks
scored=space.add_collision_handler(1,2)
scored.post_solve=bricks.breaking_bricks

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys=pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        player.move(True)
    elif keys[pygame.K_LEFT]:
        player.move(False)
    else:
        player.stop()


    draw(space,screen,draw_options)
    space.step(1/FPS)
    pygame.display.update()
    clock.tick(FPS)
