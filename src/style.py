############################################################
# @file   style.py
# @brief  module to handle formatting of data for reference 
#         styles
#
# @author Charles Duso
# @date   May 3, 2017
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

def get_valid_styles():
    '''
    Validates the styles from the config folder and returns
    a list of valid styles

    @return a list of valid styles
    '''

    #TODO - Log invalid styles

    style_file = "../config/styles.json"
    valid_styles = []

    with open(style_file, 'r') as f:
        try:
            data = json.load(f)
        except ValueError:
            print("Error: Could not read style file.")
            return ""

    for key in data:

        style_data = data.get(key)

        if style_data is None:
            print('ERROR - Could not retrieve style template')
            continue
        else:
            order = {}
            in_text = {}
            title = ""
            default = ""

            order = style_data.get('order')
            if order is None:
                print('ERROR - Could not access "order" field in style template')
                continue
            else:
                if 'method' not in order or 'sortby' not in order:
                    print('ERROR - Missing "method" or "sortby" values in "order" field of style template.')
                    continue

            in_text = style_data.get('in_text_style')
            if in_text is None:
                print('ERROR - Could not access "in_text_style" field in style template')
                continue
            else:
                if 'index' not in in_text or 'template' not in in_text:
                    print('ERROR - Could not access "index" or "template" in "in_text_style" field of style template')
                    continue

            title = style_data.get('title')
            if title is None:
                print('ERROR - Could not access "title" field in style template')
                continue

            default = style_data.get('default_style')
            if default is None:
                print('ERROR - Could not access "default_style" field in style template')
                continue
            
        valid_styles.append(key)

    return valid_styles

def read_style_file( style_form ):
    '''
    Extracts a specified style from a style file

    @param  file  the file to extract style data from
    @param  style the style to extract
    @return       a dictionary containing style data
    '''

    style_file = "../config/styles.json"

    with open(style_file, 'r') as f:
        try:
            data = json.load(f)
        except ValueError:
            data = {}
            print("Error: Could not read style file.")

    return data.get(style_form)

################################################
# Function Definitions - Style Data Formatting
################################################

def validate_citations( bib_tags, bib_data ):

    sub_dict = {}  #' Dictionary for reference sections
    cite_dict = {} #' Dictionary of citations found for a reference section
    key = ''       #' Temporary key to see if entry in BibTeX database
    log = "" 

    #TODO - User logger or flag?

    # For each bibliography
    for super_key in bib_tags:

        sub_dict = bib_tags.get(super_key)
        cite_dict = sub_dict.get('citations')
        
        # For each citation
        for sub_key in cite_dict:

            key = cite_dict.get(sub_key).get('bib_key')

            if key in bib_data:
                # TODO - Do anything?
                continue
            else:
                # TODO - Verify and log?
                continue

    return

def sort_alphabetical( bib_key, sort_list, ordered_cites ):

    sorted_list = []
    sorted_tags = []
    to_sort = []
    jinja_list = []
    outer_list = []

    temp_str = ""

    # For each entry in bibliography
    for item in sort_list:

        # Sort a list of authors or titles
        item[2] = sorted(item[2], key=str.swapcase)

        to_sort.append(item[2][0])

    # Sort the list of authors/titles/other
    sorted_list = sorted(to_sort, key=str.swapcase)

    # Create a list equal to the size of the sorted list
    sorted_tags = sorted_list

    for index in sorted_list:
        jinja_list.append(0)

    # Extract the citation tags
    for index in range(0, len(sorted_list)):

        for item in range(0, len(sorted_list)):

            if sorted_list[item] in sort_list[index][2]:

                jinja_list[item] = sort_list[index][0]
                sorted_tags[item] = sort_list[index][1]
                sort_list[index][2] = ['#']
    
    outer_list.append(sorted_tags)
    outer_list.append(jinja_list)

    ordered_cites[bib_key] = outer_list

    return ordered_cites

def organize_citations( bib_tags, bib_data, order ):

    method = order.get('method')
    sort_by = order.get('sortby')

    jinja_var = ''
    sort_item = ''

    tag_list = []
    jinja_list = []
    outer_list = []
    triplet = []

    ordered_cites = {}

    if method == 'alpha':

        # Sort via authors
        if sort_by == 'author':

            # For each bibliography section
            for bib in bib_tags:

                # Grab the list of citations
                citations = bib_tags.get(bib).get('citations')
                
                # Grab the entry key and sorting token
                for entry_key in citations:
                    
                    bib_key = citations.get(entry_key).get('bib_key')
                    jinja_var = citations.get(entry_key).get('jinja_var')

                    if 'author' in bib_data.get(bib_key):

                        sort_item = bib_data.get(bib_key).get('author')

                    elif 'title' in bib_data.get(bib_key):

                        sort_item = bib_data.get(bib_key).get('title') 

                    else:
                        # Grab next available value
                        sort_item = next (iter (bib_data.get(bib_key).values()))

                    triplet.append(jinja_var)
                    triplet.append(bib_key)
                    triplet.append(sort_item)

                    tag_list.append(triplet)

                    triplet = []

                ordered_cites = sort_alphabetical(bib_tags.get(bib).get('jinja_var'), tag_list, ordered_cites)
                tag_list = []

        # Sort via titles
        elif sort_by == 'title':

            # For each bibliography section
            for bib in bib_tags:

                # Grab the list of citations
                citations = bib_tags.get(bib).get('citations')
                
                # Grab the entry key and sorting token
                for entry_key in citations:
                    
                    bib_key = citations.get(entry_key).get('bib_key')
                    jinja_var = citations.get(entry_key).get('jinja_var')

                    if 'title' in bib_data.get(bib_key):

                        sort_item = bib_data.get(bib_key).get('title')

                    elif 'author' in bib_data.get(bib_key):

                        sort_item = bib_data.get(bib_key).get('author') 

                    else:
                        # Grab next available value
                        sort_item = next (iter (bib_data.get(bib_key).values()))

                    triplet.append(jinja_var)
                    triplet.append(bib_key)
                    triplet.append(sort_item)

                    tag_list.append(triplet)

                    triplet = []

                ordered_cites = sort_alphabetical(bib_tags.get(bib).get('jinja_var'), tag_list, ordered_cites)
                tag_list = []

        # Default to first-available field
        else:
            # For each bibliography section
            for bib in bib_tags:

                # Grab the list of citations
                citations = bib_tags.get(bib).get('citations')
                
                # Grab the entry key and sorting token
                for entry_key in citations:
                    
                    bib_key = citations.get(entry_key).get('bib_key')
                    jinja_var = citations.get(entry_key).get('jinja_var')

                    sort_item = next (iter (bib_data.get(bib_key).values()))

                    triplet.append(jinja_var)
                    triplet.append(bib_key)
                    triplet.append(sort_item)

                    tag_list.append(triplet)

                    triplet = []
        
                ordered_cites = sort_alphabetical(bib_tags.get(bib).get('jinja_var'), tag_list, ordered_cites)
                tag_list = []

    # Default to first-written-first-cited
    else:

        c_count = 0

        acccess_str = ""
        
        for key in bib_tags:

            citations = bib_tags.get(key).get('citations')

            for tag in range(0, len(citations.keys())):

                access_str = "cite" + str(c_count)

                tag_list.append(citations[access_str]['bib_key'])
                jinja_list.append(citations[access_str]['jinja_var'])

                c_count += 1

            c_count = 0

            outer_list.append(tag_list)
            outer_list.append(jinja_list)
            
            ordered_cites[key] = outer_list
            tag_list = []
            jinja_list = []
            outer_list = []
    
    return ordered_cites

def generate_citations( bib_data, ordered_cites, style_data ):

    output = {}
    cur_bib = {}

    index = 1

    token = style_data.get('index')
    template = style_data.get('template')

    templator = Template(template)

    for bib in ordered_cites:

        cur_bib = ordered_cites.get(bib)

        for item in cur_bib[0]:

            bib_data[item][token] = index

            index += 1

        for item in range(0, len(cur_bib[1])):

            output[cur_bib[1][item]] = templator.render(bib_data[cur_bib[0][item]])

        index = 1

    return output

def generate_works_cited( bib_data, ordered_cites, style_data, output ):

    index = 1

    token = style_data.get('in_text_style').get('index')

    bib_list = []

    bib_string = "" #' String containing works cited

    bib_string += style_data.get('title')

    for bib in ordered_cites:

        bib_list = ordered_cites.get(bib)

        for key in bib_list[0]:

            bib_data[key][token] = index

            templator = Template(style_data.get(bib_data[key].get('ENTRYTYPE')))
            bib_string += templator.render(bib_data[key])

            index += 1

        output[bib] = bib_string
        bib_string = ""
        index = 1

    return output

def get_reference_data( style_form, bib_tags, bib_data ):

    style_data = {}    #' A dictionary containing style information
    ordered_cites = {} #' A dictionary containing ordered citations
    output     = {}    #' A dictionary for Jinja2 templating on the final document

    # Read style file and extract style choice
    style_data = read_style_file(style_form)
    
    # Validate BibTeX syntax
    validate_syntax(bib_tags)

    # Validate that citations are in BibTeX database
    validate_citations(bib_tags, bib_data)

    # Organize citations according to style
    ordered_cites = organize_citations(bib_tags, bib_data, style_data.get('order'))

    # Generate in-text citations
    output = generate_citations(bib_data, ordered_cites, style_data.get('in_text_style'))

    # Generate reference page
    output = generate_works_cited(bib_data, ordered_cites, style_data, output)

    return output