import pygame
import random
import math
pygame.init()

# initiall values
win_w,win_h=800,600
win=pygame.display.set_mode((win_w,win_h))
pygame.display.set_caption("Space Shooter 2.0")
icon= pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)
bg=pygame.image.load("bg.png")
running=True
is_won=False
score =0
health=5

# main parent class

class Thing:
	def __init__(self,width,hight,x,y,vel,image):
		self.width=width
		self.hight=hight
		self.x=x
		self.y=y
		self.vel=vel
		self.image=image

# player class
class Player(Thing):
	pass

# enemy class
class Enemy(Thing):
	def __init__(self,width,hight,x,y,vel,image):
		self.width=width
		self.hight=hight
		self.x=x
		self.y=y
		self.vel=vel
		self.image=image
		self.side=1
		self.down=False
	def move(self):
		if self.x >= 736 and not self.down:
			self.y+=32
			self.down=True
			self.side=-1
		elif self.x <= 0:
			self.y+=32
			self.down=False
			self.side=1
		self.x+=self.vel*self.side

# bullet class
class Bullet(Thing):
	def __init__(self,width,hight,x,y,vel,image):
		self.width=width
		self.hight=hight
		self.x=x
		self.y=y
		self.vel=vel
		self.image=image
		self.is_fire=False
	def fire(self,window):
		if self.is_fire:
			window.blit(self.image,(self.x,self.y))

# boss class
class Boss(Thing):
	def __init__(self,width,hight,x,y,vel,image):
		self.width=width
		self.hight=hight
		self.x=x
		self.y=y
		self.vel=vel
		self.image=image
		self.down=False
		self.side=1
		self.is_it_the_right_time=False
	def show_boss(self,window):
		if self.is_it_the_right_time:
			window.blit(self.image,(self.x,self.y))
	def boss_movement(self):
		if self.x >= win_w-self.width and not self.down:
			self.y+=32
			self.down=True
			self.side=-1
		elif self.x <= 0:
			self.y+=32
			self.down=False
			self.side=1
		self.x+=self.vel*self.side



# player instance
player=Player(64, 64, win_w//2, win_h-70, 8, pygame.image.load("hero.png"))
# enmy instance
enemy=Enemy(64, 64, random.randint(0,736), random.randint(10,150), 4, pygame.image.load("ufo.png"))
# bullet instance
bullet=Bullet(32, 32, 0, win_h-700, 15, pygame.image.load("bullet.png"))
# boss instance
boss=Boss(128, 128, random.randint(0,736), random.randint(10,150), 5, pygame.image.load("boss.png"))
# another bullet instence for boss. This time boss will shoot   nuke
nuke=Bullet(64,64,boss.x,boss.y,8,pygame.image.load("nuke.png"))
# displaying score, health,winning and game over masage
font=pygame.font.Font("freesansbold.ttf",32)
def show_score(win):
	text=font.render("Score: "+str(score),True,(255,255,255))
	win.blit(text,(0,0))
def show_health(win):
	text=font.render("Health: "+str(health),True,(255,255,255))
	win.blit(text,(0,32))
font2=pygame.font.Font("freesansbold.ttf",64)
def won(win,score):
	if score >= 150:
		text=font.render("YOU WIN :)",True,(255,255,255))
		win.blit(text,(win_w*.33,win_h//2))

	
# main draw function
def draw():
	win.blit(bg,(0,0))
	if not(is_won):
		win.blit(player.image,(player.x,player.y))
		if not(boss.is_it_the_right_time):
			win.blit(enemy.image,(enemy.x,enemy.y))
		boss.show_boss(win)
		bullet.fire(win)
		nuke.fire(win)
	show_score(win)
	show_health(win)
	won(win, score)
	pygame.display.update()

def is_collusion(x1,x2,y1,y2,width_of_the_target):
	distance=math.sqrt((math.pow(x1-y1,2))+(math.pow(x2-y2,2)))
	if distance <= width_of_the_target*0.75:
		return True


#main loop
while running:
	pygame.time.delay(40)
	for event in pygame.event.get():
		if event.type== pygame.QUIT:
			running= False
	# player movement
	keys=pygame.key.get_pressed()
	if keys[pygame.K_RIGHT] and player.x < win_w - player.width:
		player.x+=player.vel
	elif keys[pygame.K_LEFT] and player.x >= player.vel:
		player.x-=player.vel
	if keys[pygame.K_SPACE]:
		if not (bullet.is_fire):
			bullet.is_fire=True
			bullet.x=player.x+16
	# enemy and boss movement
	if not (is_won):
		if not (boss.is_it_the_right_time):
			enemy.move()
			collusion=is_collusion(enemy.x, enemy.y, bullet.x, bullet.y, enemy.width)
			if collusion :
				bullet.y=win_h-70
				bullet.is_fire=False
				enemy.x=random.randint(0, 736)
				enemy.y=random.randint(10,150)
				score +=10
		else :
			boss.boss_movement()
			collusion=is_collusion(boss.x, boss.y, bullet.x, bullet.y, boss.width)
			if collusion :
				bullet.y=win_h-70
				bullet.is_fire=False
				score +=10
				if not(nuke.is_fire):
					nuke.is_fire=True
					nuke.x=boss.x+32

	# bullet movement
	if bullet.is_fire:
		bullet.y-=bullet.vel
	if bullet.y <0:
		bullet.y=player.y
		bullet.is_fire=False
	# nuke movement
	if nuke.is_fire:
		nuke.y+=nuke.vel
	if nuke.y > win_h:
		nuke.y=boss.y
		nuke.is_fire=False
	# is this   time for the boss
	if score >=50:
		boss.is_it_the_right_time=True
	# collusion of player and nuke
	a=is_collusion(player.x, player.y, nuke.x, nuke.y, player.width)
	if a:
		nuke.y=boss.y
		nuke.is_fire=False
		health-=1
	# is this won
	if score == 150:
		is_won=True
	draw()
pygame.quit()
