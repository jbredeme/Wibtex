import re

# Style File Extraction

def validate_style_file( file ):
    #todo
    return

def read_style_file( file ):
    #todo
    return

# Reference Data Generation

def strip_markup( citations ):
    for item in range(0, len(citations)):
        citations[item] = re.sub(r'\\cite\{', '', citations[item])
        citations[item] = re.sub(r'\\bibliography\{', '', citations[item])
        citations[item] = re.sub(r'\}', '', citations[item])
    return citations

def validate_citations( citations ):
    #todo
    return

def organize_citations( citations ):
    #todo
    return

def generate_references( citations ):
    #todo
    return
