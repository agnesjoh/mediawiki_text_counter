# mediawiki_text_counter

mediawiki_text_counter is a collection of python scripts to count words from a MediaWiki XML file. The parser filters out words from each article and creates a counter collection. With help from the parser, we can create files with the most common words in thousands of articles and find the most relevant words in each article by filtering out words common in a big group of articles and only returning those specific for the given article.

## Installation

Python version 3 required.
Use the package manager [pip](https://pip.pypa.io/en/stable/) for setup.

```bash
# pip install lxml
```

## Usage

To get top n (default is 100) common words from collection of articles:
```python
python top_n_words.py filename.xml n
```
To get most relevant n (default is 10) words from an article by title (file with top 100 common words must exist):
```python
python detect_article.py filename.xml title n 
```
