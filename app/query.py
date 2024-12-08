import json


def search_book_by_title(title, json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            books = []
            for line in file:
                try:
                    book = json.loads(line.strip())  # Parse each line as JSON
                    if title.lower() in book.get('title', '').lower():
                       books.append(book)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
            return books
    except Exception as e:
        print(f"Error querying JSON: {e}")
    return None
