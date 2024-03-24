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
	charges_faster = 8
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
	syringe = 12
	electrode = 13
	trumpet = 14
	dagger = 15
	member_card = 16
	pickaxe = 17
	hammer = 18
	glowing_rune = 19
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

class Ship(Enum):
	null = 0
	d_13 = 1
	overlord = 2
	chaos = 3
	arena_blaster = 4
	skully = 5

class Active(Enum):
	none = 0
	unstable_catalyst = 1
	ancient_runsetone = 2
	petri_dish = 3
	scrambler = 4
	excavation_kit = 5
	supply_drop = 6
	focusing_lens = 7
	resonating_crystal = 8
	repair_nanites = 9
	prototype_genocide = 10
	cracked_blade = 11
	hunter_array = 12
	golden_gun = 13
	capital_investment = 14
	pulse_reflector = 15
	delivery_drone = 16
	tome_of_pyromancy = 17
	tome_of_cryomancy = 18 # loser magic
	tome_of_geomancy = 19
	tome_of_electromancy = 20
	tome_of_sight = 21
	tome_of_the_abyss = 22
	tome_of_enigmancy = 23
	scanner_2_0 = 24
	voltaic_thruster = 25
	blazing_wreath = 26
	warped_teleporter = 27
	glacial_shard = 28
	demolition_charge = 29
	stormheart = 30
	mini_weapon_trove = 31
	grim_idol = 32
	demon_s_claw = 33
	crystallized_light = 34
	hellfire_barrage = 35
	haunted_blaster = 36
	king_s_ransom = 37
	cleanup_crew = 38

class Unlock(Enum):
	sword = 1001
	razor = 1002
	consecrated_weapons = 1003
	antimagic_weapons = 1004
	disrupting_weapons = 1006
	akashic_weapons = 1005
	deep_freeze_bombs = 1007
	timebombs = 1009
	laser_bombs = 1008
	pulsar = 1023
	thunderhead = 1024
	railgun = 1025
	drill = 1026
	spear = 1027
	runic = 1028
	swarmer_pack = 1029
	mirror = 1011
	beastiary = 1012
	mirror_bomb = 1034
	gold_bomb = 1035
	energy_bomb = 1036
	second_wind = 1010
	care_package = 1030
	""""
	#non togglable ? off on new save presumably
	1012.0,
	1021.0,
	1031.0,
	1022.0,
	1011.0,
	1033.0,
	1018.0,
	1019.0,
	1032.0,
	these must correspond to
	seal 1 - 4
	d13
	loops ?
	sword ship
	chaos ship
	aena blaster
	skully
	intensity
	seeds
	bestiary
	bow ???
	more ?
	"""

class Bomb(Enum):
	# 0 creates a glitched power bomb
	laser = 1
	deep_freeze = 2
	time = 3
	fire = 4
	swarm = 5
	excavation = 6
	gold = 7
	mirror = 8
	energy = 9
	shattering = 10

class Blessing(Enum):
	none = -1
	flame = 0
	frost = 1
	earth = 2
	storm = 3
	sight = 4
	abyss = 5
	enigma = 6

class Blessed(Enum):
	blessed = -1
	normal = 0
	cursed = 1

class Lethality(Enum):
	mild = 0
	intense = 1
	sudden_death = 2
