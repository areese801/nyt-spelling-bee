# NYT Spelling Bee

This project does a dictionary attack on the New York Times Spelling Bee Puzzle.  It is only as good as the input dictionary (Websters).

Ironically, the day I wrote it, one of two possible pangrams was not found (because it's not in the dictionary).  That word was `carryout`, which I guess is a compound word, and wasn't (at the time at least) in the dictionary file the program uses.  It did find the other candidate using the standard algorithm: `autocracy`.  I guess there's room for improvement.

## Installation:
```bash 
pip3 install -r requirements.txt
```

## Usage Example
The first letter argument passed in is treated as the 'Center' letter, which must be somewhere in any matching word
```bash
python3 main.py o t r y c a u
```
## Does this ruin the fun of the game?
Probably.  I guess it depends on who you ask

