from pyweb import pydom
import gamesave

def decode_gamesave(event):
	gamesave = pydom["#gamesave_d13"][0].value
	print(gamesave)
	
