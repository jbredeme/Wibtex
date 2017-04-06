############################################################
# @file   wibtex_parser.py
# @brief  module to extraction of BibTeX databases
#
# @author Charles Duso
# @date   April 5, 2017
############################################################

################################################
# Import Python Modules
################################################

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import *

################################################
# Function Definitions
################################################
def customizations( record ):
    """Callback function to properly separate fields"""

    record = type(record)
    #record = author(record)
    record = keyword(record)
    record = link(record)
    record = page_double_hyphen(record)
    record = doi(record)
    
    return record

def validate_entries( database ):
    '''
    Validates a BibTeX database for proper entry inputs

    @param  database a BibTeX database in the form of a dictionary
    '''

    # For each entry in the database
    for index in range(0, len(database)):

        current_entry = database[index]

        try:

            entry_id = (current_entry)['ID']

        except KeyError:

            print("Error: BibTeX entry #%d does not have an ID" % i)

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
                    print("Error: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 

            
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
                    print("Error: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 


            elif current_entry['ENTRYTYPE'] == "booklet":

                if "title" not in current_entry:
                        error_string += "title"

                if error_string != "":
                    print("Error: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 


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
                    print("Error: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 


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
                    print("Error: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 

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
                    print("Error: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 


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
                    print("Error: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 


            elif current_entry['ENTRYTYPE'] == "manual":
                
                if "title" not in current_entry:
                    if error_string != "":
                        error_string += ", title"
                    else:
                        error_string += "title"

                if error_string != "":
                    print("Error: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 


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
                    print("Error: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 


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
                    print("Error: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 


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
                    print("Error: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 


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
                    print("Error: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 


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
                    print("Error: Entry {:20s} missing: {:20s}".format(entry_id, error_string)) 


            else:
                print("error")

        except KeyError:
            print("Error: Entry type not listed in BibTeX entry #%d" % i)

    return

def fix_escape_chars( database ):
    #TODO - Properly escape characters for the user
    return database

def latex_to_unicode( database ):
    #TODO - Convert escaped characters to unicode equivalents
    return database

def remove_brackets( database ):
    #TODO - Remove preservation brackets
    return database

def fix_arrays ( database ):
    #TODO - Remove arrays
    return database

def parse( path ):
    """Parses a BibTeX database and returns list of BibTeX entries"""

    # Open database and parse it, extracting properly formatted data
    try:

        with open(path) as bibtex_file:

            parser = BibTexParser()
            parser.customization = customizations
            bib_database = bibtexparser.load(bibtex_file, parser=parser)
            bib_database = bib_database.entries

    except IOError:

        print ("Error: Cannot read BibTeX file or data")
        
    # Validate entries
    validate_entries(bib_database)

    # Properly escape special characters
    bib_database = fix_escape_chars(bib_database)

    # Convert special characters to Unicode
    bib_database = latex_to_unicode(bib_database)

    # Parse out preservation brackets
    bib_database = remove_brackets(bib_database)

    return bib_database
