import re
import json

# Style File Extraction

def validate_style( file, style ):
    #todo
    return

def read_style_file( file, style ):
    with open(file, 'r') as f:
        try:
            data = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            data = {}

    return data[style]

# Reference Data Generation

def validate_syntax( bib_list ):
    regexp = re.compile(r'\\bibliography\{(.*?)\}')
    
    # Ensure that last item is bibliography tag - TODO may be dropped
    if not regexp.search(bib_list[(len(bib_list) - 1)]):
        print("Error: '\\bibliography{}' should be final tag in document.")

    # Validate that a bibliography tag exists
    valid = False
    for item in range(0, len(bib_list)):
        if regexp.search(bib_list[item]):
            valid = True

    return

def split_citations( doc_list ):

    regexp = re.compile(r'\\bibliography\{(.*?)\}')
    bib_count = 0
    num_list  = []

    # Count the number of bibliography tags
    for item in range(0, len(doc_list)):
        if regexp.search(doc_list[item]):
            num_list.append(item)
            bib_count += 1

    # Create a list or list of lists
    if bib_count > 1:
        bib_list  = []
        temp_list = []
        for item in range(0, len(doc_list)):
            if item in num_list:
                temp_list.append(doc_list[item])
                bib_list.append(temp_list)
                temp_list = []
            else:
                temp_list.append(doc_list[item])
    else:
        bib_list = doc_list

    return bib_list

def extract_citations( doc_list ):
    #TODO - May not be needed
    return

def extract_bibliography( doc_list ):
    #TODO - May not be needed
    return

def strip_markup( doc_list ):

    if any(isinstance(el, list) for el in doc_list):
        for sub_list in doc_list:
            for item in range(0, len(sub_list)):
                sub_list[item] = re.sub(r'\\cite\{', '', sub_list[item])
                sub_list[item] = re.sub(r'\\bibliography\{', '', sub_list[item])
                sub_list[item] = re.sub(r'\}', '', sub_list[item])
    else:
        for item in range(0, len(doc_list)):
            doc_list[item] = re.sub(r'\\cite\{', '', doc_list[item])
            doc_list[item] = re.sub(r'\\bibliography\{', '', doc_list[item])
            doc_list[item] = re.sub(r'\}', '', doc_list[item])

    return doc_list

def get_dict_from_entry( bib_list, key ):
    for dict in bib_list:
        if dict['ID'] == key:
            return dict

def set_dict_index( bib_list, index, author, id, value):
    for item in range(0, len(bib_list)):
        if bib_list[item]['ID'] == id and  bib_list[item]['author'] == author :
             bib_list[item]['value'] = value
    return bib_list

def validate_citations( citations ):
    #todo
    return

def remove_duplicates( list ):
    seen = set()
    seen_add = seen.add
    return [x for x in list if not (x in seen or seen_add(x))]

def organize_citations( citations, bib_list, style_data ):

    """ TODO - if alpha:
        value = 0
        temp_list = citations[0:(len(citations) - 1)]
        auth_list = []
        auth_dict_list = []
        auth_entry_dict = {}
        
        # Get the authors from the list of citations
        for entry in temp_list:
            id = (get_dict_from_entry(bib_list, entry)['author'])[0]

            auth_entry_dict[id] = entry
            auth_dict_list.append(auth_entry_dict)
            auth_entry_dict = {}

            auth_list.append(id)

        auth_list = sorted(auth_list, key=str.lower)
        print(auth_list)
        print(auth_dict_list)

        #for item in range(0, len(auth_list)):
        #    auth_list[item] = auth_entry_dict[auth_list[item]]            

        #print(auth_list) """

    if any(isinstance(el, list) for el in citations):

        for sub_list in citations:
            temp_list = sub_list[0:(len(sub_list) - 1)]
            temp_list = remove_duplicates(temp_list)
            print(temp_list)
    else:
        # Remove duplicate data
        temp_list = citations[0:(len(citations) - 1)]
        temp_list = remove_duplicates(temp_list)
        print(temp_list)
        
    return citations

def generate_citations( citations ):
    #todo
    return

def generate_works_cited( citations ):
    return

def get_reference_data( style_file, doc_list ):
    return

test = ['\\cite{article_okay}', '\\cite{article_bad}', '\\cite{article_good}', '\\bibliography{test}',
        '\\cite{demo5}', '\\cite{demo6}', '\\cite{demo7}', '\\bibliography{demo8}',
        '\\cite{demo92}', '\\cite{demo10}', '\\cite{demo11}', '\\bibliography{demo12}',
        '\\cite{demo13}', '\\cite{demo14}', '\\cite{demo15}', '\\bibliography{demo16}']

validate_syntax(test)
test = split_citations(test)
test = strip_markup(test)

# load from file:
with open('test.json', 'r') as f:
    try:
        data = json.load(f)
    # if the file is empty the ValueError will be thrown
    except ValueError:
        data = {}

organize_citations(test, data, None)
read_style_file('style.json', 'ccsc')

