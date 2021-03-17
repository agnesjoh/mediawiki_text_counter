import wiki_word_parser as wikiparser
import sys
import csv


# Writes to a file
def write_output(output, n):
    with open('top_{}.txt'.format(n), 'w', newline='') as f:
        w = csv.writer(f)
        for word in output:
            w.writerow(list(word))

def main():
    filename = sys.argv[1]
    if len(sys.argv) > 2:
    	n = sys.argv[2] 
    else:
    	n = 100
    root = wikiparser.parse_mw(filename)
    text_nodes = wikiparser.get_texts(root)
    word_counter = wikiparser.convert_texts(text_nodes)
    top_100 = wikiparser.get_top_words(word_counter, n)
    write_output(top_100,n)
main()