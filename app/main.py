import os
from flask import Flask, request, jsonify
from ocr import extract_text
from query import search_book_by_title

app = Flask(__name__)

# Path to JSON database
JSON_FILE_PATH = "bookMeta.jsonl.json"


# OCR API: Extract text from an uploaded image
@app.route('/ocr', methods=['POST'])
def ocr_text():
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

    # Extract text using OCR
    text = extract_text(file_path)
    if text:
        return jsonify({'extracted_text': text})
    else:
        return jsonify({'error': 'Unable to extract text from image'}), 500


# Book Info API: Search book information using a title
@app.route('/search', methods=['POST'])
def search_book():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'No title provided'}), 400
    title = data['title']
    book_info = search_book_by_title(title, JSON_FILE_PATH)
    if book_info:
        return jsonify(book_info)
    else:
        return jsonify({'error': f'No book found for title: {title}'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
