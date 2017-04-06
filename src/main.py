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

bib_data    = {}
cite_data   = {}

################################################
# Read BibTeX Database (wibtex_parser.py)
################################################

bib_data = wibtex_parser.parse(input_bib)

################################################
# Read Word Document (docx_io.py)
################################################

# TODO - Jarid's Code goes here

################################################
# Generate Reference Data (style.py)
################################################

cite_data = get_reference_data( style_file, style, doc_list, bib_data )

################################################
# Write to Word Document (docx_io.py)
################################################

# TODO - Jarid's Code goes here

# DONE :)
