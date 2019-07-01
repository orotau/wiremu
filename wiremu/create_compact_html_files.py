'''
This module is used to create compact html files. 
An example is as follows...

<div class="section" id="Ekieki" xml:lang="en">
  <p class="hang">
    <span class="foreign bold" xml:lang="mi">Ekieki</span> =
    <b>ikeike</b>, a.
    <i>High, lofty</i>.
  </p>
</div>

The key elements being 
Everything in the div tag with class = section

and

the leftmost word in the 3rd line span class - Ekieki in this case
This will be used in name of the file

We will write an html file that has the name
HeadWord - 
Page number in Wiremu 6 as 3 digit number with leading zeroes - 
Sequential Number on page of Headword as a 2 digit number with leading zeroes
.html

In the case where the page begins with a part of an entry held over from the previous page
the third part of the name of that entry will be 00

See code below for format of the html
'''

import config
import pprint
from bs4 import BeautifulSoup

ALL_TEXT = "All"

dictionary_letters = ('A', 'E', 'H', 'I', 'K', 'M', 'N', 'Ng', 'O', 'P', 'R', 'T', 'U', 'W', 'Wh')
letter_choices = list(dictionary_letters)
letter_choices.append(ALL_TEXT)

def create_compact_html_files(letter):

    cf = config.ConfigFile()
    text_files_path = (cf.configfile[cf.computername]['original_files_path'])

    for dictionary_letter in dictionary_letters:
        if letter == dictionary_letter or letter == ALL_TEXT:
            # open the specific html file
            file_name = dictionary_letter + ".html"
            text_file_path = text_files_path + file_name
            with open(text_file_path, 'r') as f:
                soup = BeautifulSoup(f, "lxml") # belt and braces, explicit parser defined
                headword_soups = soup.find_all(class_="section")
                for headword_soup in headword_soups:
                    print(headword_soup.prettify())
    return True



if __name__ == '__main__':

    import sys
    import argparse
    import ast

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the create_compact_html_files function
    create_compact_html_files_parser = subparsers.add_parser('create_compact_html_files')
    create_compact_html_files_parser.add_argument('letter', choices = letter_choices)
    create_compact_html_files_parser.set_defaults(function = create_compact_html_files)

    # parse the arguments
    arguments = parser.parse_args()
    arguments = vars(arguments) #convert from Namespace to dict

    #attempt to extract and then remove the function entry
    try:
        function_to_call = arguments['function']
    except KeyError:
        print ("You need a function name. Please type -h to get help")
        sys.exit()
    else:
        #remove the function entry as we are only passing arguments
        del arguments['function']

    if arguments:
        #remove any entries that have a value of 'None'
        #We are *assuming* that these are optional
        #We are doing this because we want the function definition to define
        #the defaults (NOT the function call)
        arguments = { k : v for k,v in arguments.items() if v is not None }

        #alter any string 'True' or 'False' to bools
        arguments = { k : ast.literal_eval(v) if v in ['True','False'] else v
                                              for k,v in arguments.items() }

    result = function_to_call(**arguments) #note **arguments works fine for empty dict {}

    print (result)
