import pytesseract
import cv2

def extract_book_title(image_path):
    try:
        # Load the image
        img = cv2.imread(image_path)

        # Apply OCR
        text = pytesseract.image_to_string(img)
        print("Extracted Text:")
        print(text)
        lines = text.split('\n')

        # Return the first non-empty line as a potential book title
        for line in lines:
            line = line.strip()
            if line:
                return line
    except Exception as e:
        print(f"Error during OCR: {e}")
    return None