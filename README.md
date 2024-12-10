 # Book Cover Recognizer

This application scans book covers to extract the title and fetches book details from a JSON database.

## How to Run

### Prerequisites
- Docker installed

### Steps
1. Build the Docker image:
   ```bash
   docker build -t book-scanner .
2. Run the Docker container:
    ```bash
    docker run -d -p 5001:5001 book-scanner
    ```
3. Test the application:

    Upload an image of a book cover using tools like Postman or curl:
     ```bash
     curl -X POST -F "file=@path_to_book_cover.jpg" http://localhost:5001/upload
     ```

### Additional Setup for Google Vision API

1. Enable the Google Vision API in your Google Cloud project.
2. Download the JSON key file for your Google Cloud service account and rename it to `google_credentials.json`.
3. Place the `google_credentials.json` file in the root directory of the project.

### Dependencies
* Flask: API framework
* OpenCV: Image processing
* pytesseract: OCR engine
* Google Vision API: OCR engine


## Endpoints

### 1. `/ocr` (POST)
Extract text from an uploaded image using Optical Character Recognition (OCR).

#### Request:
- **Method**: `POST`
- **Form Data**:
  - `file`: Image file to process

#### Response:
- **200 OK**:
  ```json
  {"extracted_text": ["line1", "line2", ...]}

### 1. `/search` (POST)
Search for book information using a title.

#### Request:
- **Method**: `POST`
- **Form Data**:
  - `title`: Book Title

#### Response:
- **200 OK**:
  ```json
  {"title": "Book Title", "author": "Author Name", ...}