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
			
			
	# html_to_xml: todo
	#
	# @pram xml
	#
	def html_to_xml(self, xml):
		xml = xml.replace(b'&quot;', b'"')										#=> markup clean up required													            
		xml = xml.replace(b'<br />', b'</w:t><w:br/><w:t xml:space="preserve">')	#=> line break injections													
		gumbo = BeautifulSoup(xml, "lxml")										#=> XML Parser

		for item in gumbo.findAll('w:r'): 					#=> find all the word runs
			bisque = BeautifulSoup(str(item), "lxml")	
			rpr = bisque.find('w:rpr')						#=> find the rPr data
			rpr2 = rpr
			
			# correct auto formatting
			rpr = str(rpr).replace('rpr', 'rPr')
			rpr = rpr.replace('<w:rtl w:val="0"></w:rtl>', '<w:rtl w:val="0"/>')
			
			
			for text in bisque.findAll('w:t'):				#=> look in each text run
				broth = BeautifulSoup(str(text), 'html.parser')
				pattern_list = []
				list2 = []
				key_list = []
				# print('---------------------------------------------------')
				# print(text)
				
				
				
				if not (len(broth.findAll('b')) == 0 and  len(broth.findAll('font')) == 0 and  len(broth.findAll('i')) == 0 and  len(broth.findAll('u')) == 0):
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
							
					
					if len(list2) > 1:
						for index in range(len(list2)):
							if index == 0:
								list2[index] = list2[index] + '</w:t></w:r>'
								
							else:
								if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) == 0:
									if index != (len(list2) - 1):
										list2[index] = '<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000">' + str(rpr) + '<w:t xml:space="preserve">' + list2[index] + '</w:t></w:r>'
										
									else:
										list2[index] = '<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000">' + str(rpr) + '<w:t xml:space="preserve">' + list2[index]						
									
								else:
									rPr_temp = ''
									
									#=> B/F/I/U
									if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) != 0:
										rPr_temp = '<w:b w:val="1"/><w:i w:val="1"/><w:sz w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:szCs w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:u w:val="single"/>'

									# #=> B/F/I
									if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) == 0:
										rPr_temp = '<w:b w:val="1"/><w:i w:val="1"/><w:sz w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:szCs w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/>'

									#=> B/F/U
									if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) != 0:					
										rPr_temp = '<w:b w:val="1"/><w:sz w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:szCs w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:u w:val="single"/>'
										
									#=> B/I/U
									if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) != 0:					
										rPr_temp = '<w:b w:val="1"/><w:i w:val="1"/><w:u w:val="single"/>'
										
									#=> B/U
									if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) != 0:
										rPr_temp = '<w:b w:val="1"/><w:u w:val="single"/>'
										
									#=> B/I
									if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) == 0:
										rPr_temp = '<w:b w:val="1"/><w:i w:val="1"/>'
										
									#=> B/F
									if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) == 0:
										rPr_temp = '<w:b w:val="1"/><w:sz w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:szCs w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/>'
											
									#=> B
									if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) == 0:
										rPr_temp = '<w:b w:val="1"/>'
										
									#=> F/I/U
									if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) != 0:
										rPr_temp = '<w:i w:val="1"/><w:sz w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:szCs w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:u w:val="single"/>'
										
									#=> F/I
									if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) == 0:
										rPr_temp = '<w:i w:val="1"/><w:sz w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:szCs w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/>'
										
									#=> F/U
									if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) != 0:
										rPr_temp = '<w:sz w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:szCs w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:u w:val="single"/>'
										
									#=> F
									if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) == 0:
										rPr_temp = '<w:sz w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/><w:szCs w:val="' + str(BeautifulSoup(str(list2[index]), 'html.parser').font['size']) + '"/>'
										
									#=> I/U
									if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) != 0:
										rPr_temp = '<w:i w:val="1"/><w:u w:val="single"/>'
										
									# #=> I
									if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) != 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) == 0:
										rPr_temp = '<w:i w:val="1"/>'
										
									#=> U
									if len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('b')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('font')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('i')) == 0 and len(BeautifulSoup(str(list2[index]), 'html.parser').findAll('u')) != 0:
										rPr_temp = '<w:u w:val="single"/>'
									
									list2[index] = '<w:r w:rsidDel="00000000" w:rsidR="00000000" w:rsidRPr="00000000"><w:rPr>' + str(rPr_temp) + '<w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">' + BeautifulSoup(str(list2[index]), 'html.parser').getText() + '</w:t></w:r>'

					for x in list2:
						x = x.replace('> <', '><')
			
				for index in range(len(list2)):
					if str(key_list[index]) != '</w:t>':
						xml = xml.replace(bytes(key_list[index], 'utf8'), bytes(list2[index], 'utf8'))
						
					# print('------------ OUTPUT Chcker -------------')	
					# print(key_list[index])
					# print(list2[index])
					# print('-----------------------------------------')
					
					xml = xml.replace(b'</w:t></w:r></w:t></w:r>', b'</w:t></w:r>')
					
		return xml		

		
# docx = Document('test_data\example2.docx')
# xml  = docx.get_xml()
# xml = xml.replace('College', '<font size="45">professor</font>')
# xml = xml.replace('believable.', '<b>what up</b>')
# xml = xml.replace('packages', '<i><u>Boya</u></i>')
# xml = xml.replace('popularised', '<font size="45"><u><b>YES YES YES</b></u></font>')
# xml = xml.replace('readable', '<br />')
# xml = xml.replace('Latin', '<br />')
# xml = xml.replace('\\bibliography{second_bib}', '<b><font size="23">THE real test</font></b>')		
# xml = xml.replace('\\bibliography{third_bib}', '<b><font size="23"><i>Another Test</i></font></b>')
# xml = xml.replace('consectetur,', '<br /><br />')

# xml = docx.html_to_xml(xml)
# docx.save_xml(docx.get_xml_tree(xml.encode('utf-8')), 'xml_out.docx')	