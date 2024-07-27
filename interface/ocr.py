import pytesseract, PIL, markdown2, io, requests
pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR/tesseract.exe'


def convert_to_str(url: str) -> str:
    image = PIL.Image.open(io.BytesIO(requests.get(url).content))
    image_rgb = image.convert('RGB')
    text = pytesseract.image_to_string(image_rgb, lang='ben+eng')
    return text
    

def convert_to_html(url: str) -> str:
    text = convert_to_str(url)
    text_utf_8 = text.encode('utf-8').decode('utf-8')
    html = str(markdown2.markdown(text_utf_8)).replace('\n', '<br>')
    return html
