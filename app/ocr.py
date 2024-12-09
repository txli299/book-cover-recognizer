import re
import spacy
import json
import unicodedata
from google.cloud import vision
from query import search_book_by_title

nlp = spacy.load("en_core_web_sm")

def normalize_text(text):
    """
    Normalize text by:
    - Unicode normalization to NFD
    - Removing diacritical marks
    - Lowercasing
    - Stripping whitespace
    """
    text = unicodedata.normalize('NFD', text)
    text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Mn')
    text = text.lower().strip()
    return text

def extract_text(image_path):
    """
    Use Google Cloud Vision API to extract text from an image.
    Make sure you have set GOOGLE_APPLICATION_CREDENTIALS environment variable.

    Returns: A list of lines of extracted text.
    """
    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(f'Vision API Error: {response.error.message}')

    annotations = response.text_annotations
    if not annotations:
        return []

    full_text = annotations[0].description
    raw_lines = full_text.split('\n')
    extracted_lines = [line.strip() for line in raw_lines if len(line.strip()) > 1]

    return extracted_lines

def find_book_info_from_extracted_text(text_lines, database_path):
    """
    Given OCR extracted lines, try to find matching book info from the database.
    Improvement: Now using exact normalized equality checks instead of substring matches.

    For each line:
    - Normalize it.
    - Use search_book_by_title as an initial filter (based on substring in original code).
    - Then re-check matches by strict equality:
      If normalized line == normalized title OR normalized line == normalized author, consider it a match.
    """
    matches_info = []
    for line in text_lines:
        norm_line = normalize_text(line)
        
        # Initial search using substring match (as implemented in query.py)
        matched_books = search_book_by_title(line, database_path)
        if matched_books is None:
            continue

        final_matched_books = []
        for book in matched_books:
            book_title = normalize_text(book.get("title", ""))
            book_author = normalize_text(book.get("author", ""))
            
            # Strict equality check
            # Only consider it a match if norm_line exactly equals the title or the author
            if norm_line == book_title or norm_line == book_author:
                final_matched_books.append(book)

        # If no books found in the initial filtered set, try scanning the entire file again
        # This is a fallback approach if needed.
        if not final_matched_books:
            try:
                with open(database_path, 'r') as f:
                    for b_line in f:
                        try:
                            b_book = json.loads(b_line.strip())
                            b_title = normalize_text(b_book.get("title", ""))
                            b_author = normalize_text(b_book.get("author", ""))

                            if norm_line == b_title or norm_line == b_author:
                                final_matched_books.append(b_book)
                        except:
                            pass
            except:
                pass

        # Build final result list
        for book in final_matched_books:
            book_info = {
                "title": book.get("title", ""),
                "subtitle": book.get("subtitle", ""),
                "author": book.get("author", ""),
                "publisher": book.get("publisher", []),
                "isbn10": book.get("isbn10", []),
                "isbn13": book.get("isbn13", []),
                "synopsis": book.get("synopsis", "")
            }
            matches_info.append(book_info)

    return matches_info

def extract_and_match_titles(image_path, database_path):
    """
    Extract lines from image using OCR and then match them against the database.
    Returns a dict:
    {
        "extracted_text": [...],
        "matches": [ {...}, {...} ]
    }
    """
    extracted_text = extract_text(image_path)
    matched_books = find_book_info_from_extracted_text(extracted_text, database_path)
    return {
        "extracted_text": extracted_text,
        "matches": matched_books
    }
