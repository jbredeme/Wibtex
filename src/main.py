# Author(s): Charles Duso, Jarid Bredemeier
# Date: Wednesday May 3, 2017
# File: main.py
# Copyright © 2017 All rights reserved 
#

import logger
import style
import wibtex_parser
import docx_io

# module to execute the WibTeX Reference Management System
# 
# @pram input_bib  the input BibTeX database file path.
# @pram input_doc  the input Microsoft Word document.
# @pram style_form the chosen reference style.
# @pram output_doc the chosen output Word document.
# @pram log
#
def execute(input_bib, input_doc, style_form, output_doc, log):

    # Construct Output Data
    bib_data = {}  	#=> the BibTeX database
    bib_tags = []  	#=> the dictionary of BibTeX tags in the Word document
    cite_data = {}  #=> the formatted reference data to insert in the document
    xml = ""  		#=> the document string

    bib_data = wibtex_parser.parse(input_bib, log)	#=> read BibTeX Database (wibtex_parser.py)
	
    docx = docx_io.Document(input_doc)				#=> read in the document
	
    xml = (docx.get_xml())							#=> extract XML
	
    bib_tags, xml = docx.get_dict_xml(xml)			#=> extract BibTeX markup

    # Generate Reference Data (style.py)
    cite_data = style.get_reference_data(style_form, bib_tags, bib_data, log)

	
    # Write to Word Document (docx_io.py)
    xml = docx.jinja_it(xml, cite_data)				#=> take the dictonary with the template and run Jinja2 over it
    xml = docx.html_to_wordlm(xml.decode('utf-8'))	#=> convert the html to xml
	
    tree = docx.get_xml_tree(xml.encode('utf-8'))
    docx.save_xml(tree, output_doc)					#=> save the results into a new document