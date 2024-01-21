# Savefile Tool : Alpha Release

Python scripts to decode Star of Providence, (formerly known as Monolith) save files  
This is an alpha, Some values are not yet documented and there might bugs

## ⚠️ Warning ⚠️

The Run savefile contains some information that gets copied back to your permanent savefile when you end/quit the run  
For this reason, it is not recommended that you load previous run files and that you only load savefiles that you created  
Doing otherwise might result in data loss (I've experienced some of it myself)

## requirements
- python3

## How to use

Download the repo with git or by using the download zip button  
open a terminal in the extracted/cloned folder  

to decode a gamesave.d13 file execute `python3 gamesave.py -d -i PATH_TO_GAMESAVE_D13`.  
This will output a json file to your terminal, You can put it into a text editor and modify your savefile.  
Once you are done editing save it somewhere and do `python3 gamesave.py -i PATH_TO_JSON_FILE`  
This will output the gamesave.d13 file to your terminal  

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

after either of those commands, send EOF (CTRL+Z ENTER on windows/CTRL+D on unix like oses)  
  
alternatively you can redirect the sandard input and or output  
  
## Options
*	`-i|--input input_file` read from `input_file` instead of stdin  
*	`-d|--decode` decode an entry instead of encoding it  
*	`-v|--verbose` to display additional information on stderr  
*	`-t|--type` to select the type of entries either `9201` or `2E01`  
*	`-k|--kind` to select the kind of list to decode (weapon/keyword/cartridge/upgrade...)  
*	`-h|--help` displays an help message
