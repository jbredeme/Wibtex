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
import logger
from jinja2 import Template, Environment, BaseLoader

################################################
# Function Definitions - Jinja2 Pipe & Filters
################################################


def font(value, size, color=None):
    '''
    Wraps Jinja2 contextual data in font size

    @param  value   the data to wrap
    @param  size    the value to generate tags with
    @return         the wrapped data
    '''

    if color:
        if isinstance(value, list):
            data = ""
            for item in value:
                data += '<font color="' + str(color) + ' \
                        size="' + size + '">' + str(item) + '</font>'
            return data

        elif isinstance(value, str):
            return '<font color="' + str(color) + ' \
                    size="' + size + '">' + str(item) + '</font>'
        else:
            return '<font color="' + str(color) + ' \
                    size="' + size + '">' + str(item) + '</font>'
    else:
        if isinstance(value, list):
            data = ""
            for item in value:
                data += '<font size="' + size + '">' + str(item) + '</font>'
            return data

        elif isinstance(value, str):
            return '<font size="' + size + '">' + value + '</font>'
        else:
            return '<font size="' + size + '">' + str(value) + '</font>'


def wrap_html(value, wrapper):
    '''
    Wraps Jinja2 contextual data in HTML-like fashion

    @param  value   the data to wrap
    @param  wrapper the value to generate tags with
    @return         the wrapped data
    '''

    if isinstance(value, list):
        data = ""
        for item in value:
            data += "<" + wrapper + ">" + str(item) + "</" + wrapper + ">"
        return data

    elif isinstance(value, str):
        return "<" + wrapper + ">" + value + "</" + wrapper + ">"
    else:
        return "<" + wrapper + ">" + str(value) + "</" + wrapper + ">"


def add_chars(value, char):
    '''
    Adds characters to end of Jinja2 contextual data

    @param  value   the data to filter
    @param  char    the value to append
    @return         the modified data
    '''

    if isinstance(value, str):
        return value + char
    elif isinstance(value, list):
        data = ""
        for item in value:
            data += str(item) + char
        return data
    else:
        return str(value) + char


def wrap(value, char):
    '''
    Wraps Jinja2 contextual data (specialized for braces/brackets)

    @param  value   the data to filter
    @param  char    the values to wrap
    @return         the modified data
    '''

    if isinstance(value, str):

        if char is ')' or char is '(':
            return '(' + value + ')'

        elif char is ']' or char is '[':
            return '[' + value + ']'

        return char + value + char

    elif isinstance(value, str):

        data = ""

        for item in value:
            if char is ')' or char is '(':
                data += '(' + str(item) + ')'
            elif char is ']' or char is '[':
                data += '[' + str(item) + ']'
            else:
                data += char + str(item) + char
        return data

    else:

        if char is ')' or char is '(':
            return '(' + str(value) + ')'

        elif char is ']' or char is '[':
            return '[' + str(value) + ']'

        return char + str(value) + char


def add_to_front(value, char):
    '''
    Adds characters to front of Jinja2 contextual data

    @param  value   the data to filter
    @param  char    the value to append
    @return         the modified data
    '''

    if isinstance(value, str):
        return char + value
    elif isinstance(value, list):
        data = ""
        for item in value:
            data += char + str(item)
        return data
    else:
        return char + str(value)


def authors_ccsc(value):
    '''
    Adds CCSC author format to Jinja2 contextual data

    @param  value   the data to filter
    @return         the modified data
    '''

    if isinstance(value, list):

        f_half = ""  # First half of an author list
        s_half = ""  # Second half of an author list

        if len(value) <= 1:
            f_half = re.findall('\w+,\s+', str(value[0]))
            s_half = re.findall('\s(\w)', str(value[0]))
            name = re.findall('\w+', str(value[0]))

            if not f_half:
                return name[0] + ' '
            elif not s_half:
                return f_half[0].split(',')[0] + ' '
            else:
                return str(name[0]) + ", "
            return ''

        else:
            string = ""

            for item in value:
                f_half = re.findall('\w+,\s+', str(item))
                s_half = re.findall('\s(\w)', str(item))
                name = re.findall('\w+', str(item))

                if not s_half:
                    string += name[0] + ", "
                elif not s_half:
                    string += f_half.split(',')[0] + ", "
                else:
                    string += str(name[0]) + ", "

            return string

    elif isinstance(value, str):
        return value + ', '

    else:
        return str(value)


def authors_acm(value):
    '''
    Adds ACM author format to Jinja2 contextual data

    @param  value   the data to filter
    @return         the modified data
    '''

    f_half = ""
    s_half = ""

    if isinstance(value, list):

        # If list of authors is one
        if len(value) <= 1:

            f_half = re.findall('\w+,\s+', str(value[0]))
            s_half = re.findall('\s(\w)', str(value[0]))
            name = re.findall('\w+', str(value[0]))

            # If no last name exists return name
            if not f_half:
                return name[0] + ' '

            # If the initials don't exist
            elif not s_half:
                return f_half[0].split(',')[0] + ' '

            # If initials exist, format them
            else:
                out = f_half[0]
                for item in s_half:
                    out += item + '.'
                return out + ' '

        # If list of authors is two
        elif len(value) == 2:
            first = ""
            second = ""

            f_half = re.findall('\w+,\s+', str(value[0]))
            s_half = re.findall('\s(\w)', str(value[0]))
            name = re.findall('\w+', str(value[0]))

            # If no last name exists return name
            if not f_half:
                first = name[0]

            # If the initials don't exist
            elif not s_half:
                first = f_half[0].split(',')[0]

            # If initials exist, format them
            else:
                first = f_half[0]
                for item in s_half:
                    first += item + '.'

            f_half = re.findall('\w+,\s+', str(value[1]))
            s_half = re.findall('\s(\w)', str(value[1]))
            name = re.findall('\w+', str(value[1]))

            # If no last name exists return name
            if not f_half:
                second = name[0]

            # If the initials don't exist
            elif not s_half:
                second = f_half[0].split(',')[0]

            # If initials exist, format them
            else:
                second = f_half[0]
                for item in s_half:
                    second += item + '.'

            return first + ' and ' + second + ' '

        # List of 3 or more authors
        else:

            out = ""
            temp = ""

            # For each author
            for index in range(0, len(value)):

                f_half = re.findall('\w+,\s+', str(value[index]))
                s_half = re.findall('\s(\w)', str(value[index]))
                name = re.findall('\w+', str(value[index]))

                # If second to last author
                if index == len(value) - 2:
                    if not f_half:
                        temp = name[0] + ' and '
                    elif not s_half:
                        temp = f_half[0].split(',')[0] + ' and '
                    else:
                        temp = f_half[0]
                        for item in s_half:
                            temp += item + '.'
                        temp += ' and '
                    out += temp

                # If last author
                elif index == len(value) - 1:
                    if not f_half:
                        temp = name[0]
                    elif not s_half:
                        temp = f_half[0].split(',')[0]
                    else:
                        temp = f_half[0]
                        for item in s_half:
                            temp += item + '.'
                    out += temp + ' '

                # If author not last nor second to last
                else:
                    if not f_half:
                        temp = name[0]
                    elif not s_half:
                        temp = f_half[0].split(',')[0]
                    else:
                        temp = f_half[0]
                        for item in s_half:
                            temp += item + '.'
                    out += temp + ', '

            return out

    return value


def authors_apa(value):
    '''
    Adds APA author format to Jinja2 contextual data

    @param  value   the data to filter
    @return         the modified data
    '''

    f_half = ""
    s_half = ""

    # For a list of authors
    if isinstance(value, list):

        # If we have a single author
        if len(value) <= 1:
            f_half = re.findall('\w+,\s+', str(value[0]))
            s_half = re.findall('\s(\w)', str(value[0]))
            name = re.findall('\w+', str(value[0]))

            # If no last name
            if not f_half:
                return name[0] + ' '

            # If no initials
            elif not s_half:
                return f_half[0].split(',')[0] + ' '

            # If initials and last name
            else:
                out = f_half[0]
                for item in s_half:
                    out += item + '.'

                return out + ' '

        # If we have two authors
        elif len(value) == 2:
            first = ""
            second = ""

            f_half = re.findall('\w+,\s+', str(value[0]))
            s_half = re.findall('\s(\w)', str(value[0]))
            name = re.findall('\w+', str(value[0]))

            # If no last name
            if not f_half:
                first = name[0]

            # If no initials
            elif not s_half:
                first = f_half[0].split(',')[0]

            # If initials and last name
            else:
                first = f_half[0]
                for item in s_half:
                    first += item + '.'

            f_half = re.findall('\w+,\s+', str(value[1]))
            s_half = re.findall('\s(\w)', str(value[1]))
            name = re.findall('\w+', str(value[1]))

            # If no last name
            if not f_half:
                second = name[0]

            # If no initials
            elif not s_half:
                second = f_half[0].split(',')[0]

            # If initials and last name
            else:
                second = f_half[0]
                for item in s_half:
                    second += item + '.'

            return first + ' and ' + second + ' '

        # If number of authors greater than 7
        elif len(value) > 7:

            out = ""
            temp = ""

            # For each author
            for index in range(0, len(value)):

                f_half = re.findall('\w+,\s+', str(value[index]))
                s_half = re.findall('\s(\w)', str(value[index]))
                name = re.findall('\w+', str(value[index]))

                # If we are at the sixth author
                if index == 6:
                    out += ' ... '

                # If we are between the first and last authors
                elif index > 6 and index <= len(value) - 2:
                    continue

                # If we are the second to last author
                elif index == len(value) - 1:

                    # If no last name
                    if not f_half:
                        temp = name[0]

                    # If no initials
                    elif not s_half:
                        temp = f_half[0].split(',')[0]

                    # If initials and last name
                    else:
                        temp = f_half[0]
                        for item in s_half:
                            temp += item + '.'
                    out += temp + ' '

                # If we are the first author
                else:

                    # If no last name
                    if not f_half:
                        temp = name[0]

                    # If no initials
                    elif not s_half:
                        temp = f_half[0].split(',')[0]

                    # If initials and last name
                    else:
                        temp = f_half[0]
                        for item in s_half:
                            temp += item + '.'
                    out += temp + ', '

            return out

        # If we have > 2 and < 7 authors
        else:

            out = ""
            temp = ""

            for index in range(0, len(value)):

                f_half = re.findall('\w+,\s+', str(value[index]))
                s_half = re.findall('\s(\w)', str(value[index]))
                name = re.findall('\w+', str(value[index]))

                if index == len(value) - 2:

                    # If no last name
                    if not f_half:
                        temp = name[0] + ' and '

                    # If no initials
                    elif not s_half:
                        temp = f_half[0].split(',')[0] + ' and '

                    # If initials and last name
                    else:
                        temp = f_half[0]
                        for item in s_half:
                            temp += item + '.'
                        temp += ' and '
                    out += temp

                elif index == len(value) - 1:

                    # If no last name
                    if not f_half:
                        temp = name[0]

                    # If no initials
                    elif not s_half:
                        temp = f_half[0].split(',')[0]

                    # If initials and last name
                    else:
                        temp = f_half[0]
                        for item in s_half:
                            temp += item + '.'
                    out += temp + ' '

                else:

                    # If no last name
                    if not f_half:
                        temp = name[0]

                    # If no initials
                    elif not s_half:
                        temp = f_half[0].split(',')[0]

                    # If initials and last name
                    else:
                        temp = f_half[0]
                        for item in s_half:
                            temp += item + '.'
                    out += temp + ', '

            return out

    elif isinstance(value, str):
        return value + ', '

    else:
        return str(value) + ', '


def get_last(value):
    '''
    Extracts the last name of an author from Jinja2 contextual data

    @param  value   the data to filter
    @return         the modified data
    '''

    result = ""

    if isinstance(value, list):

        result = re.findall('^(.+?),', str(value[0]))

        if result != []:
            return result[0]
        else:
            return str(value[0])

    elif isinstance(value, str):

        result = re.findall('^(.+?),', value)

        if result != []:
            return result[0]

        else:
            return value

    else:
        return str(value)


def construct_env():
    '''
    Constructs a Jinja2 environment with all filter functions added

    @return the Jinja2 custom environment
    '''

    environment = Environment(loader=BaseLoader)
    environment.filters['wrap_html'] = wrap_html
    environment.filters['add_chars'] = add_chars
    environment.filters['wrap'] = wrap
    environment.filters['font'] = font
    environment.filters['add_to_front'] = add_to_front
    environment.filters['authors_ccsc'] = authors_ccsc
    environment.filters['authors_acm'] = authors_acm
    environment.filters['authors_apa'] = authors_apa
    environment.filters['get_last'] = get_last

    return environment

################################################
# Function Definitions - Style File Interaction
################################################


def get_valid_styles(log):
    '''
    Validates the styles from the config folder and returns
    a list of valid styles

    @return a list of valid styles
    '''

    style_file = "../config/styles.json"
    valid_styles = []

    # Open the pre-pathed style file
    with open(style_file, 'r') as f:
        try:
            data = json.load(f)
        except ValueError:
            log.log_data("\nError: Could not read style file.")
            return ""

    # For each style in the style file
    for key in data:

        style_data = data.get(key)

        # If style cannot be accessed log it
        if style_data is None:
            log.log_data('\nERROR - Could not retrieve style template')
            continue

        else:
            order = {}
            in_text = {}
            title = ""
            default = ""

            # Verify order field and its sub-fields exist
            order = style_data.get('order')
            if order is None:
                log.log_data('\nERROR - Could not access "order" \
                             field in style template')
                continue
            else:
                if 'method' not in order or 'sortby' not in order:
                    log.log_data('\nERROR - Missing "method" or "sortby" \
                                 values in "order" field of style template.')
                    continue

            # Verify in_text_style field and its sub-fields exist
            in_text = style_data.get('in_text_style')
            if in_text is None:
                log.log_data('\nERROR - Could not access "in_text_style"\
                             field in style template')
                continue
            else:
                if 'index' not in in_text or 'template' not in in_text:
                    log.log_data('\nERROR - Could not access "index" or\
                                 "template" in "in_text_style" field of\
                                 style template')
                    continue

            # Verify title field exists
            title = style_data.get('title')
            if title is None:
                log.log_data('\nERROR - Could not access "title" field \
                             in style template')
                continue
            else:
                if 'key' not in title or 'template' not in title:
                    log.log_data('\nERROR - Missing "key" or "template"\
                                 values in "title" field of style template.')
                    continue

            # Verify default_style field exists
            default = style_data.get('default_style')
            if default is None:
                log.log_data('\nERROR - Could not access "default_style"\
                             field in style template')
                continue

        # If key is valid, then append it to the list
        valid_styles.append(key)

    return valid_styles


def read_style_file(style_form, log):
    '''
    Extracts a specified style from a style file

    @param  style_form the style format to extract
    @return            a dictionary containing style data
    '''

    style_file = "../config/styles.json"

    with open(style_file, 'r') as f:
        try:
            data = json.load(f)
        except ValueError:
            data = {}
            log.log_data("\nError: Could not read style file.")

    return data.get(style_form)

################################################
# Function Definitions - Style Data Formatting
################################################


def validate_citations(bib_tags, bib_data, log):
    '''
    Verifies that a set of BibTeX tags extracted from a BibTeX database exist

    @param  bib_tags BibTeX tags extracted from a document
    @param  bib_data BibTeX database
    '''

    sub_dict = {}
    cite_dict = {}
    key = ''
    invalid_keys = []
    temp_sub = {}
    temp_final = {}

    # For each bibliography
    for super_key in bib_tags:

        sub_dict = bib_tags.get(super_key)
        cite_dict = sub_dict.get('citations')

        # For each citation
        for sub_key in cite_dict:

            key = cite_dict.get(sub_key).get('bib_key')

            if key in bib_data:
                continue
            else:
                # Remove it from the key list
                log.log_data(
                    "\nERROR: Could not find key referened \
                    in document within BibTeX database: " + str(sub_key))
                invalid_keys.append(key)
                continue

    return bib_tags


def sort_alphabetical(bib_key, sort_list, ordered_cites):
    '''
    Sorts a set of citations alphabetically

    @param  bib_key         the associated reference section
    @param  sort_list       the list of items to sort
    @param  orderered_cites the dictionary containing sorted reference sections
    @return                 ordered dictionary sections of the citations
    '''

    sorted_list = []
    sorted_tags = []
    to_sort = []
    jinja_list = []
    outer_list = []

    temp_str = ""

    # For each entry in bibliography
    for item in sort_list:

        # Sort a list of authors or titles for a BibTeX entry
        item[2] = sorted(item[2], key=str.swapcase)

        # Append the list of sorted authors/titles
        to_sort.append(item[2][0])

    # Sort the list of authors/titles/other from all acquired BibTeX entries
    sorted_list = sorted(to_sort, key=str.swapcase)

    # Create a list equal to the size of the sorted list
    # TODO - Verify
    for index in sorted_list:
        sorted_tags.append(0)

    # Create a list equal to the size of the sorted list
    for index in sorted_list:
        jinja_list.append(0)

    # Extract the citation tags
    for index in range(0, len(sorted_list)):

        for item in range(0, len(sorted_list)):

            # If item is in list to sort
            if sorted_list[index] in sort_list[item][2]:

                # Extract information and negate this item
                # The same author may appear for many entries
                # We choose the first available match and then nullify it
                jinja_list[index] = sort_list[item][0]
                sorted_tags[index] = sort_list[item][1]
                sort_list[item][2] = ['#']
                break

    # Add sorted items to the master list
    outer_list.append(sorted_tags)
    outer_list.append(jinja_list)

    # Associate the master list with a reference section
    ordered_cites[bib_key] = outer_list

    return ordered_cites


def organize_citations(bib_tags, bib_data, order):
    '''
    Sorts a set of citations based on order chosen (alphabetic/numeric)

    @param  bib_tags BibTeX tags extracted from a document
    @param  bib_data BibTeX database
    @param  order    the order with which to arrange the tags
    @return          ordered list of the citations extracted
    '''

    # Extract sorting method from style format
    method = order.get('method')
    sort_by = order.get('sortby')

    jinja_var = ''
    sort_item = ''

    tag_list = []
    jinja_list = []
    outer_list = []
    triplet = []

    # Dictionary that will contain sets of ordered citations
    ordered_cites = {}

    # If we are to sort alphabetically
    if method == 'alpha':

        # If we are to sort via authors
        if sort_by == 'author':

            # For each bibliography section
            for bib in bib_tags:

                # Grab the list of citations
                citations = bib_tags.get(bib).get('citations')

                # Grab the entry key and sorting token
                for entry_key in citations:

                    bib_key = citations.get(entry_key).get('bib_key')
                    jinja_var = citations.get(entry_key).get('jinja_var')

                    if not bib_data.get(bib_key):
                        continue

                    # If author in BibTeX database
                    if 'author' in bib_data.get(bib_key):

                        sort_item = bib_data.get(bib_key).get('author')

                    # If title in BibTeX database and NOT author
                    elif 'title' in bib_data.get(bib_key):

                        sort_item = bib_data.get(bib_key).get('title')

                    # No title and no author (unlikely), but grab next resource
                    else:
                        # Grab next available value
                        sort_item = next(
                            iter(
                                bib_data.get(bib_key).values()
                                )
                            )

                    # Create a triplet of jinja variable, BibTeX key, and value
                    triplet.append(jinja_var)
                    triplet.append(bib_key)
                    triplet.append(sort_item)

                    # Append triplet to list to sort
                    tag_list.append(triplet)

                    triplet = []

                # Sort this set of bibtex citations for this reference section
                ordered_cites = sort_alphabetical(
                    bib_tags.get(bib).get('jinja_var'),
                    tag_list, ordered_cites)
                tag_list = []

        # If we are to sort via titles
        elif sort_by == 'title':

            # For each bibliography section
            for bib in bib_tags:

                # Grab the list of citations
                citations = bib_tags.get(bib).get('citations')

                # Grab the entry key and sorting token
                for entry_key in citations:

                    bib_key = citations.get(entry_key).get('bib_key')
                    jinja_var = citations.get(entry_key).get('jinja_var')

                    if not bib_data.get(bib_key):
                        continue

                    # If title in BibTeX database
                    if 'title' in bib_data.get(bib_key):

                        sort_item = bib_data.get(bib_key).get('title')

                    # If author in BibTeX database and NOT title
                    elif 'author' in bib_data.get(bib_key):

                        sort_item = bib_data.get(bib_key).get('author')

                    # If author and title NOT in BibTeX database
                    else:
                        # Grab next available value
                        sort_item = next(
                            iter(
                                bib_data.get(bib_key).values()
                                )
                            )

                    # Create a triplet of jinja variable, BibTeX key
                    triplet.append(jinja_var)
                    triplet.append(bib_key)
                    triplet.append(sort_item)

                    # Append triplet to list to sort
                    tag_list.append(triplet)

                    triplet = []

                # Sort this set of bibtex citations for this reference section
                ordered_cites = sort_alphabetical(
                    bib_tags.get(bib).get('jinja_var'),
                    tag_list, ordered_cites)
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

                    sort_item = next(
                        iter(
                            bib_data.get(bib_key).values()
                            )
                        )

                    # Create a triplet of jinja variable, BibTeX key
                    triplet.append(jinja_var)
                    triplet.append(bib_key)
                    triplet.append(sort_item)

                    tag_list.append(triplet)

                    triplet = []

                # Sort this set of bibtex citations for this reference section
                ordered_cites = sort_alphabetical(
                    bib_tags.get(bib).get('jinja_var'),
                    tag_list, ordered_cites)
                tag_list = []

    # Default to first-written-first-cited
    else:

        # This is the count of citations used to interface with the Jinja
        c_count = 0

        # Access string used to retrieve document keys extracted
        access_str = ""

        # For each reference section
        for key in bib_tags:

            citations = bib_tags.get(key).get('citations')

            # For each tag in the reference section
            for tag in range(0, len(citations.keys())):

                # Generate the access key (i.e. 'cite + X')
                access_str = "cite" + str(c_count)

                # Append bib key and corresponding jinja var to lists
                tag_list.append(citations[access_str]['bib_key'])
                jinja_list.append(citations[access_str]['jinja_var'])

                c_count += 1

            # Reset count for next access section
            c_count = 0

            # Append list of jinja vars and bib keys to master list
            outer_list.append(tag_list)
            outer_list.append(jinja_list)

            # Associate a reference section with the master list and reset
            ordered_cites[key] = outer_list
            tag_list = []
            jinja_list = []
            outer_list = []

    return ordered_cites


def generate_citations(bib_data, ordered_cites, style_data, environment):
    '''
    Generates in-text citations for the document from a pre-ordained
    style

    @param bib_data      a dictionary containing BibTeX database entries
    @param ordered_cites a dictionary containing citation keys/jinja variables
    @param style_data    a dicitonary containing style template data
    @param environment   a Jinja2 environment with custom filters

    @return              a dictionary containing formatted reference data
    '''

    output = {}
    cur_bib = {}

    index = 1

    token = style_data.get('index')
    template = style_data.get('template')

    templator = environment.from_string(template)

    # For each reference section
    for bib in ordered_cites:

        # Extract the current reference section
        cur_bib = ordered_cites.get(bib)

        # For each citation tag
        for item in cur_bib[0]:

            # Set the numerical index of that citation
            if item:
                bib_data[item][token] = index

            # Increment the index
            index += 1

        # For each item in the current reference section
        for item in range(0, len(cur_bib[1])):

            # Render the template string and assign the key as its jinja
            output[cur_bib[1][item]] = templator.render(
                bib_data[cur_bib[0][item]])

        # Reset the index
        index = 1

    return output


def generate_works_cited(
        bib_data, ordered_cites,
        style_data, environment, output):
    '''
    Generates reference sections based upon a preordained style

    @param bib_data      a dictionary containing BibTeX database entries
    @param ordered_cites a dictionary containing citation keys/jinja variables
    @param style_data    a dicitonary containing style template data
    @param environment   a Jinja2 environment with custom filters
    @param output        a dictionary containing formatted reference data

    @return              a dictionary containing formatted reference data
    '''

    # Index for numbering citations
    index = 1

    # Extract the in-text citation token as it may be used
    token = style_data.get('in_text_style').get('index')

    bib_list = []

    bib_string = ""

    header = {}

    extended_styles = {}
    alt_style = {}

    found = False

    default = style_data.get('default_style')
    template = ""
    entrytype = ""

    # For each bibliography
    for bib in ordered_cites:

        # Constrtuct the reference title
        header[style_data.get('title').get('key')] = (
            style_data.get('title').get('key')
        )
        templator = environment.from_string(
            style_data.get('title').get('template'))
        bib_string += templator.render(header)

        # Extract the reference section
        bib_list = ordered_cites.get(bib)

        # For each citation key
        for key in bib_list[0]:

            # Add the numerical token to the
            bib_data[key][token] = index

            # Extract the entry type
            entrytype = bib_data[key]['ENTRYTYPE']

            # Construct the template from the BibTeX entry key
            extended_styles = style_data.get('extended_styles')

            # Set template to the default incase we can't find a valid
            template = default

            # Grab the preferred or supported style, else default to default
            if extended_styles:

                # For each alternate style
                for type in extended_styles:

                    # Grab the alternate style
                    alt_style = extended_styles.get(type)

                    # If BibTeX entry part of preferred
                    if entrytype in alt_style.get('preferred'):
                        template = alt_style.get('template')
                        found = True

                    # If BibTeX entry part of supported and not preferred
                    if (
                        found is False and
                            entrytype in alt_style.get('supported')):
                            template = alt_style.get('template')

            # Render the chosen template
            templator = environment.from_string(template)

            # Add reference string to master reference
            bib_string += templator.render(bib_data[key])

            # Reset the filtering tokens
            found = False

            # Increment the index counter
            index += 1

        # Add the formatted reference string to the master dictionary
        output[bib] = bib_string

        # Reset the index and the reference string
        bib_string = ""
        index = 1

    return output


def get_reference_data(style_form, bib_tags, bib_data, log):

    style_data = {}
    ordered_cites = {}
    output = {}

    # Read style file and extract style choice
    style_data = read_style_file(style_form, log)

    # Validate that citations are in BibTeX database
    bib_tags = validate_citations(bib_tags, bib_data, log)

    # Organize citations according to style
    ordered_cites = organize_citations(
        bib_tags, bib_data,
        style_data.get('order'))

    # Construct the Jinja2 environment
    environment = construct_env()

    # Generate in-text citations
    output = generate_citations(
        bib_data, ordered_cites,
        style_data.get('in_text_style'), environment)

    # Generate reference page
    output = generate_works_cited(
        bib_data, ordered_cites, style_data, environment, output)

    return output
