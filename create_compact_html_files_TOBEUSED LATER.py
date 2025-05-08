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
Sequential Number of Headword (per letter) as a 3 digit number with leading zeroes
.html

In the case where the page begins with a part of an entry held over from the previous page
the first and third part of the name will be the same, only the page number will be different

See code below for format of the html
'''

import config
import pprint
from bs4 import BeautifulSoup
from collections import OrderedDict, Counter

PREFACE_PAGES_COUNT = 25 # the html treats page 1 as page 26, due to the preface pages xxv (25)

dictionary_letters = ('A', 'E', 'H', 'I', 'K', 'M', 'N', 'Ng', 'O', 'P', 'R', 'T', 'U', 'W', 'Wh')
start_pages = {
    'A' : 1,
    'E' : 25,
    'H' : 29,
    'I' : 73,
    'K' : 81,
    'M' : 161,
    'N' : 216,
    'Ng' : 225,
    'O' : 237,
    'P' : 243,
    'R' : 319,
    'T' : 354,
    'U' : 464,
    'W' : 472,
    'Wh' : 484,
}


def create_compact_html_files(letter):

    cf = config.ConfigFile()
    text_files_path = (cf.configfile[cf.computername]['original_files_path'])
    sections_and_pbs = []

    # open the specific html file
    file_name = letter + ".html"
    text_file_path = text_files_path + file_name
    with open(text_file_path, 'r') as f:
        soup = BeautifulSoup(f)
        soup_sections_and_pbs = soup.select(".section,[title='page break']") #pb = page break
        for soup_section_or_pb in soup_sections_and_pbs:
            # remove the p tag with the id 'hang' as we don't need it
            if soup_section_or_pb.select_one(".hang"):
                soup_section_or_pb.select_one(".hang").unwrap()   
            sections_and_pbs.append(soup_section_or_pb)

    # create a list of keys for each section
    # Headword-PageNumber-Sequential Number for the letter E
    # For example "Engari-027-031"
    page_numbers = get_page_numbers(letter, sections_and_pbs)
    od = OrderedDict(sorted(Counter(page_numbers).items()))
    pprint.pprint(od)
    pass
    return True


def get_page_numbers(letter, sections_and_pbs):
    '''
    given the list passed returns the page number of each section
    Where a section spans 2 pages it will be split in two and a different page number
    assigned to each part
    '''   

    page_numbers = []

    for counter, section_or_pb in enumerate(sections_and_pbs):
        # print(counter, section_or_pb.name)
        # only going to create page numbers for sections
        # find the first page break entry (if it exists), looking backwards from where we are
        if section_or_pb.name == "div":
            reversed_list_before = reversed(sections_and_pbs[:counter])
            try:
                page_break_entry = next(x for x in reversed_list_before if x.name == "a")
                # print(page_break_entry)
            except StopIteration:
                # we are on the first page for the letter and it is not a brand new page
                page_number_to_use = start_pages[letter]
            else:
                page_number = int(page_break_entry["href"].replace('#n', ''))
                page_number_to_use = page_number - PREFACE_PAGES_COUNT

            page_numbers.append(page_number_to_use)
            print (page_number_to_use, section_or_pb["id"].replace(".", chr(772)))


    return page_numbers
    
           
    
              



if __name__ == '__main__':

    import sys
    import argparse
    import ast

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the create_compact_html_files function
    create_compact_html_files_parser = subparsers.add_parser('create_compact_html_files')
    create_compact_html_files_parser.add_argument('letter', choices = list(dictionary_letters))
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
