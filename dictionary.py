"""
Not to be confused with python dict types, this module has to do with the English dictionary
"""

import requests
import os
import re
import string

def _get_dictionary_file_name():
    """
    Constructs the path to the dictionary file name
    """

    this_dir = os.path.dirname(os.path.realpath(__file__))
    output_file_name = os.path.join(this_dir, 'websters_dictionary.txt')

    return output_file_name

def download_websters_dictionary(verbose: bool=True):
    """
    Downloads the Webster's dictionary from an online source.
    Args:
        verbose (bool): If True, prints messages, otherwise not.
    """
    # Webster's Unabridged Dictionary
    url="https://www.gutenberg.org/cache/epub/29765/pg29765.txt" 
   
    if verbose:
        print(f"Retrieving Webster's Dictionary from [{url}]...")

    response = requests.get(url=url)

    if not response.ok:
        response.raise_for_status()
    
    dictionary_string = response.text

    return dictionary_string

def save_websters_dictionary(verbose: bool=True):
    """
    Saves the dictionary to a flat file:
    
    Args:
        verbose (bool): If True, prints messages, otherwise not.
    """

    output_file_name = _get_dictionary_file_name()

    data = download_websters_dictionary(verbose=verbose)
    with open(output_file_name, 'w') as f:
        f.write(data)

    if verbose:
        print(f"Websters dictionary saved to file [{output_file_name}]")

def init_websters_dictionary(verbose: bool=True):
    """
    Makes a dictionary file if it doesn't exist yet
    """

    output_file_name = _get_dictionary_file_name()
    if not os.path.isfile(output_file_name):
        if verbose:
            print(f"Dictionary file does not yet exist at [{output_file_name}].  "\
                f"A new one will be created")
        save_websters_dictionary(verbose=verbose)
    else:
        if verbose:
            print(f"Dictionary file already exists at [{output_file_name}].  "\
                f"No need to get a new one.\nTo force a refresh, call "\
                f"[save_websters_dictionary()].  Or just delete [{output_file_name}]")

def get_dictionary_words(include_hyphenated: bool = False, verbose: bool = True):
    """
    Parses a list of 'all' words out of the dictionary file
    This project in general is used to solve the Daily Wall Street Journal Spelling Bee puzzle
    and thus excludes hyphenated words by default, as these don't apply to the puzzle,
    the dictionary file is formatted in such a way that a word is always on a single line on its own
    with its definition beneath it.  Thus, we can look for just a complete match
    of our strict regex on every line of the file

    Args:
        include_hyphenated (bool): If True, includes hyphenated words
        verbose: If True, prints messages.  Otherwise not
    """

    # Ensure we have a dictionary file to work with
    init_websters_dictionary(verbose=False)

    # Handle regex
    if not include_hyphenated:
        if verbose:
            print("Hyphenated words will be excluded from the output")
        _re_pattern = r"^[a-z]+"
    else:
        if verbose:
            print("Hyphenated words will be included in the output")
        _re_pattern = r"^[a-z\-]+"
    re_pattern = re.compile(_re_pattern, re.IGNORECASE)


    # Traverse dictionary file
    lines_matched = 0
    lines_unmatched = 0
    blank_lines = 0
    words = []
    with open(_get_dictionary_file_name(), 'r') as f:
        for _line in f:
            line = _line.strip().lower()

            if not line:
                blank_lines += 1
                continue # Skip blank lines
        
            # Check for a complete regex match
            match = re.fullmatch(pattern=re_pattern, string=line)

            # Record matching words, update counters
            if match:
                words.append(line)

                lines_matched += 1
            else:
                lines_unmatched += 1
    total_lines = blank_lines + lines_matched + lines_unmatched

    ret_val = list(set(words))
    
    if verbose: 
        print(f"Dictionary file is {total_lines} lines, including blanks:\n" \
                f"Non Blank Lines: {lines_unmatched + lines_matched}\n" \
                f"Unmatched Lines: {lines_unmatched}\n" \
                f"Matched Lines: {lines_matched}\n" \
                f"Unique Words: {len(ret_val)}")

    return ret_val

if __name__ == '__main__':
    get_dictionary_words()
