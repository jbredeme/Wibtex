import re

# Style File Extraction

def validate_style_file( file ):
    #todo
    return

def read_style_file( file ):
    #todo
    return

# Reference Data Generation

def validate_syntax( doc_list ):
    regexp = re.compile(r'\\bibliography\{(.*?)\}')
    
    # Ensure that last item is bibliography tag - TODO may be revised
    if not regexp.search(doc_list[(len(doc_list) - 1)]):
        print("Error: '\\bibliography{}' should be final tag in document.")

    # Validate that a bibliography tag exists - TODO may be unnecessary
    for item in range(0, len(doc_list)):
        if regexp.search(doc_list[item]):
            print(doc_list[item])
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
    #todo
    return

def extract_bibliography( doc_list ):
    return

def strip_markup( doc_list ):
    for item in range(0, len(doc_list)):
        doc_list[item] = re.sub(r'\\cite\{', '', doc_list[item])
        doc_list[item] = re.sub(r'\\bibliography\{', '', doc_list[item])
        doc_list[item] = re.sub(r'\}', '', doc_list[item])
    return doc_list

def validate_citations( citations ):
    #todo
    return

def organize_citations( citations ):
    #todo
    return

def generate_citations( citations ):
    #todo
    return

def generate_works_cited( citations ):
    return

def get_reference_data( style_file, doc_list ):
    return
