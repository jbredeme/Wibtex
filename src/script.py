#!/usr/bin/python

############################################################
# @file   script.py
# @brief  script to execute the WibTeX RMS
#
# @author Charles Duso
# @date   May 4, 2017
############################################################

# Import libraries
import sys
import main
import logger
import style

# Extract the argument set
arguments = sys.argv

# Validate input
if len(sys.argv) < 5:
    print("Error: Too few arguments supplied to system.")
    print("Input is of the form: file.docx file.bib style output.docx")

elif len(sys.argv) > 5:
    print("Error: Too many arguments supplied to system.")
    print("Input is of the form: file.docx file.bib style output.docx")

else:

    input_doc   = arguments[1]
    input_bib   = arguments[2]
    style_input = arguments[3]
    output      = arguments[4]
    log         = logger.SimpleLogger()

    # Verify BibTeX database
    if not input_bib.endswith('.bib'):
        log.log_data("Error: Expected BibTeX file extension '.bib' for third argument")
        quit()

    # Verify input Word document
    if not input_doc.endswith('.docx'):
        log.log_data("Error: Expected Word file extension '.docx' for second argument")
        quit()

    # Verify output Word document
    if not output.endswith('.docx'):
        log.log_data("Error: Expected Word file extension '.docx' for fifth argument")
        quit()
    
    # Verify style file
    styles = style.get_valid_styles(log)
    if style_input not in styles and style_input.lower() not in styles and style_input.upper() not in styles:
        log.log_data("Error: Could not locate chosen style in style file.")
        quit()

    # Otherwise execute the program
    print("Executing WibTeX RMS...")
    main.execute(input_bib, input_doc, style_input, output, log)