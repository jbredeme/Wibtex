############################################################
# @file   main.py
# @brief  module to execute the WibTeX Reference Management
#         System
#
# @author Charles Duso, Jarid Bredemeier
# @date   May 3, 2017
############################################################

################################################
# Import Python Modules
################################################

import logger
import style
import wibtex_parser
import docx_io

def execute( input_bib, input_doc, style_form, output_doc, log ):
    '''
    Executes the WibTeX RMS

    @param input_bib  the input BibTeX database file path
    @param input_doc  the input Microsoft Word document
    @param style_form the chosen reference style
    @param output_doc the chosen output Word document
    '''

    ################################################
    # Construct Output Data
    ################################################
    bib_data    = {} #' The BibTeX database
    bib_tags    = [] #' The dictionary of BibTeX tags in the Word document
    cite_data   = {} #' The formatted reference data to insert in the document
    xml         = "" #' The document string
    
    ################################################
    # Read BibTeX Database (wibtex_parser.py)
    ################################################

    bib_data = wibtex_parser.parse(input_bib, log)

    # ################################################
    # # Read Word Document (docx_io.py)
    # ################################################

    # Read in the document
    docx = docx_io.Document(input_doc)

    # Extract XML
    xml  = (docx.get_xml())

    # Extract BibTeX markup
    bib_tags, xml = docx.get_dict_xml(xml)

    ################################################
    # Generate Reference Data (style.py)
    ################################################

    cite_data = style.get_reference_data(style_form, bib_tags, bib_data, log)

    ################################################
    # Write to Word Document (docx_io.py)
    ################################################

    # Take the dictonary with the template and run Jinja2 over it
    xml = docx.jinja_it(xml, cite_data)

    # # Convert the html to xml
    xml = docx.html_to_xml(xml)

    # Save the results into a new document
    docx.save_xml(docx.get_xml_tree(xml), output_doc)

    # DONE :)