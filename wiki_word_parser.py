# pip install lxml
# pip install markdown 
from lxml import etree
from lxml.etree import tostring
import sys
import re
from collections import Counter

# Parses mediawiki xml file to element tree
def parse_mw(filename):
    tree = etree.parse(filename)
    return tree.getroot()

# Finds all text in element tree
def get_texts(root):
    return root.findall('.//text', namespaces=root.nsmap)

def get_text_by_title(root,lookup):
    pages = root.findall('.//page', namespaces=root.nsmap)
    for page in pages:
        title = page.find('.//title', namespaces=page.nsmap)
        print(title.text)
        if title.text == lookup:
            return page.find('.//text', namespaces=page.nsmap)
    return None

# Filters out links. 
# Example: 'example.com' -> ''
def links_re():
    urls = "([^\s\n<>]+\.[^(\s\n<>\},\.)]+(\s|\n|\}|\|))" 
    return urls

# Filters out numbers. 
# Example: '123' -> ''
def number_re():
    return "(\s(\d)+\s)"

# Filters out markdown symbols. 
# Example: '== Header ==' -> 'Header'
def markdown_symbols_re():
    sections = "(==+)"
    bold_italics = "(''+)"
    lists = "(\*)"
    return '|'.join([
        sections,
        bold_italics,
        lists
    ])

# Filters out mediawiki special syntax. 
# Example: '{{ Infobox some text' -> 'some text'
def wikipedia_special_re():
    infobox = "(\{\{(I|i)nfobox)"
    infobox_fields = "(\|.*?=)"
    end_box = "(\{\{end box)"
    redirects = "(#(redirect|REDIRECT))|(\{\{R\sfrom\s.*?\}\})"
    links = "(\[+((Category|Template):)?)|(\]+)"
    return '|'.join([
        infobox,
        infobox_fields,
        redirects,
        links,
    ])

# Filters out special characters. 
# Example: '={' -> ''
def special_char_re():
    return "([()|\{\}‘’\"\-,\=])"

# Filters out refrence syntax.
# Example: '{{cite web' -> ''
def ref_re():
    reflist_re = "(\{\{(R|r)eflist\}\})"
    cite_Re = "(\{\{cite(\s|\n)web)"
    return '|'.join([
        reflist_re,
        cite_Re
    ])

# Filters out the beginning of an template.
# Example: '{{color|some text' -> 'some text'
def templates_re():
    return "(\{\{(.*?\|)?)"

# Filters out html tags and attributes. 
# Example '<b class="123">some text</b>' -> 'some text'
def html_re():
    tags = "(<\/?.*?>)"
    attrib = "([^(\s|\n)]+=[^(\s|\n)]*)"
    attrib_value = "(\".*?;?\")|[^(\s|\n)]*?(;|:)"
    return '|'.join([
        tags,
        attrib,
        attrib_value
    ])

# Joins all the regex filters together and creates one.
def re_filter():
    return '|'.join([
        wikipedia_special_re(),
        ref_re(),
        links_re(),
        templates_re(),
        markdown_symbols_re(),
        html_re(),
        number_re(),
        special_char_re()
    ])

# Filters out words using a regex string.
def filter_words(text, re_filter):
    return re.sub(re_filter, ' ', text)

# Splits text into words. 
def split_string(s):
    return re.split('\s+|(?<!\d)[,:]|[,:](?!\d)|-', s)

# Checks if a word only includes valid characters. 
def is_word(word):
    return re.match('(-|[a-zA-Z]|\d)*[a-zA-Z](-|[a-zA-Z]|\d)*', word)


# Adds a word to a counter collection if it is valid.
def count_word(word, word_counter):
    #print(word)
    if not is_word(word): 
        #if word not in ['','$6','-']:
        #print(word) #safety check
        #   quit()
        return
    key = re.sub('\s+','', word.lower())
    if not key in word_counter.keys(): 
        word_counter[key] = 0
    word_counter[key] +=1

# Converts texts to words and adds them to a counter collection. 
def convert_texts(texts):
    word_counter = Counter()
    temp = texts[:3]
    for node in texts:
        if node.text:
            cleaned_text = filter_words(node.text, re_filter())
            words = split_string(cleaned_text)
            for word in words: 
                count_word(word, word_counter)  
    return word_counter

# Returns the n most common words in a counter collection
def get_top_words(counter, n):
    return counter.most_common(n)
