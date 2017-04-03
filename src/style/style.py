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
    
    # Ensure that last item is bibliography tag
    if not regexp.search(doc_list[(len(doc_list) - 1)]):
        print("Error: '\\bibliography{}' should be final tag in document.")

    # Validate that a bibliography tag exists
    for item in range(0, len(doc_list)):
        if regexp.search(doc_list[item]):
            print(doc_list[item])
    return

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

test = ['\\cite{demo}', '\\cite{demo2}', '\\cite{demo3}', '\\bibliography{demo4}']
#print(test)

#print(strip_markup(test))
validate_syntax(test)