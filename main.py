"""
Main program to brute force (dictionary attack, more accurately) the New York Times Spelling Bee Puzzle
"""

import string
import re
import sys
from columnize import columnize
from dictionary import get_dictionary_words

def main(letters_list:list):
    """
    Main Program
    Args:
        letters_list (list): A list of letters for the puzzle.  The first is treated as the 'Center'
        (Required for puzzle) letter.
    """

    center_letter = letters_list[0]
    other_letters = letters_list[1:]
    print(f"[Arguments]:")
    print(f"'{center_letter}' is the center (required) letter.  The other letters are: {other_letters}")

    center_letter_pattern = re.compile(f"^.*{center_letter}.*$")
    all_letters_pattern = re.compile(f"^({'|'.join(letters_list)})+$") # We could handle required length of 4+ chars here, but we'll do it in the loop


    dictionary_words = get_dictionary_words(include_hyphenated=True, verbose=False)
    matched_words = [] # Running list of words that satisfy the rules.  Of course, this doesn't mean that the puzzle of the day will actually accept them
    pangrams = []

    # Placeholder dict by first letter
    matched_words_by_letter = {}
    for l in letters_list:
        matched_words_by_letter[l] = []
    
    # Find matched
    for _w in dictionary_words:
        # Replace hyphens with empty string in case the puzzle would accept this as a compound word (I think that's the proper term)
        w = re.sub(pattern=r"\-+", repl="", string=_w)
        # if _w != w:
        #     print(f"Changed '{_w}' to '{w}'")
        
        # Word must be 4+ chars
        if not len(w) >= 4:
            continue

        # Word must have the center letter in it somewhere
        center_letter_match = re.search(pattern=center_letter_pattern, string=w)
        if not center_letter_match:
            continue
        
        # Word must contain only letters from the letters list
        letters_match = re.fullmatch(pattern=all_letters_pattern, string=w)
        if not letters_match:
            continue

        # If we haven't continued the loop yet, we've got a matching word
        matched_words.append(w)
        matched_words_by_letter[w[0]].append(w)

        # Have we found a pangram (each letter in the word at least once)?
        found_pangram = True #Until proven otherwise
        if len(w) < 7:
            found_pangram = False # Not possible for words less than 7 chars

        if found_pangram: # If still true, check for each char
            for l in letters_list:
                if l not in w:
                    found_pangram = False
                    break
        
        if found_pangram: # If still true, we've found a pangram
            pangrams.append(w)

    print(f"\n[Matching words]:\n")

    for k in sorted(matched_words_by_letter.keys()):
        print(f"Found {len(matched_words_by_letter[k])} word(s) that begin with '{k}':")
        print(columnize(sorted(matched_words_by_letter[k]), displaywidth=80))

    if pangrams:
        print(f"Found {len(pangrams)} pangram(s).  These contain each letter in the puzzle:")
        print(columnize(sorted(pangrams), displaywidth=80))

if __name__ == '__main__':

    # Input validations
    args = sys.argv

    alphabet = [char for char in string.ascii_lowercase] # Break into list of single chars
    
    error_message = f"This program requires 7 single-letter, unique arguments to be passed in.  " \
        f"The first letter should be the 'center' (required in each word) letter of the puzzle." \
        f"The order doesn't matter for the other 6 letters.\n" \
        f"Valid letters are: {(' '.join(alphabet))}\n" \
        f"Got {len(args) - 1}: {args[1:]}"

    # Need exactly 8 args: This programs name (0) 7 letters
    if not len(args) == 8:
        raise ValueError(error_message)

    # All letters passed in must be mutually exclusive
    _duplicates = []
    letters_list = []

    idx = 1
    while idx < len(args):
        _letter = args[idx].strip().lower()

        # Detect duplicates
        if _letter in letters_list:
            if _letter not in _duplicates:
                _duplicates.append(_letter)
        

        if _letter not in alphabet:
            raise ValueError(f"An invalid letter or string ('{_letter}') was passed into the program."\
                             f"Valid letters are: {alphabet}")

        letters_list.append(_letter)

        idx += 1

    # Raise error for duplicates
    if len(_duplicates) > 0:
        _m = f"Duplicate letters are not allowed!\n{error_message}"
        raise ValueError(_m)


    main(letters_list=letters_list)


