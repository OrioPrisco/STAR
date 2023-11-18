# monolith-savefile

Python scripts to decode Star of Providence, (formerly known as Monolith) save files

## requirements
- python3

## How to use

Download the repo with `https://github.com/OrioPrisco/monolith-savefile` or by using the download zip button  
open a terminal in the extracted/cloned folder  

to decode a gamesave.d13 file execute `python3 gamsave.py -d -i PATH_TO_GAMESAVE_D13`.  
This will output a json file to your terminal, You can put it int oa text editor and modify your savefile.  
Once you are done editing save it somewhere and do `python3 gamsave.py -i PATH_TO_JSON_FILE`  
This will output the gaemsave.d13 file to your terminal  

## Options
*	`-i|--input input_file` read from `input_file` instead of stdin  
*	`-d|--decode` decode a savefile instead of encoding it  
*	`-v|--verbose` to display additional information on stderr  
*	`-h|--help` displays an help message

## Manual decoding

The savefile is a base64 encoded file, with some lines starting with `2E01` or `9201`.  
To decode these lines you can use the `transform.py` script.  

to decode execute `python3 transform.py -d` then paste one or more line of `9201` and/or `2E01` from a monolith savefile
to encode execute `python3 transform.py` then paste one ore more decoded line

ater either of those commands, send EOF (CTRL+Z ENTER on windows/CTRL+D on unix like oses)  
  
alternatively you can redirect the sandard input and or output  
  
## Options
*	`-i|--input input_file` read from `input_file` instead of stdin  
*	`-d|--decode` decode an entry instead of encoding it  
*	`-v|--verbose` to display additional information on stderr  
*	`-t|--type` to select the type of entries either `9201` or `2E01`  
*	`-k|--kind` to select the kind of list to decode (weapon/keyword/cartridge/upgrade...)  
*	`-h|--help` displays an help message
