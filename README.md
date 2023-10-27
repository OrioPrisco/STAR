# monolith-savefile

Python scripts to decode and reencode `9201` and `2E01` entries from monolith save files

## requirements
- python3

## How to use

Download the repo with `https://github.com/OrioPrisco/monolith-savefile` or by using the download zip button  
open a terminal in the extracted/cloned folder  

to decode execute `python3 transform.py -d` then paste one or more line of `9201` and/or `2E01` from a monolith savefile
to encode execue `python3 transform.py` then paste one ore more decoded line

ater either of those commands, send EOF (CTRL+Z ENTER on windows/CTRL+D on unix like oses)  
  
alternatively you can redirect the sandard input and or output  
  
## Options
*	`-i|--input input_file` read from `input_file` instead of stdin  
*	`-v|--verbose` to display additional information on stderr  
*	`-t|--type` to select the type of entries either `9201` or `2E01`  
*	`-t|--type` to select the kind of list to decode (weapon/keyword/cartridge/upgrade)  
*	`-h|--help` displays an help message
