import pytesseract
import cv2
import re


def extract_text(image_path):
    """
    Extract and clean text from the image using OCR.
    Args:
        image_path (str): Path to the image file.
    Returns:
        list: List of cleaned lines or None if extraction fails.
    """
    try:
        # Load the image
        img = cv2.imread(image_path)
        print(f"Original Dimensions: {img.shape}")

        # Apply OCR
        raw_text = pytesseract.image_to_string(img, config="--psm 3")
        print(raw_text)
        # Split text into lines and clean each line
        lines = raw_text.split('\n')
        cleaned_lines = [
            # Clean and strip non-printable characters
            re.sub(r'[^\x20-\x7E]', '', line).strip()
            for line in lines if line.strip()  # Remove empty lines
        ]

        print("Extracted Lines:")
        for line in cleaned_lines:
            print(line)

        return cleaned_lines if cleaned_lines else None
    except Exception as e:
        print(f"Error during OCR: {e}")
        return None
