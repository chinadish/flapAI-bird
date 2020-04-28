import numpy as np

#CONSTANTS

SCREEN_W = 1200
SCREEN_H = 900
ggap = SCREEN_H/5
sizes = [3,2,1]
SPAWN = SCREEN_W/15

#HACKY VARIABLES

delta = 0
create = True
score = 0
travelled = 0
analysis = np.array([0,0,0])							# the input data for the network! dist to pipe, 10 x height of (bird - next hole), 100 x bird vertical v

def resdefault():										# used to reset all changing cfg variables for each run (I don't know the canonical way to do this)
	global delta
	global create 
	global score
	global travelled 
	global analysis 


	delta = 0
	create = True
	score = 0
	travelled = 0
	analysis = np.array([0,0,0])	

#def init():
#	global clock
#	clock = pygame.time.Clock()