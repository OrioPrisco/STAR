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
	second_wind = 10
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
	ringshot = 23
	instant_recall = 24
	shielded = 25
	lance = 26
	chariot = 27
	heavy = 28
	bloodlust = 29
	freeze = 30
	continuous = 31
	align = 32
	consecrated = 33
	antimagic = 34
	akashic = 35
	disrupting = 36
	backblast = 37
	infested = 38
	swarming = 39
	drag = 40
	instant_hit = 41
	overcharge = 42
	high_caliber = 43
	hit_streak = 44
	backshot = 45
	wall_breaker = 46
	all_pierce = 47
	holy = 48
	hunter = 49
	ammo_leak = 50
	ammo_steal = 51
	super_galactic = 52
	heaven_piercing = 53
	all_blast = 54
	echo = 55
	unstable = 56
	sticky_bombs = 57
	remote_trigger = 58
	lunge = 59
	pin = 60
	enigmatic = 61 # overrides other keywords
	excavate = 62
	auto_hammer = 63
	curse_of_pain = 64
	curse_of_numbness = 65
	curse_of_fatigue = 66
	curse_of_stiffness = 67
	curse_of_haphephobia = 68
	curse_of_paranoia = 69
	curse_of_chaos = 70
	sharpshooter = 71
	impale = 72
	sacred = 73
	entropic = 74

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
	unknown = 9
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
	pulsar = 8
	thunderhead = 9
	railgun = 10
	drill = 11
	spear = 12
	runic = 13
	bow = 14 # SCRAPPED
	grenade = 15 # SCRAPPED
	skully = 100

class Cartridge(Enum):
	magnifying_glass = 0
	firecracker = 1
	victory_sign = 2
	golden_star = 3
	cool_sunglasses = 4
	spyglass = 5
	hat = 6
	plate = 7
	_13_leaf_clover = 8
	mining_hat = 9
	rocket = 10
	cloak = 11
	dagger = 15
	member_card = 16
	pickaxe = 17
	hammer = 18
	glowing_run = 19
	treasure_chest = 20
	err_integer_overflow = 21
	battery = 22
	broken_mirror = 23
	crowbar = 24
	gun = 25
	calculator = 26
	bulwark = 27
	plug = 28
	braveheart = 29
	scope = 30
	crackshot = 31
	reflector = 32
	garbage_data = 33
	magic_sword = 34
	magic_shield = 35
	magic_rod = 36
	magic_pack = 37
	temple_game = 38
	power_core = 39
	iron_heart = 40
	transfusion = 41
	credit_card = 42
	bandage = 43
	contract = 44

class Unique(Enum):
	white_death = 1
	dragon_breath = 2
	donner = 3
	latafayn = 4
	snowblower = 5
	gun_with_no_name = 6
	iron_fist = 7
	shockwave = 8
	gorynich = 9
	sueela = 10
	lidenbrock = 11
	longinus = 12
	eternal_vigil = 13
	chronoton = 14
	purifier = 15
	luxor = 16
	excalibur = 17
	genocide = 18
	headhunter = 19
	the_claw = 20
	twinwave = 21
	black_hole = 22
	solaris = 23
	crimson_lotus = 24
	thousand_needles = 25
	councils_blessing = 26
	worlds_largest_gun = 27
	worldfire = 28
	bonechill = 29
	phantom_edge = 30
	atomica = 31
	detonator = 32
	delta = 33
	soundwave = 34
	corona = 35
	zephyr = 36
	excavator = 37
	painstaker = 38
	#shockwave = 39 # ? crashed, somethingto do with angle.
	polar_star = 40
	ace_of_swords = 41
	sacred_arms = 42
	grasp_of_entropy = 43
	edge_of_reality = 44
