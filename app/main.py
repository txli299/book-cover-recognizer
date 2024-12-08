import os
from flask import Flask, request, jsonify
from ocr import extract_book_title
from query import search_book_by_title

app = Flask(__name__)

# Path to JSON database
JSON_FILE_PATH = "app/books.json"


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Ensure the temp directory exists
    temp_dir = "app/temp"
    os.makedirs(temp_dir, exist_ok=True)

    # Save uploaded file
    file_path = os.path.join(temp_dir, file.filename)
    file.save(file_path)

    # Extract book title using OCR
    title = extract_book_title(file_path)
    if not title:
        return jsonify({'error': 'Unable to extract book title'}), 400

    # Search for book information
    book_info = search_book_by_title(title, JSON_FILE_PATH)
    if book_info:
        return jsonify(book_info)
    else:
        return jsonify({'error': f'No book found for title: {title}'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
