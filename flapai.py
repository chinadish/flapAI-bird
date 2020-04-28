import pygame
from pygame.locals import *
from random import randint
import numpy as np 
import time

from player import Player
from player import Obstacle
import cfg


gap = cfg.ggap
arbitrarystop = 500
black = (0,0,0)
white = (255,255,255)
blue = (150, 250, 255)

def action(model):

	pygame.init()
	screen = pygame.display.set_mode((cfg.SCREEN_W,cfg.SCREEN_H))
	pygame.display.set_caption('FlapAI Bird!')
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill(blue)							#COLOUR
	clock = pygame.time.Clock()
	myfont = pygame.font.Font(None, 40)


	bird = Player()
	obgroup = pygame.sprite.Group()
	screen.blit(background, (0, 0))
	screen.blit(bird.surf, bird.rect)
	pygame.display.flip()

	observed = np.array([[0,0,0]], dtype='f')								# input for the neural net
	
	done = False
	cfg.resdefault()

	while not done:

		scoretext = myfont.render("Score: "+str(cfg.score), 0, (0,0,0))
		

		if cfg.create == True:												# note to self: obstacle needs to be created first before searching for nearest
			ob = Obstacle(randint(gap + cfg.SCREEN_H/12, cfg.SCREEN_H*5/6))
			obgroup.add(ob)
			cfg.create = False

		observed[0][0] = obtainnearestx(obgroup)
		observed[0][1] = obtainhdiff(obgroup, bird)
		observed[0][2] = obtainbvel(bird)

		if model.toflap(np.transpose(observed)):
			bird.jump()

		for event in pygame.event.get():									
			if event.type == pygame.QUIT:
				done = True
			elif event.type == KEYDOWN:
				#if event.key == K_SPACE:									# AI won't be clicking (right?)
				#	bird.jump()
				if event.key == K_ESCAPE:
					done = True

		bird.update()
		obgroup.update()

		for each in obgroup:
			if (bird.rect.colliderect(each.rect1)) or (bird.rect.colliderect(each.rect2)):
				bird.dead = True


		screen.blit(background, (0,0))
		screen.blit(bird.surf, bird.rect)


		for each in obgroup:
			screen.blit(each.surf1, each.rect1)
			screen.blit(each.surf2, each.rect2)

		screen.blit(scoretext, (5, 10))


		pygame.display.flip()
		cfg.delta = clock.tick(60)

		if (cfg.score >= arbitrarystop):
			done = True

		if bird.dead == True:
			done = True

			bird.kill()						# kill bird and obstacles
			for item in obgroup:
				item.kill()

	print("Score: " + str(cfg.score))
	return cfg.travelled




def obtainnearest(pipes):													# finds the nearest pipe							
	closestd = cfg.SCREEN_W
	closestp = Obstacle(cfg.SCREEN_W)
	for pipe in pipes:
		loc = pipe.rect1.x
		if ((loc<closestd) and (loc>0)):
			closestd = loc
			closestp = pipe
	return closestp

def obtainnearestx(pipes):													# given pipes, returns x coord of nearest pipe / 100
	closestp = obtainnearest(pipes)
	return (closestp.rect1.x)/100.0

def obtainhdiff(pipes, bird):												# given pipes, returns height diff between bird and nearest pipe / 10
	closestp = obtainnearest(pipes)
	return (closestp.rect1.y - (bird.rect.y + bird.birdsize))/10.0

def obtainbvel(bird):														# returns bird's y-velocity times delta
	return bird.vely * cfg.delta



#action()
#time.sleep(0.5)
#action()


pygame.quit()
