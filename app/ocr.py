import pytesseract
import cv2
import re


# def extract_text(image_path):
#     """
#     Extract and clean text from the image using OCR.
#     Args:
#         image_path (str): Path to the image file.
#     Returns:
#         list: List of cleaned lines or None if extraction fails.
#     """
#     try:
#         # Load the image
#         img = cv2.imread(image_path)
#         print(f"Original Dimensions: {img.shape}")
#
#         # Apply OCR
#         raw_text = pytesseract.image_to_string(img, config="--psm 3")
#         print(raw_text)
#         # Split text into lines and clean each line
#         lines = raw_text.split('\n')
#         cleaned_lines = [
#             # Clean and strip non-printable characters
#             re.sub(r'[^\x20-\x7E]', '', line).strip()
#             for line in lines if line.strip()  # Remove empty lines
#         ]
#
#         print("Extracted Lines:")
#         for line in cleaned_lines:
#             print(line)
#
#         return cleaned_lines if cleaned_lines else None
#     except Exception as e:
#         print(f"Error during OCR: {e}")
#         return None

def preprocess_image(image_path):
    """
    Preprocess the image to improve OCR accuracy.
    Args:
        image_path (str): Path to the image file.
    Returns:
        numpy.ndarray: Preprocessed image.
    """
    # Load the image
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to remove noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply thresholding to make the text stand out
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh

def extract_text(image_path):
    """
    Extract and clean text from the image using OCR.
    Args:
        image_path (str): Path to the image file.
    Returns:
        list: List of cleaned lines or None if extraction fails.
    """
    try:
        # Preprocess the image
        preprocessed_img = preprocess_image(image_path)

        # Apply OCR
        raw_text = pytesseract.image_to_string(preprocessed_img, config="--psm 3")
        print(f"Raw OCR Output:\n{raw_text}")

        # Split text into lines and clean each line
        lines = raw_text.split('\n')
        cleaned_lines = [
            # Clean and strip non-printable characters
            re.sub(r'[^\x20-\x7E]', '', line).strip()
            for line in lines if line.strip()  # Remove empty lines
        ]

        print("Extracted and Cleaned Lines:")
        for line in cleaned_lines:
            print(line)

        return cleaned_lines if cleaned_lines else None
    except Exception as e:
        print(f"Error during OCR: {e}")
        return None