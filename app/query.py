import json


def search_book_by_title(title, json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            books = json.load(file)
            for book in books:
                if title.lower() in book.get('title', '').lower():
                    return book
    except Exception as e:
        print(f"Error querying JSON: {e}")
    return None
