############################################################
# @file   main.py
# @brief  module to execute the WibTeX Reference Management
#         System
#
# @author Hayden Aupperle, Jarid Bredemeier, Charles Duso
# @date   April 5, 2017
############################################################

################################################
# Import Python Modules
################################################
import style
import wibtex_parser
#import docx_io

################################################
# Construct Input Data
################################################
input_bib   = "test_data/demo_bib.bib"
input_doc   = "test_data/demo.docx"
input_style = "test_data/demo_style.json"
style_form  = "ccsc"

################################################
# Construct Output Data
################################################
bib_data    = {} #' The BibTeX database
bib_tags    = [] #' The list of BibTeX tags in the Word document
cite_data   = {} #' The formatted reference data to insert in the document

################################################
# Read BibTeX Database (wibtex_parser.py)
################################################

bib_data = wibtex_parser.parse(input_bib)

################################################
# Read Word Document (docx_io.py)
################################################

# TODO - Jarid's Code goes here
# bib_tags is the list of BibTeX markup from the document

################################################
# Generate Reference Data (style.py)
################################################

cite_data = style.get_reference_data(input_style, style_form, bib_tags, bib_data)

################################################
# Write to Word Document (docx_io.py)
################################################

# TODO - Jarid's Code goes here
# cite_data is the dictionary containing strings to inject in the XML

# DONE :)
