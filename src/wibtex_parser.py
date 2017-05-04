############################################################
# @file   wibtex_parser.py
# @brief  module to extraction of BibTeX databases
#
# @author Charles Duso
# @date   May 3, 2017
############################################################

################################################
# Import Python Modules
################################################

import re
import logger
import bibtexparser
import map
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import *
from bibtexparser.latexenc import *

################################################
# Function Definitions
################################################

def customizations( record ):
    '''
    Callback function to properly separate fields

    @param record the value we wish to modify
    '''

    # First, we convert everything to unicode
    record = author(record)

    return record

def validate_entries( database, log, flag = True):
    '''
    Validates a BibTeX database for proper entry inputs

    @param  database a BibTeX database in the form of a dictionary
    '''

    if flag:
        # For each entry in the database
        for index in range(0, len(database)):

            current_entry = database[index]

            try:

                entry_id = (current_entry)['ID']

            except KeyError:

                log.log_data("\nError: BibTeX entry #%d does not have an ID" % i)

            # Verify entries have their respective, required fields
            try:

                error_string = ""

                if current_entry['ENTRYTYPE'] == "article":

                    if "author" not in current_entry:
                        error_string += "author"

                    if "title" not in current_entry:
                        if error_string != "":
                            error_string += ", title"
                        else:
                            error_string += "title"

                    if "journal" not in current_entry:
                        if error_string != "":
                            error_string += ", journal"
                        else:
                            error_string += "journal"

                    if "year" not in current_entry:
                        if error_string != "":
                            error_string += ", year"
                        else:
                            error_string += "year"

                    if error_string != "":
                        log.log_data("\nError: Entry {:20s} missing: {:20s}".format(entry_id, error_string))

                
                elif current_entry['ENTRYTYPE'] == "book":
                    
                    if "author" not in current_entry:
                        error_string += "author"

                    if "title" not in current_entry:
                        if error_string != "":
                            error_string += ", title"
                        else:
                            error_string += "title"

                    if "publisher" not in current_entry:
                        if error_string != "":
                            error_string += ", publisher"
                        else:
                            error_string += "publisher"

                    if "year" not in current_entry:
                        if error_string != "":
                            error_string += ", year"
                        else:
                            error_string += "year"

                    if error_string != "":
                        log.log_data("\nError: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 


                elif current_entry['ENTRYTYPE'] == "booklet":

                    if "title" not in current_entry:
                            error_string += "title"

                    if error_string != "":
                        log.log_data("\nError: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 


                elif current_entry['ENTRYTYPE'] == "conference":

                    if "author" not in current_entry:
                        error_string += "author"

                    if "title" not in current_entry:
                        if error_string != "":
                            error_string += ", title"
                        else:
                            error_string += "title"

                    if "booktitle" not in current_entry:
                        if error_string != "":
                            error_string += ", booktitle"
                        else:
                            error_string += "booktitle"

                    if "year" not in current_entry:
                        if error_string != "":
                            error_string += ", year"
                        else:
                            error_string += "year"

                    if error_string != "":
                        log.log_data("\nError: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 


                elif current_entry['ENTRYTYPE'] == "inbook":

                    if "author" not in current_entry:
                        error_string += "author"

                    if "editor" not in current_entry:
                        if error_string != "":
                            error_string += ", editor"
                        else:
                            error_string += "editor"

                    if "title" not in current_entry:
                        if error_string != "":
                            error_string += ", title"
                        else:
                            error_string += "title"

                    if "chapter" not in current_entry:
                        if error_string != "":
                            error_string += ", chapter"
                        else:
                            error_string += "chapter"

                    if "pages" not in current_entry:
                        if error_string != "":
                            error_string += ", pages"
                        else:
                            error_string += "pages"
                    
                    if "publisher" not in current_entry:
                        if error_string != "":
                            error_string += ", publisher"
                        else:
                            error_string += "publisher"


                    if "year" not in current_entry:
                        if error_string != "":
                            error_string += ", year"
                        else:
                            error_string += "year"

                    if error_string != "":
                        log.log_data("\nError: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 

                elif current_entry['ENTRYTYPE'] == "incollection":
                    
                    if "author" not in current_entry:
                        error_string += "author"

                    if "title" not in current_entry:
                        if error_string != "":
                            error_string += ", title"
                        else:
                            error_string += "title"

                    if "booktitle" not in current_entry:
                        if error_string != "":
                            error_string += ", booktitle"
                        else:
                            error_string += "booktitle"
            
                    if "publisher" not in current_entry:
                        if error_string != "":
                            error_string += ", publisher"
                        else:
                            error_string += "publisher"

                    if "year" not in current_entry:
                        if error_string != "":
                            error_string += ", year"
                        else:
                            error_string += "year"

                    if error_string != "":
                        log.log_data("\nError: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 


                elif current_entry['ENTRYTYPE'] == "inproceedings":
                    
                    if "author" not in current_entry:
                        error_string += "author"

                    if "title" not in current_entry:
                        if error_string != "":
                            error_string += ", title"
                        else:
                            error_string += "title"

                    if "booktitle" not in current_entry:
                        if error_string != "":
                            error_string += ", booktitle"
                        else:
                            error_string += "booktitle"

                    if "year" not in current_entry:
                        if error_string != "":
                            error_string += ", year"
                        else:
                            error_string += "year"

                    if error_string != "":
                        log.log_data("\nError: Entry {:20s} missing: {:20s}".format(entry_id, error_string))

                elif current_entry['ENTRYTYPE'] == "manual":
                    
                    if "title" not in current_entry:
                        if error_string != "":
                            error_string += ", title"
                        else:
                            error_string += "title"

                    if error_string != "":
                        log.log_data("\nError: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 


                elif current_entry['ENTRYTYPE'] == "mastersthesis":
                    
                    if "author" not in current_entry:
                        error_string += "author"

                    if "title" not in current_entry:
                        if error_string != "":
                            error_string += ", title"
                        else:
                            error_string += "title"

                    if "school" not in current_entry:
                        if error_string != "":
                            error_string += ", school"
                        else:
                            error_string += "school"

                    if "year" not in current_entry:
                        if error_string != "":
                            error_string += ", year"
                        else:
                            error_string += "year"

                    if error_string != "":
                        log.log_data("\nError: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 


                elif current_entry['ENTRYTYPE'] == "misc":
                    continue

                elif current_entry['ENTRYTYPE'] == "phdthesis":
                    
                    if "author" not in current_entry:
                        error_string += "author"

                    if "title" not in current_entry:
                        if error_string != "":
                            error_string += ", title"
                        else:
                            error_string += "title"

                    if "school" not in current_entry:
                        if error_string != "":
                            error_string += ", school"
                        else:
                            error_string += "school"

                    if "year" not in current_entry:
                        if error_string != "":
                            error_string += ", year"
                        else:
                            error_string += "year"

                    if error_string != "":
                        log.log_data("\nError: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 


                elif current_entry['ENTRYTYPE'] == "proceedings":

                    if "title" not in current_entry:
                        if error_string != "":
                            error_string += ", title"
                        else:
                            error_string += "title"

                    if "year" not in current_entry:
                        if error_string != "":
                            error_string += ", year"
                        else:
                            error_string += "year"

                    if error_string != "":
                        log.log_data("\nError: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 


                elif current_entry['ENTRYTYPE'] == "techreport":
                    
                    if "author" not in current_entry:
                        error_string += "author"

                    if "title" not in current_entry:
                        if error_string != "":
                            error_string += ", title"
                        else:
                            error_string += "title"

                    if "institution" not in current_entry:
                        if error_string != "":
                            error_string += ", institution"
                        else:
                            error_string += "institution"

                    if "year" not in current_entry:
                        if error_string != "":
                            error_string += ", year"
                        else:
                            error_string += "year"

                    if error_string != "":
                        log.log_data("\nError: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 


                elif current_entry['ENTRYTYPE'] == "unpublished":
                    
                    if "author" not in current_entry:
                        error_string += "author"

                    if "title" not in current_entry:
                        if error_string != "":
                            error_string += ", title"
                        else:
                            error_string += "title"

                    if "note" not in current_entry:
                        if error_string != "":
                            error_string += ", note"
                        else:
                            error_string += "note"

                    if error_string != "":
                        log.log_data("\nError: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 


                else:
                    return

            except KeyError:
                log.log_data("\nError: Entry type not listed in BibTeX entry #%d" % i)

    return

def fix_escape_chars( database ):
    '''
    Strips backslashes from a BibTeX database

    @param  database a BibTeX database in the form of a dictionary
    '''

    temp_dict = {}
    temp_list = []

    # For each dictionary
    for index in range(0, len(database)):

        temp_dict = database[index]
        
        # For each key
        for key in temp_dict:

            # If entry is a list
            # TODO - Check for nested lists?
            if isinstance(temp_dict[key], list):

                for item in temp_dict[key]:

                    temp_list.append(item.replace("\\", ""))

                temp_dict[key] = temp_list
                temp_list = []

            else:
                temp_dict[key] = temp_dict[key].replace("\\", "")

        database[index] = temp_dict

    return database

# TODO - Optional as callback function appears robust enough to handle
def latex_to_unicode( database ):
    '''
    Converts a TeX character codes to Unicode

    @param  database a BibTeX database in the form of a dictionary
    '''

    key_item_list = []
    matches = []
    converted_matches = []
    item_string = ""

    convert = map.RosettaStone()

    regex = r'\\\\.*\{.*\}|\\\\\w+[^\}\{]'

    # For each entry
    for index in range(0, len(database)):

        sub_dict = database[index]

        # For each key
        for key in sub_dict:

            if isinstance(sub_dict[key], list):

                for item_i in range(0, len(sub_dict[key])):

                    item_string = sub_dict[key][item_i]

                    if item_string:

                        # Find matches
                        matches = re.findall(regex, item_string)

                        # Convert matches
                        if matches:
                            converted_matches = []

                            for match in matches:
                                converted_matches.append(convert.get_encoding(match))

                            if len(matches) == len(converted_matches):

                                for item in range(0, len(matches)):
                                    item_string = re.sub(regex, converted_matches[item], item_string, count=1)
                                
                    key_item_list.append(item_string)

                sub_dict[key] = key_item_list
                key_item_list = []

            else:

                # Extract the value associated with the key
                item_string = sub_dict[key]

                if item_string:

                    # Find matches
                    matches = re.findall(regex, item_string)

                    # Convert matches
                    if matches:

                        converted_matches = []

                        for match in matches:
                            converted_matches.append(convert.get_encoding(match))

                        if len(matches) == len(converted_matches):

                            for item in range(0, len(matches)):
                                item_string = re.sub(regex, converted_matches[item], item_string, count=1)
                        
                sub_dict[key] = item_string
        
        database[index] = sub_dict
    
    return database

def remove_brackets( database ):
    '''
    Strips preservation braces from a BibTeX database

    @param  database a BibTeX database in the form of a dictionary
    '''

    temp_dict = {}
    temp_list = []

    # For item in database
    for index in range(0, len(database)):
        temp_dict = database[index]

        # For each key strip brackets
        for key in temp_dict:

            # If entry is a list
            # TODO - Check for nested lists?
            if isinstance(temp_dict[key], list):

                for item in temp_dict[key]:

                    temp_list.append(re.sub(r'[\{\}]', '', item))

                temp_dict[key] = temp_list
                temp_list = []

            else:
                temp_dict[key] = re.sub(r'[\{\}]', '', temp_dict[key])

        database[index] = temp_dict

    return database

def convert_to_dictionary( bib_database, log ):
    '''
    Converts a BibTeX database to a dictionary

    @param bib_database the database to convert to
    '''

    final_dict = {} #' Dictionary with which we store items by BibTeX entry key
    entry_key = ''  #' The entry key to a BibTeX entry

    # For each item in the database
    for item in bib_database:

        # Get the ID and use it as the key for the entry
        entry_key = item.get('ID')

        # Sort authors if possible
        if item.get('author'):
            item['author'] = sorted(item['author'], key=str.swapcase)

        # If key not in new dictionary, store it
        if entry_key is not None and entry_key not in final_dict:
            final_dict[entry_key] = item

        else:
            log.log_data("\nEntry key already exists in database")
    
    return final_dict

def parse( path, log ):
    '''
    Parses a BibTeX database and returns list of BibTeX entries

    @param  path a BibTeX database file path
    '''

    # Open database and parse it, extracting properly formatted data
    try:

        with open(path) as bibtex_file:

            parser = BibTexParser()
            parser.customization = customizations
            bib_database = bibtexparser.load(bibtex_file, parser=parser)
            bib_database = bib_database.entries

    except IOError:

        log.log_data("\nError: Cannot read BibTeX file or data")

    # Validate entries
    validate_entries(bib_database, log)

    # Convert characters to unicode
    bib_database = latex_to_unicode(bib_database)

    # Parse out preservation brackets
    bib_database = remove_brackets(bib_database)

    # Parse out backslashes
    bib_database = fix_escape_chars(bib_database)

    # Convert to dictionary of dictionaries with access via entry key
    bib_database = convert_to_dictionary(bib_database, log)

    return bib_database
