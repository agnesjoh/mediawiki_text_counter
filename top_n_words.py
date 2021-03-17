import wiki_word_parser as wikiparser
import sys


def main():
    #handle arguments
    filename = sys.argv[1]
    if len(sys.argv) > 2:
    	n = sys.argv[2] 
    else:
    	n = 100

    # get an etree from xml file
    root = wikiparser.parse_mw(filename)
    # get all text nodes in the etree
    text_nodes = wikiparser.get_texts(root)
    # split the text into word counter collection
    word_counter = wikiparser.convert_texts(text_nodes)
    # get the top 100 words from the word counter collection
    top_100 = wikiparser.get_top_words(word_counter, n)
    # write results to a file
    filename = 'top_{}.txt'.format(n)
    wiki_word_parser.write_output(top_100, filename)
main()