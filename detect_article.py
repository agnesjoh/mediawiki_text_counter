import wiki_word_parser as wikiparser
import sys

def main():
	#handle arguments
	if len(sys.argv) < 3:
		print('title missing')
		return

	filename = sys.argv[1]
	title = sys.argv[2]

	if len(sys.argv) > 3:
		n = int(sys.argv[3])
	else: 
		n = 100

	# get an etree from xml file
	root = wikiparser.parse_mw(filename) 
	# get a list of common words from top_100.txt file
	filter_words = wikiparser.get_common_words(100)
	# get a text from page by using the title as search lookup
	text_node = wikiparser.get_text_by_title(root, title) 
	# split the text into word counter collection
	word_counter = wikiparser.convert_texts([text_node])
	# remove common words from the counter collection
	top_article_words = wikiparser.filter_common(word_counter, filter_words)
	# fetch the top n relevant words from the word counter collection
	top_n = wikiparser.get_top_words(top_article_words, n)
	# write results to a file
	filename = '{}_top_{}.txt'.format(title, n)
	wikiparser.write_output(top_n, filename)

main()