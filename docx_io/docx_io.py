import sys, os, shutil, re, zipfile, tempfile, sys
from lxml import etree


class Document:
	'''
	__init__ is the the constructor for the document class that stores a qualified path to a target Open file.

	@pram filename is the directory\name of the target Open XML document file.
	'''
	def __init__(self, filename):
		self.filename = filename
		
		try:
			self.zipfile = zipfile.ZipFile(filename)
			
		except (OSError, IOError) as e:
			print "Unable to read file:", self.filename

	
	'''	
	get_xml extracts the Open XML contents from a document zip compression

	@returns string containing the Open XML.
	'''
	def get_xml(self):
		try:
			with open(self.filename, 'rb') as fh:
				unzipped = zipfile.ZipFile(fh)
				xml_content = unzipped.read('word/document.xml')	#<= Retrieve Open XML
				return xml_content

		except (OSError, IOError) as e:
			print "Unable to read file:", self.filename

			
	'''
	save_xml copies the contents from the orginal Open XML document compression replacing all the content inside the 
	document.xml with the xml_content string and saves it into a new Open XML document compression by the specified name
	indicated by output_filename.
	
	@pram xml_content is a string containing some data that will be written into the document.xml.
	@pram output_filename is a string that is used to name the new Open XML document.
	@returns true indicating successful document creation; false upon failure to create document
	'''
	def save_xml(self, xml_content, output_filename):
		dir = tempfile.mkdtemp()

		self.zipfile.extractall(dir)
		
		try:
			with open(os.path.join(dir,'word/document.xml'), 'w') as f:
				xml_str = etree.tostring(xml_content, pretty_print=True)
				f.write(xml_str)
				
			filenames = self.zipfile.namelist()	#<= Get a list of all the files in the original docx zipfile

			# Create the new zip file and add all the files into the archive
			zip_copy_filename = output_filename
			with zipfile.ZipFile(zip_copy_filename, "w", zipfile.ZIP_DEFLATED) as docx:
				for filename in filenames:
					docx.write(os.path.join(dir, filename), filename)
					
			shutil.rmtree(dir)	#<= Clean up the dir
			return True
			
		except (OSError, IOError) as e:
			print "Unable to save file:", output_filename
			return False
			
			
	'''
	get_xml_tree create an element or tree of elements from a string containing XML.
	
	@returns a new element instance represented by the XML.
	'''
	def get_xml_tree(self, xml_string):
	   return etree.fromstring(xml_string)
   
   
	'''
	get_latex find all the regular expression pattern(s) in the xml content and puts them intoa
	a list structure.
	
	@pram xml_content is a string containing xml data
	@returns a list of matching regular expression elements \cite{...} and \bib{...}
	'''
	def get_latex(self, xml_content):
		pattern = re.compile(r'\\cite\s*{[^}]*}|\\bibliography\s*{[^}]*}')	#<= Define regular expression
		list = pattern.findall(xml_content, re.IGNORECASE)
		return list
		
		
	'''
	remove_markup removes any embedded Open XML markup inside a latex element as a result of formatting
	that occurred during document design
	
	@pram list is a python list of string elements representing latex markup
	@return list of string entries without Open XML mkarkup elements
	'''
	def remove_markup(self, list):
		pattern = re.compile(r'<w:[^>]*>|</w:[^>]*>|')
		
		# Iterate through the list removing any Open XML markup embedded inside latex elements
		for i in range(0, len(list)):
			list[i] = pattern.sub('', list[i])
		
		return list

