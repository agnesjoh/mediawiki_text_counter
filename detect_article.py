import sys
import wiki_word_parser as wikiparser
import csv
from collections import Counter

def get_common_words(n):
	with open('top_{}.txt'.format(n), newline='') as csvfile:
		rows = csv.reader(csvfile, delimiter=',')
		return [row[0] for row in rows]

def filter_common(word_counter, filter_list):
	article_specific_words = Counter()
	for word in word_counter:
		if word not in filter_list:
			article_specific_words[word] = word_counter[word]
	return article_specific_words

def write_output(output, article):
    with open('{}_top_10.txt'.format(article), 'w', newline='') as f:
        w = csv.writer(f)
        for word in output:
            w.writerow(list(word))

def main():
	filename = sys.argv[1]

	if len(sys.argv) < 3:
		print('title missing')
		return

	title = sys.argv[2]

	if len(sys.argv) > 3:
		n = sys.argv[3]
	else: 
		n = 100
	root = wikiparser.parse_mw(filename)
	text_node = wikiparser.get_text_by_title(root, title)
	filter_words = get_common_words(n)
	word_counter = wikiparser.convert_texts([text_node])
	top_article_words = filter_common(word_counter, filter_words)
	top_10 = wikiparser.get_top_words(top_article_words, 10)
	write_output(top_10, title)
main()