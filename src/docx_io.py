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

sampleText = 'This is a <b></b>test string to <i>test</i> simple HTML <u>markup</u> elements <b><i>converson</i></b> to <u><b><font size=18>Open XML markup</font></b></u> for word <font size="15">document</font> formatting. <font size=6><b><u><i>For nested markup they</i></u></b></font> can appear in any order, font size value can be quote or not quoted'

soup = BeautifulSoup(sampleText, 'html.parser')
print('\n-------------------- Original text feed --------------------')
print('\n' + sampleText + '\n')
print('------------------------------------------------------------\n')
	
for e in soup.findAll():
	chowder = BeautifulSoup(str(e), 'html.parser')
	
	if chowder.b != None and chowder.font != None and chowder.i != None and chowder.u != None:		#=> contains bold, font, italic, and underline html markup elements
		if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			print('Oringal markup:\n\t' + str(e))
			print('\tLine analysis: contains bold, font, italic, and underline html markup elements\n')
			print('Open XML Markup Equivalent:')
			print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:b w:val="1"/><w:i w:val="1"/><w:sz w:val="' + str(chowder.font['size']) + '"/><w:szCs w:val="' + str(chowder.font['size']) + '"/><w:u w:val="single"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			print('\n--\n')
		
	if chowder.b != None and chowder.font != None and chowder.i != None and chowder.u == None:		#=> Line analysis: contains bold, font, and italic html markup elements
		if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			print('Oringal markup:\n\t' + str(e))
			print('\tLine analysis: contains bold, font, and italic html markup elements\n')
			print('Open XML Markup Equivalent:')
			print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:b w:val="1"/><w:i w:val="1"/><w:sz w:val="' + str(chowder.font['size']) + '"/><w:szCs w:val="' + str(chowder.font['size']) + '"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			print('\n--\n')

	if chowder.b != None and chowder.font != None and chowder.i == None and chowder.u != None:		#=> Line analysis: contains bold, font, and underline html markup elements
		if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			print('Oringal markup:\n\t' + str(e))
			print('\tLine analysis: contains bold, font, and underline html markup elements\n')
			print('Open XML Markup Equivalent:')
			print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:b w:val="1"/><w:sz w:val="' + str(chowder.font['size']) + '"/><w:szCs w:val="' + str(chowder.font['size']) + '"/><w:u w:val="single"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			print('\n--\n')		
			
	if chowder.b != None and chowder.font == None and chowder.i == None and chowder.u != None:		#=> Line analysis: contains bold, and underline html markup elements
		if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			print('Oringal markup:\n\t' + str(e))
			print('\tLine analysis: contains bold, and underline html markup elements\n')
			print('Open XML Markup Equivalent:')
			print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:b w:val="1"/><w:u w:val="single"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			print('\n--\n')
			
	if chowder.b != None and chowder.font == None and chowder.i != None and chowder.u == None:		#=> Line analysis: contains bold, and italic html markup elements
		if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content	
			print('Oringal markup:\n\t' + str(e))
			print('\tLine analysis: contains bold, and italic html markup elements\n')	
			print('Open XML Markup Equivalent:')
			print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:b w:val="1"/><w:i w:val="1"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			print('\n--\n')
			
	if chowder.b != None and chowder.font != None and chowder.i == None and chowder.u == None:		#=> Line analysis: contains bold, and font html markup elements
		if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			print('Oringal markup:\n\t' + str(e))
			print('\tLine analysis: contains bold, and font html markup elements\n')
			print('Open XML Markup Equivalent:')
			print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:b w:val="1"/><w:sz w:val="' + str(chowder.font['size']) + '"/><w:szCs w:val="' + str(chowder.font['size']) + '"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			print('\n--\n')	
			
	if chowder.b != None and chowder.font == None and chowder.i == None and chowder.u == None:		#=> Line analysis: contains only a bold html markup element
		if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			print('Oringal markup:\n\t' + str(e))
			print('\tLine analysis: contains only a bold html markup element\n')
			print('Open XML Markup Equivalent:')
			print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:b w:val="1"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			print('\n--\n')	
      
	if chowder.b == None and chowder.font != None and chowder.i != None and chowder.u != None:		#=> Line analysis: contains font, italic, and underline html markup elements
		if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			print('Oringal markup:\n\t' + str(e))
			print('\tLine analysis: contains font, italic, and underline html markup elements\n')
			print('Open XML Markup Equivalent:')
			print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:i w:val="1"/><w:sz w:val="' + str(chowder.font['size']) + '"/><w:szCs w:val="' + str(chowder.font['size']) + '"/><w:u w:val="single"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			print('\n--\n')
	
	if chowder.b == None and chowder.font != None and chowder.i != None and chowder.u == None:		#=> Line analysis: contains font, and italic html markup elements
		if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content	
			print('Oringal markup:\n\t' + str(e))
			print('\tLine analysis: contains font, and italic html markup elements\n')
			print('Open XML Markup Equivalent:')
			print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:i w:val="1"/><w:sz w:val="' + str(chowder.font['size']) + '"/><w:szCs w:val="' + str(chowder.font['size']) + '"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			print('\n--\n')
      			

	if chowder.b == None and chowder.font != None and chowder.i == None and chowder.u != None:		#=> Line analysis: contains font, and underline html markup elements
		if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			print('Oringal markup:\n\t' + str(e))
			print('\tLine analysis: contains font, and underline html markup elements\n')
			print('Open XML Markup Equivalent:')
			print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:sz w:val="' + str(chowder.font['size']) + '"/><w:szCs w:val="' + str(chowder.font['size']) + '"/><w:u w:val="single"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			print('\n--\n')
      			

	if chowder.b == None and chowder.font != None and chowder.i == None and chowder.u == None:		#=> Line analysis: contains only a font html markup element
		if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			print('Oringal markup:\n\t' + str(e))
			print('\tLine analysis: contains only a font html markup element\n')
			print('Open XML Markup Equivalent:')
			print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:sz w:val="' + str(chowder.font['size']) + '"/><w:szCs w:val="' + str(chowder.font['size']) + '"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			print('\n--\n')
			
      			
	if chowder.b == None and chowder.font == None and chowder.i != None and chowder.u != None:		#=> Line analysis: contains italic, and underline html markup elements
		if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			print('Oringal markup:\n\t' + str(e))
			print('\tLine analysis: contains italic, and underline html markup elements\n')	
			print('Open XML Markup Equivalent:')
			print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:i w:val="1"/><w:u w:val="single"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			print('\n--\n')
      			
	if chowder.b == None and chowder.font == None and chowder.i != None and chowder.u == None:		#=> Line analysis: contains only an italic html markup element
		if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			print('Oringal markup:\n\t' + str(e))
			print('\tLine analysis: contains only an italic html markup element\n')
			print('Open XML Markup Equivalent:')
			print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:i w:val="1"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			print('\n--\n')	
			
	if chowder.b == None and chowder.font == None and chowder.i == None and chowder.u != None:		#=> Line analysis: contains only an underline html markup element
		if e.getText() != e.parent.getText():														#=> check to see if this element is a descendant of a parent with the same content
			print('Oringal markup:\n\t' + str(e))
			print('\tLine analysis: contains only an underline html markup element\n')
			print('Open XML Markup Equivalent:')
			print('<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:u w:val="single"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + e.getText() + '</w:t></w:r>')
			print('\n--\n')
			
			
# docx = Document('test_data\html_to_xml_test.docx')
# xml  = docx.get_xml()
# type(xml)
# out = xml.replace('Simple', '<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr><w:u w:val="single"/><w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">formatted</w:t></w:r>')
# print(out)
# docx.save_xml(docx.get_xml_tree(out.encode('utf-8')), 'xml_out.docx')			
# -------------------------------------------------------------------------------------------------------------------------