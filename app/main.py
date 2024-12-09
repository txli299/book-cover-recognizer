import os
from ocr import extract_text, extract_and_match_titles
from query import search_book_by_title
import os
from flask import Flask, request, jsonify
from ocr import extract_and_match_titles

app = Flask(__name__)
JSON_FILE_PATH = "app/bookMeta.jsonl.json"

@app.route('/ocr', methods=['POST'])
def ocr_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    temp_dir = "app/temp"
    os.makedirs(temp_dir, exist_ok=True)

    file_path = os.path.join(temp_dir, file.filename)
    file.save(file_path)

    result = extract_and_match_titles(file_path, JSON_FILE_PATH)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
