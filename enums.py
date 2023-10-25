#!/bin/python3

from enum import Enum

class Upgrade(Enum):
	salvage = 0
	weatherproof = 1
	focus = 2
	scanner = 3
	stealth = 4
	discount = 5
	autobomb = 6
	plating = 7
	artifact = 8
	blink = 9
	extra_pow = 11
	fortune = 12
	reserves = 13
	quickening = 15
	scrap_runner = 16
	capacity = 17

class Keyword (Enum):
	piercing = 0
	ricochet = 1
	split = 2
	homing = 3
	triple = 4
	knockback = 5
	giant = 6
	reflective = 7
	charges = 8
	wider = 9
	chain = 10
	shotgun = 11
	finale = 12
	crossbeams = 13
	twinshooter = 14
	pulsewaves = 15
	overheat = 16
	shrapnel = 17
	phasing = 18
	surge = 19
	bursts = 20
	quick = 21
	gatling = 22
	backblast = 37
	high = 43
	backshot = 45

"""
missing :
freeze
akashic
antimagic
consecrated
disrupting
infested
align
swarming
instant hit
overcharge
drag
continuous
bloodlust
heavy
lunge
chariot
instant recall
lance
shieldfield
ringshor
auto hammer

all unique keywords and curses
"""

class Floor(Enum):
	#(excavation) = 0 ??
	#(excavation) = 1 ??
	tutorial = 2
	hub = 3
	excavation = 4
	archives = 5
	maintenance_system = 6
	bellows = 7
	sanctum = 8
	#??? = 9
	the_conduit = 10
	temple = 11
	nowhere = 12
	d13_battle = 13

class Weapon(Enum):
	olddefault = 0
	vulcan = 1
	fireball = 2
	laser = 3
	sword = 4
	charge = 5
	revolver = 6
	razor = 7
	skully = 100
	#missing a few
