import pytesseract
import cv2


def extract_text(image_path):
    """
    Extract text from the image using OCR.
    Args:
        image_path (str): Path to the image file.
    Returns:
        str: Extracted text or None if extraction fails.
    """
    try:
        # Load the image
        img = cv2.imread(image_path)

        # Apply OCR
        text = pytesseract.image_to_string(img)
        print(text)
        return text.strip()
    except Exception as e:
        print(f"Error during OCR: {e}")
        return None
