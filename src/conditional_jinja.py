import re
import jinja2
from jinja2 import Template, Environment, BaseLoader
from datetime import datetime

def datetimeformat(value, format):
    return datetime.strptime(value, format).date()

def wrap_html(value, wrapper):
    return "<" + wrapper + ">" + value + "</" + wrapper + ">"

def add_chars(value, char):
    return value + char

def wrap(value, char):
    if char is ')' or char is '(':
        return '(' + value + ')'
    elif char is ']' or char is '[':
        return '[' + value + ']'
    return char + value + char

def add_to_front(value, char):
    return char + value

def authors_ccsc(value):
    if isinstance(value, list):
        if len(value) <= 1:
            return value[0] + ', '
        else:
            string = ""
            for item in value:
                string += item + ", "
            return string
    elif isinstance(value, str):
        return value + ', '
    else:
        return ''

def authors_acm(value):
    f_half = ""
    s_half = ""

    if isinstance(value, list):

        if len(value) <= 1:
            f_half = re.findall('\w+,\s+', value[0])
            s_half = re.findall('\s(\w)', value[0])
            name   = re.findall('\w+', value[0])

            if not f_half:
                return name[0] + ' '
            elif not s_half:
                return f_half[0].split(',')[0] + ' '
            else:
                out = f_half[0]
                for item in s_half:
                    out += item + '.'
                return out + ' '

        elif len(value) == 2:
            first = ""
            second = ""

            f_half = re.findall('\w+,\s+', value[0])
            s_half = re.findall('\s(\w)', value[0])
            name   = re.findall('\w+', value[0])

            if not f_half:
                first = name[0]
            elif not s_half:
                first =  f_half[0].split(',')[0]
            else:
                first = f_half[0]
                for item in s_half:
                    first += item + '.'

            f_half = re.findall('\w+,\s+', value[1])
            s_half = re.findall('\s(\w)', value[1])
            name   = re.findall('\w+', value[1])

            if not f_half:
                second = name[0]
            elif not s_half:
                second =  f_half[0].split(',')[0]
            else:
                second = f_half[0]
                for item in s_half:
                    second += item + '.'
            
            return first + ' and ' + second + ' '

        else:

            out = ""
            temp = ""

            for index in range(0, len(value)):

                f_half = re.findall('\w+,\s+', value[index])
                s_half = re.findall('\s(\w)', value[index])
                name   = re.findall('\w+', value[index])

                if index == len(value) - 2:
                    if not f_half:
                        temp = name[0] = 'and '
                    elif not s_half:
                        temp = f_half[0].split(',')[0] + 'and '
                    else:
                        temp = f_half[0]
                        for item in s_half:
                            temp += item + '.'
                        temp += ' and '
                    out += temp

                elif index == len(value) - 1:
                    if not f_half:
                        temp = name[0]
                    elif not s_half:
                        temp = f_half[0].split(',')[0]
                    else:
                        temp = f_half[0]
                        for item in s_half:
                            temp += item + '.'
                    out += temp + ' '

                else:                    
                    if not f_half:
                        temp = name[0]
                    elif not s_half:
                        temp = f_half[0].split(',')[0]
                    else:
                        temp = f_half[0]
                        for item in s_half:
                            temp += item + '.'
                    out += temp + ', '

            return out

    elif isinstance(value, str):
        return value + ', '

    else:
        return ''

#\w+,\s+\w? <=^|\s\w

environment = Environment(loader=BaseLoader)
environment.filters['datetimeformat'] = datetimeformat
environment.filters['wrap_html'] = wrap_html
environment.filters['add_chars'] = add_chars
environment.filters['wrap'] = wrap
environment.filters['add_to_front'] = add_to_front
environment.filters['authors_ccsc'] = authors_ccsc
environment.filters['authors_acm'] = authors_acm



dict = {'variable' : 'test',
        'data': ['tee, bob', 'john, ', 'tony,bro', 'alex, m'],
        'date': '2006',
        'author': ['alex'],
        'title': 'Shitty book',
        'journal':'Wall Street',
        'volume': '1000',
        'issue':'green',
        'pages':'97-100',
        'year':'2007',
        'num': '1',
        'publisher': 'scholastic',
        'city': 'narnia',
        'retrieved': 'March 3, 2017',
        'url': 'www.google.com'}
template_string = "{% if variable is defined %}{{ variable|wrap_html('b')|add_chars('#$$') }}{{ data[1:3]|join(',')|add_chars('#')|wrap('(') }}{% else %}{{ data2|join(',') if data2 else '' }}{{','}}{% endif %}"
ts = "{{num|add_chars('. ') if num else ''}}{{author|authors_acm() if author else '' }}{{editor|authors_acm() if editor else '' }}{{title|add_chars('. ') if title else '' }}{{publisher|add_chars(', ') if publisher else '' }}{{city if city else ''}}{% if city is defined and year is defined %}{{year|add_chars('.')|add_to_front(', ')}}{% elif year is defined %}{{year|add_chars('.')}}{% else %}{{'.'}}{% endif %}"
template = environment.from_string(ts)
output = template.render(dict)
print(output)

# import re
# test = 'Zupperle, Auther'
# print(re.findall('\w+,\s+', test)[0].split(',')[0])
# print(re.findall('\s(\w)', test))

