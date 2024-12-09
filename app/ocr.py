import cv2
import pytesseract
from pytesseract import Output
import spacy
import re
from query import search_book_by_title

# 加载 NLP 模型
nlp = spacy.load("en_core_web_sm")

def preprocess_image(image_path):
    """预处理图像以优化 OCR 检测"""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 应用高斯模糊
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # 二值化
    _, binary = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)
    return binary

def extract_text(image_path):
    """从图像中提取文字"""
    # 图像预处理
    processed_image = preprocess_image(image_path)

    # 使用 Tesseract 提取文字
    custom_config = r'--oem 3 --psm 6'  # 默认配置：OCR 引擎模式和页面分割模式
    text = pytesseract.image_to_string(processed_image, config=custom_config)
    
    # 清理提取出的文本
    lines = text.split('\n')
    cleaned_lines = [line.strip() for line in lines if len(line.strip()) > 2]  # 过滤空行或短行
    return cleaned_lines

def filter_book_titles(text_lines, database_path):
    """根据提取的文本筛选可能的书名"""
    potential_titles = []

    for line in text_lines:
        # 使用正则表达式匹配可能的书名
        if re.match(r'^[A-Z][a-zA-Z0-9\s:;,"\'-]+$', line):
            potential_titles.append(line)

    # 与数据库匹配
    matched_titles = []
    for title in potential_titles:
        matches = search_book_by_title(title, database_path)
        if matches:
            matched_titles.extend(matches)

    return matched_titles

def extract_and_match_titles(image_path, database_path):
    """综合提取书名并匹配数据库"""
    extracted_text = extract_text(image_path)
    matched_books = filter_book_titles(extracted_text, database_path)
    return matched_books
