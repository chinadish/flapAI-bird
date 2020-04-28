import pygame
from pygame.locals import *
from player import Player
from player import Obstacle
import cfg
from random import randint

gap = cfg.ggap

black = (0,0,0)
white = (255,255,255)
blue = (150, 250, 255)





def main():
	pygame.init()
	screen = pygame.display.set_mode((cfg.SCREEN_W,cfg.SCREEN_H))
	pygame.display.set_caption('Flappy!')

	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill(blue)

	bird = Player()

	obgroup = pygame.sprite.Group()

	screen.blit(background, (0, 0))
	
	screen.blit(bird.surf, bird.rect)

	pygame.display.flip()


	done = False
	clock = pygame.time.Clock()
	delta = clock.tick(60)

	myfont = pygame.font.Font(None, 40)




	while not done:

		scoretext = myfont.render("Score: "+str(cfg.score), 0, (0,0,0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					bird.jump()
				if event.key == K_ESCAPE:
					done = True
		if cfg.create == True:
			ob = Obstacle(randint(gap + cfg.SCREEN_H/12, cfg.SCREEN_H*11/12))
			obgroup.add(ob)

			cfg.create = False

		bird.update()
		obgroup.update()

		for each in obgroup:
			if (bird.rect.colliderect(each.rect1)) or (bird.rect.colliderect(each.rect2)):
				bird.dead = True

		if bird.dead == True:
				done = True


		screen.blit(background, (0,0))
		screen.blit(bird.surf, bird.rect)




		for each in obgroup:
			screen.blit(each.surf1, each.rect1)
			screen.blit(each.surf2, each.rect2)

		screen.blit(scoretext, (5, 10))


		pygame.display.flip()
		cfg.delta = clock.tick(60)

main()
pygame.quit()
