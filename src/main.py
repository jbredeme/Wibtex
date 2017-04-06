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
import docx_io

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
xml         = "" #' The document string
output      = "test_data/demo_output.docx"

################################################
# Read BibTeX Database (wibtex_parser.py)
################################################

bib_data = wibtex_parser.parse(input_bib)

################################################
# Read Word Document (docx_io.py)
################################################

# Read in the document
docx = docx_io.Document(input_doc)

# Extract XML
xml  = docx.get_xml()

# Get the Latex Markup
bib_tags = docx.get_latex(xml)

# Insert jinja variables into the XML
xml = docx.insert_vars(xml, bib_tags)

print(bib_tags)

for i in range(0, len(bib_tags)):
    bib_tags[i] = str(bib_tags[i],'utf-8')

print(bib_tags)

# ################################################
# # Generate Reference Data (style.py)
# ################################################

# cite_data = style.get_reference_data(input_style, style_form, bib_tags, bib_data)

# ################################################
# # Write to Word Document (docx_io.py)
# ################################################

# # Take the dictonary with the template and run Jinja2 over it
# xml = docx.jinja_it(xml, cite_data)

# # Save the results into a new document
# docx.save_xml(docx.get_xml_tree(xml), output)

# DONE :)
