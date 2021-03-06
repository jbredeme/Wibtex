# WibTeX Reference Management System (WRMS) ![Jarid_Bredemeier](https://img.shields.io/badge/build-passing-green.svg?style=flat-plastic)
WibTeX Reference Management System simplifies the process of preparing documents for cross-discipline research publications by eliminating the need to reconstruct bibliographic information produced in BibTeX to a format suitable for Microsoft Word. WibTeX allows the user to construct reference pages and in-text citations sourced from BibTeX bibliographic information from within a Microsoft Word Document, using a LaTeX workflow.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Microsoft Office Version Compatibility
* Microsoft Office 2010/2013/2016

### Dependencies
What you need to install the software and how to install them
* [Jinja2](http://jinja.pocoo.org/docs/2.9/) - Templating engine.
* [Bibtexparser 0.6.2](https://pypi.python.org/pypi/bibtexparser) - Bibtex database parsing package.
* [lxml 3.7.2](http://lxml.de/) - Toolkit for processing XML and HTML in the Python language.
* [Beautiful Soup 4.4.0](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - library for pulling data out of HTML and XML files.

### Installation
A step by step series of examples that tell you how to get a development env running

```
python setup.py install
```

## Usage
Example of how to use the program
```
python script.py input_doc.docx file.bib style output_doc.docx

OR

python wibtex_gui
```

### Coding style(s) and custom template(s)
Templates for reference styles follow the JSON format depicted below. All
templates must contain an 'order', 'in_text_style', 'title', and 'default_style'
fields in order to be considered valid.
```
{
    "CCSC": {
        "order": {
            "method": "alpha",
            "sortby": "author"
        },
        "in_text_style": {
            "index" : "num",
            "template": "{{num|wrap(']') if num else ''}}"
        },
        "title": {
            "key" : "REFERENCES",
            "template": "{{REFERENCES|wrap_html('b')|font('28', '#4286F4')}}"
        },
        "default_style": "<br />{{num|wrap(']')|add_chars(' ') if num else ''}}{{author|authors_ccsc() if author else '' }}{% if title is defined and author is defined %}{{title|add_chars('.')|add_to_front(', ')}}{% elif title is defined %}{{title|add_chars('.')}}{% else %}{{'.'}}{% endif %}",
        "extended_styles": {
            "journal": {
                "supported": ["journal", "article", "mastersthesis", "incollection"],
                "preferred": ["journal", "article", "mastersthesis", "incollection", "conference"],
                "template": "<br />{{num|wrap(']')|add_chars(' ') if num else ''}}{{author|authors_ccsc() if author else '' }}{{title|add_chars(', ') if title else '' }}{{journal|wrap_html('i')|add_chars(', ') if journal else ''}}{{volume|add_chars(', ') if volume else '' }}{{issue|wrap(')')|add_chars(', ') if issue else ''}}{{pages if pages else ''}}{% if pages is defined and year is defined %}{{year|add_chars('.')|add_to_front(', ')}}{% elif year is defined %}{{year|add_chars('.')}}{% else %}{{'.'}}{% endif %}"
            },
            "book": {
                "supported": ["book", "booklet", "conference"],
                "preferred": ["book"],
                "template": "<br />{{num|wrap(']')|add_chars(' ') if num else ''}}{{author|authors_ccsc() if author else '' }}{{title|wrap_html('i')|add_chars(', ') if title else '' }}{{city|add_chars(': ') if city else ''}}{{publisher if publisher else '' }}{% if publisher is defined and year is defined %}{{year|add_chars('.')|add_to_front(', ')}}{% elif year is defined %}{{year|add_chars('.')}}{% else %}{{'.'}}{% endif %}"
            }, ...
    }, ...
}
```

## Built With
* [Python 3.6.x](https://www.python.org/) - Implementation language.

## Authors
* **Jarid Bredemeier** - *Document IO Module*
* **Charles Duso** - *Templating Module*
* **Hayden Aupperle** - *User Interface*

See also the list of [contributors](https://github.com/jbredeme/Wibtex/graphs/contributors) who participated in this project.

## License
Copyright 2017 Jarid Bredemeier, Charles Duso, Hayden Aupperle

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


