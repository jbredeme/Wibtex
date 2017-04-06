############################################################
# @file   style.py
# @brief  module to handle formatting of data for reference 
#         styles
#
# @author Charles Duso
# @date   April 5, 2017
############################################################

################################################
# Import Python Modules
################################################

import re
import json
from jinja2 import Template

################################################
# Function Definitions - Style File Interaction
################################################

def validate_style( style_file, style_form ):
    '''
    Validates a specified style from a style file

    @param  file  the file to extract style data from
    @param  style the style to validate
    @return       a boolean indicating success or failure
    '''

    # TODO - Need to flesh out convntions

    return

def read_style_file( style_file, style_form ):
    '''
    Extracts a specified style from a style file

    @param  file  the file to extract style data from
    @param  style the style to extract
    @return       a dictionary containing style data
    '''

    with open(style_file, 'r') as f:
        try:
            data = json.load(f)
        except ValueError:
            data = {}
            print("Error: Could not read style file.")

    return data[style_form]

################################################
# Function Definitions - Style Data Formatting
################################################

def validate_syntax( doc_list ):
    '''
    Validates Word document syntax 

    @param  doc_list a list of BibTeX markup extracted from the document
    @return          a boolean indicating success or failure
    '''

    #TODO - Function may be dropped or reformatted

    valid = False

    # Check for any markup containing a \bibliography{ ... }
    reg_exp = re.compile(r'\\bibliography\{(.*?)\}')
    
    # Ensure that last item is bibliography tag
    if not reg_exp.search(doc_list[(len(doc_list) - 1)]):
        print("Error: '\\bibliography{}' should be final tag in document.")
    else:
        valid = True

    for item in range(0, len(doc_list)):

        if reg_exp.search(doc_list[item]):

            valid = True

    if valid == False:
        print("Error: Missing \\bibliography{} markup in document.")

    return valid

def split_citations( doc_list ):
    '''
    Splits citations into separate lists for each \bibliography{} tag

    @param  doc_list  a list of BibTeX markup extracted from the document
    @return           a list or list of lists containing BibTeX markup
    '''
    # TODO - Change to rename bibliographies based on count

    reg_exp = re.compile(r'\\bibliography\{(.*?)\}')
    bib_count = 0
    num_list  = []

    # Count the number of bibliography tags
    for index in range(0, len(doc_list)):

        # If bibliography tag found, append its index to the list 
        if reg_exp.search(doc_list[index]):
            num_list.append(index)
            bib_count += 1

    # Create a list or list of lists separated by bibliography tag
    if bib_count > 1:

        bib_list  = []
        temp_list = []

        for index in range(0, len(doc_list)):

            # Add list to list of lists
            if index in num_list:
                temp_list.append(doc_list[index])
                bib_list.append(temp_list)
                temp_list = []
            # Add item to list
            else:
                temp_list.append(doc_list[index])

    # Create a single list
    else:
        bib_list = doc_list

    return bib_list

def strip_markup( doc_list ):
    '''
    Splits BibTeX markup from tags contained in the document

    @param  doc_list  a list of BibTeX markup extracted from the document
    @return           a list or list of lists without BibTeX markup
    '''

    # If the doc_list is a list of lists
    if any(isinstance(element, list) for element in doc_list):

        for sub_list in doc_list:
            for index in range(0, len(sub_list)):
                sub_list[index] = re.sub(r'\\cite\{', '', sub_list[index])
                sub_list[index] = re.sub(r'cite\{', '', sub_list[index])
                sub_list[index] = re.sub(r'\\bibliography\{', '', sub_list[index])
                sub_list[index] = re.sub(r'bibliography\{', '', sub_list[index])
                sub_list[index] = re.sub(r'\}', '', sub_list[index])

    # If the doc_list is a single list
    else:

        for index in range(0, len(doc_list)):
            doc_list[index] = re.sub(r'\\cite\{', '', doc_list[index])
            doc_list[index] = re.sub(r'cite\{', '', doc_list[index])
            doc_list[index] = re.sub(r'\\bibliography\{', '', doc_list[index])
            doc_list[index] = re.sub(r'bibliography\{', '', doc_list[index])
            doc_list[index] = re.sub(r'\}', '', doc_list[index])

    return doc_list

def get_dict_from_entry( dict_list, key ):
    '''
    Returns a dictionary from a dictionary of dictionaries based on key

    @param  dict_list a dictionary of dictionaries
    @param  key       the key to find the dictionary from
    @return           a dictionary whose "ID" matches the key
    '''

    out_dict = None

    for dict in dict_list:

        if dict['ID'] == key:
            out_dict = dict
            
    return out_dict

def validate_citations( citations, bib_data ):
    #TODO - Validates that citations are in the dictionary
    return

def remove_duplicates( list ):
    '''
    Removes duplicate values from a list while preserving order

    @param  list a list of items
    @return      a list of items in their original order without duplicates
    '''
    seen = set()
    seen_add = seen.add
    out = [item for item in list if not (item in seen or seen_add(item))]
    return out

def organize_citations( citations, order ):
    '''
    Removes duplicate values and bibliography tag(s) from a list/list of lists
    of citations

    @param  citations a list or list of lists of extracted data
    @return           a list or list of lists of citation data
    '''

    # TODO - Handle alphabetic ordering (default and backup methods)

    # If citations is a list of lists
    if any(isinstance(element, list) for element in citations):

        for index in range(0, len(citations)):

            temp_list = (citations[index])[0:(len(citations[index]) - 1)]
            temp_list = remove_duplicates(temp_list)

    # If citations is a single list
    else:
        # Remove duplicate data
        temp_list = citations[0:(len(citations) - 1)]
        temp_list = remove_duplicates(temp_list)
        
    return temp_list

def generate_citations( citations, bib_data, style_form ):
    '''
    Generates in-text citation strings from the style file template

    @param  citations   a list or list of lists of unique citations
    @param  bib_data    a list of BibTeX bibliography entries
    @param  style_form  a template representing the in-text citation 
    @param  output_dict the dictionary to store output data in
    @return             a dictionary containing formatted in-text citations
    '''

    output_dict = {}

    template = Template(style_form['in_text_style'])

    # If citations is a list of lists
    if any(isinstance(element, list) for element in citations):

        #TODO - Generate unique citations for sources shared across bibliographies

        return

    # If citations is a single list
    else:

        index = 1
        # Generate in-text citation and add it to the output dictionary
        for tag in citations:

            dict = get_dict_from_entry(bib_data, tag)
            dict['num'] = index
            output_dict[tag] = template.render(dict)
            index += 1

    return output_dict

def generate_works_cited( citations, bib_data, style_form, output_dict ):
    '''
    Generates a works cited page from the style_form file template

    @param  citations   a list or list of lists of unique citations
    @param  bib_list    a list of BibTeX bibliography entries
    @param  style_form  a template representing the citation output 
    @param  output_dict the dictionary to store output data in
    @return             a dictionary containing formatted citation data
    '''
    
    bib_string = "" #' String containing works cited

    # If citations is a list of lists
    if any(isinstance(element, list) for element in citations):

        #TODO - Generate works cited for sources shared across bibliographies

        return

    # If citations is a single list
    else:

        # Extract the list of citations
        temp_list = citations[0:(len(citations) - 1)]

        for item in temp_list:

            dict = get_dict_from_entry(bib_data, item)

            # Generate a template based on the entry type
            template = Template(style_form[dict['ENTRYTYPE']])

            # Append the output to the refernce string
            bib_string += template.render(dict)

    # Set the bibliography key equal to the reference string
    output_dict[citations[len(citations) - 1]] = bib_string

    return output_dict

def get_reference_data( style_file, style_form, doc_list, bib_data ):

    bib_list   = {}
    cite_list  = {}
    style_data = {}
    output     = {}

    # Validate style chosen from style file
    validate_style(style_file, style_form)

    # Read style file and extract style choice
    style_data = read_style_file(style_file, style_form)

    # Validate BibTeX syntax
    validate_syntax(doc_list)

    # Partition reference sections
    bib_list = split_citations(doc_list)

    # Strip BibTeX markup
    bib_list = strip_markup(bib_list)

    # Validate that citations are in BibTeX database
    validate_citations(bib_list, bib_data)

    # Organize citations according to style
    cite_list = organize_citations(bib_list, style_data['order'])

    # Generate in-text citations
    output = generate_citations(cite_list, bib_data, style_data)

    # Generate reference page
    output = generate_works_cited(bib_list, bib_data, style_data, output)

    return output