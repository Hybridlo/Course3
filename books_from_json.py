from add_book import add_book
import json

if __name__ == '__main__':
    with open('books.txt', 'r') as infile:
        data = json.load(infile)
        for entry in data:
            d = {}
            d['title'] = entry.get('title')
            d['isbn'] = entry.get('isbn', '')
            d['description'] = entry.get('longDescription', '')
            d['authors'] = ', '.join(entry['authors'])
            d['tags'] = ', '.join(entry['categories'])
            add_book(d)