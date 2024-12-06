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
    docker run -d -p 5000:5000 book-scanner
    ```
3. Test the application:

    Upload an image of a book cover using tools like Postman or curl:
     ```bash
     curl -X POST -F "file=@path_to_book_cover.jpg" http://localhost:5000/upload
     ```
### Dependencies
* Flask: API framework
* OpenCV: Image processing
* pytesseract: OCR engine


