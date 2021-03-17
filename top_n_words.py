import wiki_word_parser as wikiparser
import sys


def main():
    #handle arguments
    filename = sys.argv[1]
    if len(sys.argv) > 2:
    	n = int(sys.argv[2])
    else:
    	n = 100

    # get an etree from xml file
    root = wikiparser.parse_mw(filename)
    # get all text nodes in the etree
    text_nodes = wikiparser.get_texts(root)
    # split the text into word counter collection
    word_counter = wikiparser.convert_texts(text_nodes)
    # get the top n words from the word counter collection
    top_n = wikiparser.get_top_words(word_counter, n)
    # write results to a file
    filename = 'top_{}.txt'.format(n)
    wikiparser.write_output(top_n, filename)
    
main()