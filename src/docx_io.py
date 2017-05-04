 #
 # Author: Jarid Bredemeier
 # Email: jpb64@nau.edu
 # File: docx_io.py
 # Copyright © 2017 All rights reserved 
 #
 
import sys, os, shutil, re, zipfile, tempfile
from jinja2 import Template, Environment
from bs4 import BeautifulSoup
from lxml import etree

class Document:
	#	# __init__ is the the constructor for the document class that stores a qualified path to a target Open file.
	#
	# @pram filename is the directory\name of the target Open XML document file.
	#	
	def __init__(self, filename):
		self.filename = filename
		
		try:
			self.zipfile = zipfile.ZipFile(filename)
			
		except(OSError, IOError) as e:
			print("Unable to read file:", self.filename)
			
				
	# get_xml extracts the Open XML contents from a document zip compression
	#
	# @returns string containing the Open XML.
	#
	def get_xml(self):
		try:
			with open(self.filename, 'rb') as fh:
				unzipped = zipfile.ZipFile(fh)
				xml_content = unzipped.read('word/document.xml')	#=> Retrieve Open XML
				return xml_content.decode("utf-8")

		except(OSError, IOError) as e:
			print("Unable to read file:", self.filename)
	
			
	# save_xml copies the contents from the orginal Open XML document compression replacing all the content inside the 
	# document.xml with the xml_content string and saves it into a new Open XML document compression by the specified name
	# indicated by output_filename.
	# 
	# @pram xml_content is a string containing some data that will be written into the document.xml.
	# @pram output_filename is a string that is used to name the new Open XML document.
	# @returns true indicating successful document creation; false upon failure to create document
	#
	def save_xml(self, xml_content, output_filename):
		dir = tempfile.mkdtemp()

		self.zipfile.extractall(dir)
		
		try:
			with open(os.path.join(dir,'word/document.xml'), 'w') as f:
				xml_str = etree.tostring(xml_content, pretty_print=True).decode("utf-8")
				f.write(xml_str)
				
			filenames = self.zipfile.namelist()	#=> Get a list of all the files in the original docx zipfile

			# Create the new zip file and add all the files into the archive
			zip_copy_filename = output_filename
			with zipfile.ZipFile(zip_copy_filename, "w", zipfile.ZIP_DEFLATED) as docx:
				for filename in filenames:
					docx.write(os.path.join(dir, filename), filename)
					
			shutil.rmtree(dir)	#=> Clean up the dir
			return True
			
		except(OSError, IOError) as e:
			print("Unable to save file:", output_filename)
			return False
			
			
	# get_xml_tree create an element or tree of elements from a string containing XML.
	# 
	# @returns a new element instance represented by the XML.
	#
	def get_xml_tree(self, xml_string):
	   return etree.fromstring(xml_string)

	   
	# remove_markup removes any embedded Open XML markup inside a latex element as a result of formatting
	# that occurred during document design
	# 
	# @pram list is a python list of string elements representing latex markup
	# @return list of string entries without Open XML mkarkup elements
	#	
	def remove_markup(self, list):
		pattern = re.compile(r'<w:[^>]*>|</w:[^>]*>|')
		
		# Iterate through the list removing any Open XML markup embedded inside latex elements
		for i in range(0, len(list)):
			list[i] = pattern.sub('', list[i])
		
		return list
		
		
	# This function calls the Jinja2 templating service on an Open XML docx content string in conjunction with a dictionary to match variable and value
	# pairs for substitution.
	#
	# @pram xml is a string containing xml content and jinja variables.
	# @pram dictionary of jinja variables and values used for xml targeting and replacement. 
	# @returns an xml string that is been processed by the templating engine
	# 
	def jinja_it(self, xml, dictionary):
		template = Template(xml)
		xml = template.render(dictionary).encode("utf-8")
		
		return xml

		
	# This function removes any embedded Open XML markup inside a latex tag that is a result of formatting durning document creation / editing.
	# Next it extracts and returns only the content inside the curly braces to the calling function. This is used to generate bibtex database
	# reference keys.
	#
	# @pram latex is a string containing latex markup.
	# @returns a string containing all the contents inside curly braces, None if no value was extracted.
	#
	def get_bib_key(self, latex):
		ptn_markup = re.compile(r'<w:[^>]*>|</w:[^>]*>|')
		ptn_key = re.compile(r'{(.*?)}')

		culled = ptn_key.findall(ptn_markup.sub('', latex), re.IGNORECASE)
		
		if not len(culled) == 0:
			return culled[0]
		
		else:
			return None

			
	# This function reads in an Open XML string from a docx document and parses any latex markup. Next it takes the latex markup and generates a dictionary
	# of bibliographies and nested inside each dictionary entry is another dictionary of associated citations. The design objective is to allow support for
	# referencing multiple bibliographies in a single docx document and their assoicate citations.
	#
	# @pram xml is a string containing Open XML.
	# @returns a tuple; first value is a python dictionary of the latex markup and jinja key variables generated for bibliographies and citations; second value 
	#          is a string containing the Open XML content of a docx document with the latex markup replaced with jinja templating variables.
	#
	def get_dict_xml(self, xml):
		bibs = dict()				#=> stores all bibliography enties
		citations = dict()			#=> stores all citation entries
		bib_count = 0				#=> bibliography counter
		cite_count = 0				#=> citation counter

		list = re.split(r'(\\bibliography\s*{[^}]*}|\\bib\s*{[^}]*})', xml)						#=> spit xml string into a list defined by a pattern, capture pattern
		
		for x in range(0, len(list)):															#=> iterate through the list from regex split	
			if not re.search(r'(\\bibliography\s*{[^}]*}|\\bib\s*{[^}]*})', list[x]) is None:	#=> check for a list entry for bibliography data
				try:
					cites = re.findall(r'\\cite\s*{[^}]*}', list[x - 1], re.IGNORECASE) 		#=> step back one index and find all the cite markup in the text block
					
					for i in range(0, len(cites)):												#=>  iterate through the parsed cite markup
						is_duplicate = False												
						
						for key, val in citations.items():										#=> avoid dupicate dictionary entries by checking bib_key values for matches
							if 'bib_key' in val:
								if val['bib_key'] == str(self.get_bib_key(cites[i])):
									is_duplicate = True
									
									if not val['payload'] == cites[i]:							#=> check if payload is different this can happen when the contents are the same but markup is not
										list[x - 1] = list[x - 1].replace(str(cites[i]), '{{ ' + val['jinja_var'] + ' }}')
						
									break
									
						if is_duplicate == False:												#=> add new entry if a dupicate is not found
							citations["cite" + str(cite_count)] = {'jinja_var': 'B' + str(bib_count) + 'C' + str(cite_count), 'bib_key': str(self.get_bib_key(cites[i])), 'payload': cites[i]}
							list[x - 1] = list[x - 1].replace(str(cites[i]), '{{ ' + 'B' + str(bib_count) + 'C' + str(cite_count) + ' }}')
							cite_count += 1		
							
					bibs["bib" + str(bib_count)] = {'jinja_var': 'B' + str(bib_count), 'bib_key': str(self.get_bib_key(list[x])), 'payload': list[x], 'citations': citations}
					list[x] = '{{ ' + str(bibs["bib" + str(bib_count)]['jinja_var']) + ' }}'
					bib_count += 1
					citations = dict()
					cite_count = 0
					
				except IndexError:
					return None
					
		xml = ''.join(list)			#=> convert list back into a string		
		
		return bibs, xml

		
	# This is a utility function that prints the contents of a Wibtex document dictionary
	#
	# @pram dictionary is a reference variable to a dictionary object.
	#
	def print_dict(self, dictionary):
		# Print Contents
		for key, val in dictionary.items():
			print("Bibliography")
			print("\tJinja Variable:\t" + str(val['jinja_var']))
			print("\tBib Key:\t" + str(val['bib_key']))
			print("\tBib Payload:\t" + str(val['payload']))
			print("\tCitations:")
			for ke2, val2 in val['citations'].items():
				print("\t\tJinja Variable:\t" + str(val2['jinja_var']))
				print("\t\tBib Key:\t" + str(val2['bib_key']))
				print("\t\tPayload:\t" + str(val2['payload']) + "\n")
			print("------------------------------------------------------------")
			print("------------------------------------------------------------\n")
			
			
# -------------------------------------------------------------------------------------------------------------------------

# this html parser takes non-nested html tags content is split up into blocks, blocks are defined by an opening 
# and closing tag element and any content that they surround. In case where a tag is a nested tag containing two
# or more children the parent tag is processed first, then the child, and the child of the child and so forth. 
# To illistrate this idea say you start off with a string like this 'some <b><i>simple</i></b> text' -> 
# '<b><i>simple</i></b>' -> '<i>simple</i>'. Since we have two of splits of the same content we need to prevent 
# processing the same tag more then once. In order do accomplish this I compare the contents of the child tag to
# the contents of its parent. If the contents match I know that the child is a decendant of the parent and I no 
# longer need to process any sibilings of the parent because the parent tag contains all the relevant data I need.

#sampleText = 'This is a <b></b>test string to <i>test</i> simple HTML <u>markup</u> elements <b><i>converson</i></b> to <u><b><font size=18>Open XML markup</font></b></u> for word <font size="15">document</font> formatting. <font size=6><b><u><i>For nested markup they</i></u></b></font> can appear in any order, font size value can be quote or not quoted'
# sampleText = '<u><i><b>Simple text substitution</b></i></u>'
# soup = BeautifulSoup(sampleText, 'html.parser')
# print('\n-------------------- Original text feed --------------------')
# print('\n' + sampleText + '\n')
# print('------------------------------------------------------------\n')
	
# for e in soup.findAll():
	# chowder = BeautifulSoup(str(e), 'html.parser')
	
	# if chowder.b != None and chowder.font != None and chowder.i != None and chowder.u != None:		#=> contains bold, font, italic, and underline html markup elements
		# if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			# print('Oringal markup:\n\t' + str(e))
			# print('\tLine analysis: contains bold, font, italic, and underline html markup elements\n')
			# print('Open XML Markup Equivalent:')
			# print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:b w:val="1"/><w:i w:val="1"/><w:sz w:val="' + str(chowder.font['size']) + '"/><w:szCs w:val="' + str(chowder.font['size']) + '"/><w:u w:val="single"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			# print('\n--\n')
		
	# if chowder.b != None and chowder.font != None and chowder.i != None and chowder.u == None:		#=> Line analysis: contains bold, font, and italic html markup elements
		# if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			# print('Oringal markup:\n\t' + str(e))
			# print('\tLine analysis: contains bold, font, and italic html markup elements\n')
			# print('Open XML Markup Equivalent:')
			# print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:b w:val="1"/><w:i w:val="1"/><w:sz w:val="' + str(chowder.font['size']) + '"/><w:szCs w:val="' + str(chowder.font['size']) + '"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			# print('\n--\n')

	# if chowder.b != None and chowder.font != None and chowder.i == None and chowder.u != None:		#=> Line analysis: contains bold, font, and underline html markup elements
		# if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			# print('Oringal markup:\n\t' + str(e))
			# print('\tLine analysis: contains bold, font, and underline html markup elements\n')
			# print('Open XML Markup Equivalent:')
			# print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:b w:val="1"/><w:sz w:val="' + str(chowder.font['size']) + '"/><w:szCs w:val="' + str(chowder.font['size']) + '"/><w:u w:val="single"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			# print('\n--\n')		
			
	# if chowder.b != None and chowder.font == None and chowder.i == None and chowder.u != None:		#=> Line analysis: contains bold, and underline html markup elements
		# if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			# print('Oringal markup:\n\t' + str(e))
			# print('\tLine analysis: contains bold, and underline html markup elements\n')
			# print('Open XML Markup Equivalent:')
			# print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:b w:val="1"/><w:u w:val="single"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			# print('\n--\n')
			
	# if chowder.b != None and chowder.font == None and chowder.i != None and chowder.u == None:		#=> Line analysis: contains bold, and italic html markup elements
		# if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content	
			# print('Oringal markup:\n\t' + str(e))
			# print('\tLine analysis: contains bold, and italic html markup elements\n')	
			# print('Open XML Markup Equivalent:')
			# print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:b w:val="1"/><w:i w:val="1"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			# print('\n--\n')
			
	# if chowder.b != None and chowder.font != None and chowder.i == None and chowder.u == None:		#=> Line analysis: contains bold, and font html markup elements
		# if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			# print('Oringal markup:\n\t' + str(e))
			# print('\tLine analysis: contains bold, and font html markup elements\n')
			# print('Open XML Markup Equivalent:')
			# print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:b w:val="1"/><w:sz w:val="' + str(chowder.font['size']) + '"/><w:szCs w:val="' + str(chowder.font['size']) + '"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			# print('\n--\n')	
			
	# if chowder.b != None and chowder.font == None and chowder.i == None and chowder.u == None:		#=> Line analysis: contains only a bold html markup element
		# if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			# print('Oringal markup:\n\t' + str(e))
			# print('\tLine analysis: contains only a bold html markup element\n')
			# print('Open XML Markup Equivalent:')
			# print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:b w:val="1"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			# print('\n--\n')	
      
	# if chowder.b == None and chowder.font != None and chowder.i != None and chowder.u != None:		#=> Line analysis: contains font, italic, and underline html markup elements
		# if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			# print('Oringal markup:\n\t' + str(e))
			# print('\tLine analysis: contains font, italic, and underline html markup elements\n')
			# print('Open XML Markup Equivalent:')
			# print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:i w:val="1"/><w:sz w:val="' + str(chowder.font['size']) + '"/><w:szCs w:val="' + str(chowder.font['size']) + '"/><w:u w:val="single"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			# print('\n--\n')
	
	# if chowder.b == None and chowder.font != None and chowder.i != None and chowder.u == None:		#=> Line analysis: contains font, and italic html markup elements
		# if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content	
			# print('Oringal markup:\n\t' + str(e))
			# print('\tLine analysis: contains font, and italic html markup elements\n')
			# print('Open XML Markup Equivalent:')
			# print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:i w:val="1"/><w:sz w:val="' + str(chowder.font['size']) + '"/><w:szCs w:val="' + str(chowder.font['size']) + '"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			# print('\n--\n')
      			

	# if chowder.b == None and chowder.font != None and chowder.i == None and chowder.u != None:		#=> Line analysis: contains font, and underline html markup elements
		# if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			# print('Oringal markup:\n\t' + str(e))
			# print('\tLine analysis: contains font, and underline html markup elements\n')
			# print('Open XML Markup Equivalent:')
			# print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:sz w:val="' + str(chowder.font['size']) + '"/><w:szCs w:val="' + str(chowder.font['size']) + '"/><w:u w:val="single"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			# print('\n--\n')
      			

	# if chowder.b == None and chowder.font != None and chowder.i == None and chowder.u == None:		#=> Line analysis: contains only a font html markup element
		# if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			# print('Oringal markup:\n\t' + str(e))
			# print('\tLine analysis: contains only a font html markup element\n')
			# print('Open XML Markup Equivalent:')
			# print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:sz w:val="' + str(chowder.font['size']) + '"/><w:szCs w:val="' + str(chowder.font['size']) + '"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			# print('\n--\n')
			
      			
	# if chowder.b == None and chowder.font == None and chowder.i != None and chowder.u != None:		#=> Line analysis: contains italic, and underline html markup elements
		# if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			# print('Oringal markup:\n\t' + str(e))
			# print('\tLine analysis: contains italic, and underline html markup elements\n')	
			# print('Open XML Markup Equivalent:')
			# print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:i w:val="1"/><w:u w:val="single"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			# print('\n--\n')
      			
	# if chowder.b == None and chowder.font == None and chowder.i != None and chowder.u == None:		#=> Line analysis: contains only an italic html markup element
		# if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			# print('Oringal markup:\n\t' + str(e))
			# print('\tLine analysis: contains only an italic html markup element\n')
			# print('Open XML Markup Equivalent:')
			# print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:i w:val="1"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			# print('\n--\n')	
			
	# if chowder.b == None and chowder.font == None and chowder.i == None and chowder.u != None:		#=> Line analysis: contains only an underline html markup element
		# if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			# print('Oringal markup:\n\t' + str(e))
			# print('\tLine analysis: contains only an underline html markup element\n')
			# print('Open XML Markup Equivalent:')
			# print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:u w:val="single"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			# print('\n--\n')
	


docx = Document('test_data\html_to_xml_test.docx')
xml  = docx.get_xml()

#xml = '<w:document xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" xmlns:sl="http://schemas.openxmlformats.org/schemaLibrary/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" xmlns:lc="http://schemas.openxmlformats.org/drawingml/2006/lockedCanvas" xmlns:dgm="http://schemas.openxmlformats.org/drawingml/2006/diagram" xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"> <w:background w:color="FFFFFF"/> <w:body> <w:p w:rsidR="00000000" w:rsidDel="00000000" w:rsidP="00000000" w:rsidRDefault="00000000" w:rsidRPr="00000000"> <w:pPr> <w:pBdr/> <w:contextualSpacing w:val="0"/> <w:rPr/> </w:pPr> <w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"> <w:rPr> <w:rtl w:val="0"/> </w:rPr> <w:t xml:space="preserve">Simple text <font size=12>substitution</font> test for formatting purposes. Simple text <b><i>substitution</i></b> test for formatting purposes. Simple {{ B0C0 }} text <u>substitution</u> test for formatting purposes. Simple text substitution test for <i>formatting purposes</i>. Simple text substitution {{ B0C1 }} test for formatting purposes. Simple text substitution test for formatting purposes. Simple text substitution test for formatting purposes. </w:t> </w:r> <w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"> <w:rPr> <w:i w:val="1"/> <w:u w:val="single"/> <w:rtl w:val="0"/> </w:rPr> <w:t xml:space="preserve">Simple text substitution {{ B0C0 }} test for formatting purposes.</w:t> </w:r> <w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"> <w:rPr> <w:rtl w:val="0"/> </w:rPr> <w:t xml:space="preserve"> Simple text substitution {{ B0C2 }} test for formatting purposes. Simple <b><u>text substitution</u></b> test for formatting purposes. Simple text substitution test for formatting purposes. Simple text <font size="15"><u>substitution</u></font> test for formatting purposes. Simple text substitution test for formatting purposes. <u><i><b>Simple text substitution</b></i></u> test for formatting {{ B0 }} purposes. </w:t> </w:r> </w:p> <w:sectPr> <w:pgSz w:h="15840" w:w="12240"/> <w:pgMar w:bottom="1440" w:top="1440" w:left="1440" w:right="1440" w:header="0"/> <w:pgNumType w:start="1"/> </w:sectPr> </w:body></w:document>'
xml = '<w:document xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" xmlns:sl="http://schemas.openxmlformats.org/schemaLibrary/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" xmlns:lc="http://schemas.openxmlformats.org/drawingml/2006/lockedCanvas" xmlns:dgm="http://schemas.openxmlformats.org/drawingml/2006/diagram" xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"><w:background w:color="FFFFFF"/><w:body><w:p w:rsidR="00000000" w:rsidDel="00000000" w:rsidP="00000000" w:rsidRDefault="00000000" w:rsidRPr="00000000"><w:pPr><w:pBdr/><w:contextualSpacing w:val="0"/><w:rPr/></w:pPr><w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">Simple text substitution test for formatting purposes. <i>Simple text substitution</i> test for formatting purposes. Simple {{ B0C0 }} text <b>substitution</b> test for formatting purposes. Simple text substitution test for formatting purposes. Simple text substitution {{ B0C1 }} test for formatting purposes. Simple text substitution test for formatting purposes. Simple text substitution test for formatting purposes. </w:t></w:r><w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:i w:val="1"/><w:u w:val="single"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">Simple text substitution {{ B0C0 }} test for formatting purposes.</w:t></w:r><w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve"> Simple text substitution {{ B0C2 }} test for formatting purposes. Simple text substitution test for formatting purposes. Simple text substitution test for formatting purposes. Simple text substitution test for formatting purposes. Simple text substitution test for formatting purposes. Simple text substitution test for formatting {{ B0 }} purposes. </w:t></w:r></w:p><w:sectPr><w:pgSz w:h="15840" w:w="12240"/><w:pgMar w:bottom="1440" w:top="1440" w:left="1440" w:right="1440" w:header="0"/><w:pgNumType w:start="1"/></w:sectPr></w:body></w:document>'
gumbo = BeautifulSoup(xml, "lxml")					#=> XML Parser

for item in gumbo.findAll('w:r'): 					#=> find all the word runs
	### print(item.prettify())
	#print('--')
	bisque = BeautifulSoup(str(item), "lxml")	
	rpr = bisque.find('w:rpr')						#=> find the rPr data
	rpr2 = rpr
	rpr = str(rpr).replace('rpr', 'rPr')
	rpr = rpr.replace('<w:rtl w:val="0"></w:rtl>', '<w:rtl w:val="0"/>')
	#print(rpr2.prettify())
	#print('--')

	for text in bisque.findAll('w:t'):
		broth = BeautifulSoup(str(text), 'html.parser')
		pattern_list = []
		list2 = []
		#print('LOOK at ME -> ' + str(text))
		for element in broth.findAll('b'):
			if element.getText() != element.parent.getText():
				pattern_list.append('(' + str(element) + ')')
				
		for element in broth.findAll('font'):
			if element.getText() != element.parent.getText():
				pattern_list.append('(' + str(element) + ')')
				
		for element in broth.findAll('i'):
			if element.getText() != element.parent.getText():
				pattern_list.append('(' + str(element) + ')')
			
		for element in broth.findAll('u'):
			if element.getText() != element.parent.getText():
				pattern_list.append('(' + str(element) + ')')
		
		pattern_str = '|'.join(pattern_list)
		ptrn = re.compile(pattern_str)
		
		if(pattern_str != ''):
			list2 = re.split(ptrn, str(text))
			key_list = re.split(ptrn, str(text))
	
			while None in list2:
				list2.remove(None)
				
			while None in key_list:
				key_list.remove(None)
				
			count = 0
			for i in list2:
				print('Item ' + str(count)+ " : \n\t" + i)
				count += 1			
		
		if len(list2) > 1:
			for index in range(len(list2)):
				if index == 0:
					list2[index] = list2[index] + '</w:t></w:r>'
					print("NOW in INDES")
					print(list2[index])
					print("IN TEXT")
					print(str(text))
					print("\n\n")
				else:
					if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) == 0:
						### print('No html')
						#print(list2[index])
						### print('')
						### list2[index] = '<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000">' + str(rpr) + '<w:t xml:space="preserve">' + list2[index] + '</w:t></w:r>'
						### print(list2[index])
						if index != (len(list2) - 1):
							list2[index] = '<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000">' + str(rpr) + '<w:t xml:space="preserve">' + list2[index] + '</w:t></w:r>'
						else:
							list2[index] = '<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000">' + str(rpr) + '<w:t xml:space="preserve">' + list2[index]						
						
					else:
						### print('FOUND')
						### print(list2[index])
						### print('')
						rPr_temp = ''
						
						#=> B/F/I/U
						if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) != 0:
							### print('B/F/I/U')
							rPr_temp = '<w:b w:val="1"/><w:i w:val="1"/><w:sz w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:szCs w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:u w:val="single"/>'
							### print(rPr_temp)

						# #=> B/F/I
						if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) == 0:
							### print('B/F/I')
							rPr_temp = '<w:b w:val="1"/><w:i w:val="1"/><w:sz w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:szCs w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/>'
							### print(rPr_temp)

							
						#=> B/F/U
						if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) != 0:					
							### print('B/F/U')
							rPr_temp = '<w:b w:val="1"/><w:sz w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:szCs w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:u w:val="single"/>'
							### print(rPr_temp)
							
						#=> B/I/U
						if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) != 0:					
							### print('B/I/U')
							rPr_temp = '<w:b w:val="1"/><w:i w:val="1"/><w:u w:val="single"/>'
							### print(rPr_temp)
							
						#=> B/U
						if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) != 0:
							### print('B/U')
							rPr_temp = '<w:b w:val="1"/><w:u w:val="single"/>'
							### print(rPr_temp)
							
						#=> B/I
						if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) == 0:
							### print('B/I')
							rPr_temp = '<w:b w:val="1"/><w:i w:val="1"/>'
							### print(rPr_temp)
							
						#=> B/F
						if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) == 0:
							### print('B/F')
							rPr_temp = '<w:b w:val="1"/><w:sz w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:szCs w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/>'
							### print(rPr_temp)
							
							
						#=> B
						if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) == 0:
							### print('B')
							rPr_temp = '<w:b w:val="1"/>'
							### print(rPr_temp)
							
						#=> F/I/U
						if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) != 0:
							### print('F/I/U')
							rPr_temp = '<w:i w:val="1"/><w:sz w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:szCs w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:u w:val="single"/>'
							### print(rPr_temp)
							
							
						#=> F/I
						if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) == 0:
							### print('F/I')
							rPr_temp = '<w:i w:val="1"/><w:sz w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:szCs w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/>'
							### print(rPr_temp)
							
						#=> F/U
						if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) != 0:
							### print('F/U')
							rPr_temp = '<w:sz w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:szCs w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:u w:val="single"/>'
							### print(rPr_temp)
							
						#=> F
						if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) == 0:
							### print('F')
							rPr_temp = '<w:sz w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:szCs w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/>'
							### print(rPr_temp)
							
						#=> I/U
						if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) != 0:
							### print('I/U')
							rPr_temp = '<w:i w:val="1"/><w:u w:val="single"/>'
							### print(rPr_temp)
							
						# #=> I
						if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) == 0:
							### print('I')
							rPr_temp = '<w:i w:val="1"/>'
							
							### print(rPr_temp)
							
						#=> U
						if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) != 0:
							### print('U')
							rPr_temp = '<w:u w:val="single"/>'
							### print(rPr_temp)
						
						list2[index] = '<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr>' + str(rPr_temp) + '<w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + BeautifulSoup(str(list2[index]), 'html.parser').getText() + '</w:t></w:r>'
						### print(list2[index])

		#output = ' '.join(list2)
		#output = output.replace('> <', '><')
		for x in list2:
			x = x.replace('> <', '><')
		print(list2)
		# print('------OUTPUT-------------')	
		# print(str(text))
		# print('-------------------------')	
		#xml = xml.replace(str(text), output)
		#print('---')
		#print(xml)
		#print('--')
#print(' ')		
#print(xml)
#docx.save_xml(docx.get_xml_tree(xml.encode('utf-8')), 'xml_out.docx')

		
# for item in chicken.findAll('w:t'):
	# count = 0	
	# for item in key_list:
		# xml = xml.replace(str(item), str(list2[count]))
		# count += 1
	print(len(list2))
	print(len(key_list))
	for index in range(len(list2)):

		xml = xml.replace(str(key_list[index]), str(list2[index]))
		
	# if len(re.findall(r'{{ B0C0 }}', item.getText(), re.IGNORECASE)) != 0:
		# rpr = item.parent.find('w:rpr')
		# rpr = str(rpr).replace('rpr', 'rPr')
print(xml)
#xml = '<w:document xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" xmlns:sl="http://schemas.openxmlformats.org/schemaLibrary/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" xmlns:lc="http://schemas.openxmlformats.org/drawingml/2006/lockedCanvas" xmlns:dgm="http://schemas.openxmlformats.org/drawingml/2006/diagram" xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"> 	<w:background w:color="FFFFFF"/> 	<w:body> 	<w:p w:rsidR="00000000" w:rsidDel="00000000" w:rsidP="00000000" w:rsidRDefault="00000000" w:rsidRPr="00000000"> 	<w:pPr> 		<w:pBdr/> 		<w:contextualSpacing w:val="0"/> 		<w:rPr/> 	</w:pPr> 	<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"> 		<w:rPr> 			<w:rtl w:val="0"/> 		</w:rPr> 	<w:t xml:space="preserve">Simple text substitution test for formatting purposes.Simple text substitution test for formatting purposes. Simple {{ B0C0 }} text </w:t> 	</w:r> 	 	<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"> 		<w:rPr> 			<w:b w:val="1"/> 			<w:rtl w:val="0"/> 		</w:rPr> 	<w:t xml:space="preserve">substitution</w:t> 	</w:r>  	<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"> 		<w:rPr> 			<w:rtl w:val="0"/> 		</w:rPr> 	<w:t xml:space="preserve"> test for formatting purposes. Simple text substitution test for formatting purposes. Simple text substitution {{ B0C1 }} test for formatting purposes. Simple text substitution test for formatting purposes. Simple text substitution test for formatting purposes. </w:t>  	</w:r> 	 	<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"> 	<w:rPr> 		<w:i w:val="1"/> 		<w:u w:val="single"/> 		<w:rtl w:val="0"/> 	</w:rPr> 	<w:t xml:space="preserve">Simple text substitution {{ B0C0 }} test for formatting purposes.</w:t> 	</w:r> 	 	 	<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"> 	<w:rPr> 		<w:rtl w:val="0"/> 	</w:rPr> 	<w:t xml:space="preserve"> Simple text substitution {{ B0C2 }} test for formatting purposes. Simple text substitution test for formatting purposes. Simple text substitution test for formatting purposes. Simple text substitution test for formatting purposes. Simple text substitution test for formatting purposes. Simple text substitution test for formatting {{ B0 }} purposes. </w:t> 	</w:r> 	 	</w:p> 	 	<w:sectPr> 		<w:pgSz w:h="15840" w:w="12240"/> 		<w:pgMar w:bottom="1440" w:top="1440" w:left="1440" w:right="1440" w:header="0"/> 		<w:pgNumType w:start="1"/> 	</w:sectPr> 	</w:body> 	</w:document>'
#text = etree.tostring(docx.get_xml_tree(xml.encode('utf-8')), pretty_print = True)
docx.save_xml(docx.get_xml_tree(xml.encode('utf-8')), 'xml_out.docx')	







	
			
	
# -------------------------------------------------------------------------------------------------------------------------