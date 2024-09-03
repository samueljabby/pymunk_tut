import pymunk,pygame,pymunk.pygame_util,sys,random
pygame.init()

WIDTH,HEIGHT=1000,600
FPS=100
screen=pygame.display.set_mode((WIDTH,HEIGHT))
clock=pygame.time.Clock()
space=pymunk.Space()
# draw_options=pymunk.pygame_util.DrawOptions(screen)

left=50
right=950
top=25
bottom=575
middlex=500
middley=300

class Ball():
   def __init__(self):
      self.body=pymunk.Body()
      self.reset(0,0,0)
      self.shape=pymunk.Circle(self.body,8)
      self.body.velocity=900,-500
      self.shape.density=1
      self.shape.elasticity=1
      space.add(self.body,self.shape)
      self.shape.collision_type=1

   def draw(self):
      x,y=self.body.position
      pygame.draw.circle(screen,(255,255,255),(int(x),int(y)),8)

   def reset(self,space,arbiter,g):
      self.body.position=middlex,middley
      self.body.velocity=700*random.choice([-1,1]),-400*random.choice([-1,1])
      return False


class Wall():
   def __init__(self,p1,p2,collision_number=None):
      self.body=pymunk.Body(body_type=pymunk.Body.STATIC)
      self.shape=pymunk.Segment(self.body,p1,p2,10)
      self.shape.elasticity=1
      space.add(self.body,self.shape)
      if collision_number:
         self.shape.collision_type=collision_number

   def draw(self):
      pygame.draw.line(screen,"white",self.shape.a,self.shape.b,10)

class Player():
   def __init__(self,x):
      self.body=pymunk.Body(body_type=pymunk.Body.KINEMATIC)   #here the start and end point in the segment is relative
      self.body.position=x,middley                             # to the body.position i.e ye body ka pos origin hai
      self.shape=pymunk.Segment(self.body,(0,-50),(0,50),10)
      self.shape.elasticity=1
      space.add(self.body,self.shape)

   def draw(self):
      p1=self.body.local_to_world(self.shape.a)   #in the class the pos is relative local to world srts the real oriign
      p2=self.body.local_to_world(self.shape.b)   #pygame takes the the world origin unlike munk which takes realtive pos
      pygame.draw.line(screen,"white",p1,p2,10)

   def move(self,up=True):
      if up:
         self.body.velocity=0,-1000
      else:
         self.body.velocity=0,1000

   def stop(self):
         self.body.velocity=0,0

   def on_edge(self):
      if self.body.local_to_world(self.shape.a)[1]<=top:   #this is for top shape.a is for tghhe upper part of the shape  and 1 is for checking the y pos cuz shape.a is vector
         self.body.velocity=0,0
         self.body.position=self.body.position[0],top+55
      if self.body.local_to_world(self.shape.b)[1]>=bottom:   #this is for top shape.b is for tghhe lower part of the shape and 1 is for checking the y pos cuz shape.a is vector
         self.body.velocity=0,0
         self.body.position=self.body.position[0],bottom-55


ball=Ball()
wall_left=Wall((left,top),(left,bottom),2)
wall_right=Wall((right,top),(right,bottom),2)
wall_top=Wall((left,top),(right,top))
wall_bottom=Wall((left,bottom),(right,bottom))
player1=Player(left+15)
player2=Player(right-15)


scored=space.add_collision_handler(1,2)  #You are passing the method itself (as a reference) to be called later by the collision handler.
scored.begin=ball.reset

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
          pygame.quit()
          sys.exit()

    screen.fill("black")
    ball.draw()
    wall_left.draw()
    wall_right.draw()
    wall_top.draw()
    wall_bottom.draw()
    player1.draw()
    player2.draw()

    keys=pygame.key.get_pressed()
    if not player2.on_edge():
     if keys[pygame.K_UP]:  #up
        player2.move()

     elif keys[pygame.K_DOWN]: #down
       player2.move(False)
     else:
        player2.stop()

    if not player1.on_edge():
     if keys[pygame.K_w]:
        player1.move()
     elif keys[pygame.K_s]:
        player1.move(False)
     else:
       player1.stop()

    space.step(1/FPS)
    pygame.display.update()
    clock.tick(60)
