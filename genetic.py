import numpy as np
import cfg
import pickle
from scipy import special
import flapai

RANDOMIZER = (0, 10)															# random distribution for generation
MUTATOR = (1, 0.025)																# random distribution for mutation
NUMBIRDS = 20

class Genetic():																# class of an AI; there will be many instances
	def __init__(self, sizes):
		self.numlayers = len(sizes)
		self.sizes = sizes
		self.setrandom()

	def setrandom(self):														# initialize all w & b; N(RANDOMIZER) distribuition
		self.weights = [RANDOMIZER[1]*np.random.randn(y,x) + RANDOMIZER[0]*np.ones((y,x)) for x,y in zip(self.sizes[:-1],self.sizes[1:])]
		self.biases = [RANDOMIZER[1]*np.random.randn(n,1) + RANDOMIZER[0]*np.ones((n,1)) for n in self.sizes[1:]]

	def setwb(self,w,b):
		self.weights = w
		self.biases = b

	def feedforward(self, a):
		for w,b in zip(self.weights,self.biases):
			a = sigmoid(np.dot(w,a) + b)
		return a

	def toflap(self, a):														# FLAPPING INTERFACE FUNCTION
		x = self.feedforward(a)
		#print(x[0][0])
		if (x >= 0.5):
			return 1
			print("FLAP")
		else:
			return 0

	def record(self):
		log = [cfg.travelled, self.weights, self.biases]						# list: (best score, weights, biases)
		return log

	def load(self, log):
		self.setwb(log[1], log[2])


def mutate(cand, sizes = cfg.sizes):														# returns mutated list
	cand = cand[:]
	cand[0] = 0
	for wb in [1,2]:							# iterating over weights, then over biases
		cand[wb] = cand[wb][:]
		for i in range(len(cand[wb])):
			mut = MUTATOR[1]*np.random.randn(*cand[wb][i].shape) + MUTATOR[0]*np.ones(cand[wb][i].shape)
			cand[wb][i] = cand[wb][i] * mut
	return cand

def child(c1, c2, sizes = cfg.sizes):														# creates & returns child
	c1 = c1[:]
	c2 = c2[:]
	c1[0] = 0
	c2[0] = 0
	for wb in [1,2]:							# iterating over weights, then over biases
		c1[wb] = c1[wb][:]
		c2[wb] = c2[wb][:]
		for i in range(len(c1[wb])):
			scissors = np.random.randint(2, size = c1[wb][i].shape)
			cc = np.ones(c1[wb][i].shape)
			complement = (-1)*scissors + cc
			t1 = c1[wb][i]*scissors + c2[wb][i]*complement
			t2 = c2[wb][i]*scissors + c1[wb][i]*complement
			c1[wb][i] = t1
			c2[wb][i] = t2
	return c1								# returns one child

def generate():																	# returns a list1 of lists2 ; each list2 corresponds to one of  20 AIs, generates if they don't exist
	try:
		with open('knowledge.pkl', 'rb') as f:
			candidates = pickle.load(f)
	except IOError:
		creator = Genetic(cfg.sizes)
		tosave = []
		for i in range(NUMBIRDS):
			creator.setrandom()
			tosave.append(creator.record())
		savelist(tosave)						# all saves are to knowledge.pkl
		candidates = tosave

	return candidates

def epoch():
	candidates = generate()
	if (candidates[0][0] > 3000):				# (AD HOC) choosing natural selection method
		survival(candidates)
	else:
		birth(candidates)
	temp = Genetic(cfg.sizes)
	for candidate in candidates:
		temp.load(candidate)
		candidate[0] = flapai.action(temp)
	candidates.sort(key = lambda x: x[0], reverse = True)
	savelist(candidates)
	return candidates[0][0]


def savelist(clist):							# all saves are to knowledge.pkl
	with open('knowledge.pkl', 'wb') as f:
		pickle.dump(clist, f)

def survival(pool):								# specefically for 20
	pool[4] = child(pool[0],pool[1])
	pool[5] = child(pool[0],pool[2])
	pool[6] = child(pool[0],pool[3])
	pool[7] = child(pool[0],pool[4])
	pool[8] = child(pool[1],pool[2])
	pool[9] = child(pool[1],pool[3])
	for i in range(5):
		pool[i+10] = mutate(pool[i])
		pool[i+15] = Genetic(cfg.sizes).record()

def birth(pool):
	for i in range(5):
		pool[i+5] = child(pool[i], Genetic(cfg.sizes).record())
	for i in range(10,20):
		pool[i] = Genetic(cfg.sizes).record()

def sigmoid(z):
	#return 1.0/(1.0+np.exp(-z))
	return special.expit(z)



# def tester():
# 	candidates = generate()
# 	#flapai.action(Genetic(cfg.sizes))
# 	print(candidates[0])
# 	candidates[1] = child(candidates[0], candidates[2])
# 	print(candidates[0])


for i in range(5):
	print("Best distance of EPOCH #" + str(i+1) + " = " + str(epoch()))
	