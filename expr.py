#!/usr/bin/python

from random import randint
from random import uniform
from random import random
from sys import maxsize

alphabet = '0123456789+-/*()  +-/*().f\\x                '
target = 1234567

world_size = 100
startNewWorldWith = 10
chromosome_length = 9
gene_length = 4
numFittest = 10
crossoverAnywhere = False
pCrossover = 0.25
pMutation = 0.05
maxGenerations = 200
maxHistory = 5
epsilon = 0.0001

generation = 0

#def pickOne (world):
#	max = sum(c[1][2] for c in world)
#	pick = uniform(0, max)
#	current = 0
#	for i in range(0, len(world)):
#		current += world[i][1][2]
#		if current > pick:
#			return world[i]
#			return world.pop(i)

def pickOne (world):
	pick = int(round(uniform(0, len(world)-1)))
	return world[pick]

def getGene (s, i):
	a = i*gene_length
	b = (i+1)*gene_length
	c = s[a:b]
	gene = int(c, 2)
	return gene

def fitness (s):
	expr = ''
	result = 0
	for i in range(0, chromosome_length):
		gene = getGene(s, i)
		try:
			expr += alphabet[gene]
		except IndexError:
			result = 2**63-1
			return [expr, result, 0.0]

	try:
		result = eval(expr)
	except SyntaxError:
		result = 0.0
		return [expr, result, 0.0]
	except ZeroDivisionError:
		result = 0.0
		return [expr, result, 0.0]
	except TypeError:
		result = 0.0
		return [expr, result, 0.0]
	except OverflowError:
		result = 0.0
		return [expr, result, 0.0]
	except NameError:
		result = 0.0
		return [expr, result, 0.0]
	except AttributeError:
		result = 0.0
		return [expr, result, 0.0]

	try:
		fit = 1.0/abs(target-result)
	except ZeroDivisionError:
		fit = 2**63-1
	except OverflowError:
		fit = 0.0
	except TypeError:
		return [expr, result, 0.0]

	return [expr, result, fit]

def spawn ():
	s = ''
	for i in range(0, chromosome_length*gene_length):
		s = s+(chr(randint(0, 1)+0x30))
	return [s, fitness(s)]

def populate (world, size):
	for i in range(0, size):
		world.append(spawn())

def pickFittest (w, n):
	w.sort(key = lambda x: x[1][2]) 
	i = len(w) - n
	j = len(w)
	return w[i:j]

def bestFit (world):
	w = pickFittest(world, 1)
#	print "Best fit: "+str(w[0][1][2])
	return w[0][1][2]

def bestResult (world):
	w = pickFittest(world, 1)
	return w[0][1][1]

def multiply (dad, mom):
	offspring = ''
	pickFrom = dad
#	print "Adam:    "+str(adam)
#	print "Eve:     "+str$a(eve)
	crossOvers = []
	for i in range(0, gene_length*chromosome_length):
		if (crossoverAnywhere or (i % gene_length == 0)):
			if (random() <= pCrossover):
				crossOvers.append(i)
				if (pickFrom == dad):
					pickFrom = mom
				else:
					pickFrom = dad
		offspring = offspring + pickFrom[0][i]
#	print "Offspring: "+offspring
	mutations = []
	for j in range(0, len(offspring)):
		if (random() <= pMutation):
			mutations.append(j)
#			print "Mutation at " + str(j)
#			print "From:      " + offspring
			if (offspring[j] == '0'):
				c = '1'
			else:
				c = '0'
			offspring = offspring[0:j] + c + offspring[j+1:]
#			print "To:        " + offspring
	return [offspring, fitness(offspring), dad, mom, crossOvers, mutations]

def breed (fittest):
	populate(world, startNewWorldWith)
	for i in range(startNewWorldWith, world_size):
		dad = pickOne(fittest)
		mom = pickOne(fittest)
		offspring = multiply(dad, mom)
		world.append(offspring)
	return world

def printWorld (world):
	for i in range(0, len(world)):
		p = world[i]
		chromosome = p[0]
		v_fit = p[1]
		print "chromosome: " + chromosome + ", fitness: " + str(v_fit[2]) + ", expr: " + str(v_fit[0]) + ", result: " + str(v_fit[1])

def printChromosome (chromosome, indent):
	if ((len(indent) / 2) >= maxHistory):
		return

	colorMut = "\x1B["+str(31 + ((len(indent) / 2) % 6))+'m'
	colorOn = "\x1B["+str(91 + ((len(indent) / 2) % 6))+'m'
	colorOff = "\x1B[0m"

	if (len(chromosome) > 2):
		mom = chromosome[2]
		dad = chromosome[3]
		xOvers = chromosome[4]
		muts = chromosome[5]
		printChromosome(dad, indent+'D ')
		printChromosome(mom, indent+'M ')
		print indent+colorOn+"Crossovers: "+str(xOvers) + ", Mutations: "+str(muts)+colorOff
		bits = ''
		bXover = False
		bMutation = False
		for i in range(0, chromosome_length*gene_length):
			if (i in xOvers):
				bXover = not bXover
				if (bXover):
					bits = bits + "\x1B[4m"
				else:
					bits = bits + "\x1B[24m"
			if (i in muts):
				bits = bits + colorMut
				bMutation = True
			else:
				bMutation = False
			bits = bits + chromosome[0][i]
			if (bMutation):
				bits = bits + colorOn
			if ((i+1) % gene_length == 0):
				bits = bits + ' '
		if (bXover):
			bits = bits + "\x1B[24m"
	else:
		bits = ''
		for i in range(0, chromosome_length):
			p = i*gene_length
			q = (i+1)*gene_length
			bits = bits + chromosome[0][p:q]+' '

	v_fit = chromosome[1]
	print indent+colorOn+"chromosome: " + bits + ", expr: " + str(v_fit[0]) + ", result: " + str(v_fit[1]) + ", fitness: " + str(v_fit[2])+colorOff
#	print indent+colorOn+bits+", Expr: "+str(v_fit[0])+colorOff

def printWorldHistory (world):
	for i in range(0, len(world)):
		printChromosome(world[i], '')

world = []
populate(world, world_size)
printWorld(world)
print "\n"

#while (bestFit(world) < 1):
#while (bestResult(world) != target):
while (abs(bestResult(world) - target) > epsilon):
	fittest = pickFittest(world, numFittest)
	print "Generation: " + str(generation)+", best fitness: "+str(bestFit(world))
	world = []
	world = breed(fittest)
	generation = generation + 1
	if (generation == maxGenerations):
		break

world.sort(key = lambda x: x[1][2])
printWorld(world)

winner = pickFittest(world, 1)
printWorldHistory(winner)

print "Finished at generation: "+str(generation)

bits = winner[0][0]
expr = winner[0][1][0]
result = winner[0][1][1]
fitness = winner[0][1][2]

sOut  = str(target) + "\t"
sOut += str(result)+"\t"
sOut += str(generation)+"\t"
sOut += expr+"\t"
sOut += str(fitness)+"\t"
sOut += bits+"\t"
sOut += str(world_size)+"\t"
sOut += str(startNewWorldWith)+"\t"
sOut += str(chromosome_length)+"\t"
sOut += str(gene_length)+"\t"
sOut += str(numFittest)+"\t"
sOut += str(crossoverAnywhere)+"\t"
sOut += str(pCrossover)+"\t"
sOut += str(pMutation)+"\t"
sOut += str(maxGenerations)+"\t"
sOut += alphabet+"\n"

fo = open("genalg.log", "a")
fo.write(sOut)
fo.close()

