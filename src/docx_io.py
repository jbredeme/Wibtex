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
	# __init__ is the the constructor for the document class that stores a qualified path to a target Open file.
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
	# @return string containing the Open XML.
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
	# @return true indicating successful document creation; false upon failure to create document
	#
	def save_xml(self, xml_content, output_filename):
		dir = tempfile.mkdtemp()

		self.zipfile.extractall(dir)
		
		try:
			with open(os.path.join(dir,'word', 'document.xml'), 'w') as f:
				xml_str = etree.tostring(xml_content, pretty_print = True).decode("utf-8")
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
	# @return a new element instance represented by the XML.
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
	# @return an xml string that is been processed by the templating engine
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
	# @return a string containing all the contents inside curly braces, None if no value was extracted.
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
	# @return a tuple; first value is a python dictionary of the latex markup and jinja key variables generated for bibliographies and citations; second value 
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
			print("------------------------------------------------------------\n")

			
	# generates a string by taking the first occurance of a html element or a nested set
	# of elements and joining them together. an example string might be something like
	# 'simple <b>example</b> string <i><front size="16">nothing interesting</font></i> at all'
	# would return '(<b>example</b>)|(<i><front size="16">nothing interesting</font></i>)'. this
	# string is used as a regex pattern to split the string into a list.
	#
	# @pram html string of text containing html markup
	# @return a string that can be re.compiled as a regex expression pattern
	#
	def split_html(self, html):
		pattern = []
		
		if not html:										#=> guard against empty strings
			return html
		
		else: 
			broth = BeautifulSoup(html, 'html.parser')		#=> parsing object
			for token in broth.findAll(recursive = False):	
				pattern.append('(' + str(token) + ')')
				
			pattern = '|'.join(pattern)						#=> join list into a string
			
			return pattern
		
		
	# this is a recursive parse tree function that generates wordml data from html data. this
	# function accepts nested html tags independant of order.
	#
	# @pram text is a string containing plain text, html markup, or a combination of both.
	# @return a list of wordml data.
	#		
	def recursive_builder(self, text):
		broth = BeautifulSoup(text, 'html.parser')
		if len(broth.findAll(recursive = False)) == 0:		#=> base case: text has no html elements
			output = ['<w:r>', '<w:rPr>', '</w:rPr>', '<w:t>', text, '</w:t>', '</w:r>']
			return output
			
		else:
			if broth.find().name == 'b':					#=> recursive step text with html elements
				sub = broth.b.findChildren(recursive = False)
				if len(sub) == 0:
					sub = broth.b.getText()				
				out2 = self.recursive_builder(str(sub))
				out2.insert(2, '<w:b/>')
				
			if broth.find().name == 'font':
				sub = broth.font.findChildren(recursive = False)
				if len(sub) == 0:
					sub = broth.font.getText()
				out2 = self.recursive_builder(str(sub))
				
				if broth.font.has_attr('size'): 
					out2.insert(2, '<w:sz w:val="' + broth.font['size'] +'"/>')
					out2.insert(2, '<w:szCs w:val="' + broth.font['size'] + '"/>')
					
				if broth.font.has_attr('color'):
					hex_color = str(broth.font['color'])
					hex_color = hex_color.replace('#', '')
					out2.insert(2, '<w:color w:val="' + hex_color + '" />')

			if broth.find().name == 'i':
				sub = broth.i.findChildren(recursive = False)
				if len(sub) == 0:
					sub = broth.i.getText()				
				out2 = self.recursive_builder(str(sub))
				out2.insert(2, '<w:i/>')
				
			if broth.find().name == 'u':
				sub = broth.u.findChildren(recursive = False)
				if len(sub) == 0:
					sub = broth.u.getText()				
				out2 = self.recursive_builder(str(sub))
				out2.insert(2, '<w:u w:val="single"/>')	
			
			return out2
			
			
	# splits a string recursively into a list of plain text and html markup. this function is
	# used to mamange nesting of tags inside a string of text with leading and trailing text.
	# i.e. 'some text <b> more text <i><u> even more text </u></i> and more </b> text'
	#
	# @pram 
	# @return
	#		
	def recursive_list_spliter(self, html):
		# base case: text has no html markup
		if len(broth.findAll(recursive = False)) == 0:
			return html
			
		else:
		# recursive step
			str_pattern = docx.split_html(html)
			pattern = re.compile(str_pattern)
		
			if str_pattern != '':
				list = re.split(pattern, html)
			
			for x in range(len(list)):
				self.recursive_list(list[x])
				
		return html
				
				
	# looks through the Open XML document for text runs. analyzes the text runs for embedded html
	# markup and calls a parse tree function to convert html to wordml. after wordml has been assembled
	# and is well formed, the newly generated content replaces the old data.
	#
	# @pram xml is the loaded xml data string from the docx file.
	# @return modified xml string containing the new markup.
	#			
	def html_to_wordlm(self, xml):
		# Expression patterns
		wr = re.compile(r'(<w:r\b[^>]*>(.*?)</w:r>)')
		rPr = re.compile(r'(<w:rPr\b[^>]*>(.*?)</w:rPr>)')
		wt = re.compile(r'<w:t\b[^>]*>(.*?)</w:t>')
		xml = xml.replace('<br />', 'w:br')		#=> encode break tags
		text_run = []
		accum = []
		meta_data = []
		
		# Find all the word runs in the document and put them into a list
		for element in wr.findall(xml, re.IGNORECASE):
			xml_markup = element[0]
			
			# For each word run check if there is existing rPr meta data
			if rPr.search(xml_markup) != None:
				meta_data.append(rPr.search(xml_markup).group(2))
				
			else:
				meta_data = []
				
			# Find all word text run using beautifulsoup
			for run in BeautifulSoup(xml_markup, 'lxml').findAll('w:t'):
				text_run.append(re.sub(r'<w:[^>]*>|</w:[^>]*>|', '', str(run)))	#=> remove leading OpenXML elements
				
				# Examine each text run found; word text runs are stored in a list
				for x in range(len(text_run)):
					str_pattern = self.split_html(text_run[x])
					pattern = re.compile(str_pattern)
					
					if str_pattern != '':
						list = re.split(pattern, text_run[x])
						
						while None in list:
							list.remove(None)
						
						for item in list:
							out = self.recursive_builder(item)
							
							if len(meta_data) != 0:			#=> meta data inheritance				
								out.insert(2, meta_data[0])
							
							if out[2] == '</w:rPr>':		#=> remove rPr meta data tags if no meta data
								out.remove('<w:rPr>')
								out.remove('</w:rPr>')
							
							accum = accum + out
							
					else:
						out = self.recursive_builder(text_run[x])
						if len(meta_data) != 0:				#=> meta data inheritance
							out.insert(2, meta_data[0])
							
						if out[2] == '</w:rPr>':			#=> remove rPr meta data tags if no meta data
							out.remove('<w:rPr>')
							out.remove('</w:rPr>')
							
						accum = accum + out	
						
					xml = xml.replace(xml_markup, ''.join(accum))
	
				accum = []		
				text_run = []
				
		xml = xml.replace('w:br', '</w:t><w:br/><w:t>')	#=> decode break tags
		
		return xml
