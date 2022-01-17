import os
from glob import glob
import re

import PyPDF2
import pytesseract
from pdfminer.high_level import extract_text
from reportlab.lib.pagesizes import A4, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Paragraph
from reportlab.platypus.flowables import Spacer
from reportlab.platypus.frames import Frame
from tqdm import tqdm


def imgfile_to_pdf(img_file):
    # gray = cv2.cvtColor(img_file, cv2.COLOR_BGR2GRAY)
    pdf = pytesseract.image_to_pdf_or_hocr(
                                    img_file,
                                    lang="jpn",
                                    config="--dpi 300",
                                    extension='pdf'
                                    )
    root, ext = os.path.splitext(img_file)
    pdf_name = root + ".pdf"
    with open(pdf_name, 'w+b') as f:
        f.write(pdf)  # pdf type is bytes by default
    return pdf_name


def get_jpg_files(folder):
    jpg_files = glob(folder+"/*.jpg")
    return jpg_files


def make_text_pdf(folder, text_list):
    file_path = folder+"/text.pdf"
    pdfmetrics.registerFont(TTFont("yumin", "C:/Windows/Fonts/yuminl.ttf"))
    doc = BaseDocTemplate(
        file_path,
        title="Text",
        pagesize=(200*mm, 200*mm),
        )

    frames = [Frame(10*mm, 20*mm, 180*mm, 180*mm, showBoundary=0)]

    page_template = PageTemplate("frames", frames=frames)
    doc.addPageTemplates(page_template)

    style_dict = {
        "name": "normal",
        "fontName": "yumin",
        "fontSize": 10,
        "leading": 10,
        "firstLineIndent": 10,
        }
    style = ParagraphStyle(**style_dict)

    flowables = []
    space = Spacer(10*mm, 10*mm)
    for text in text_list:
        para = Paragraph(text, style)
        flowables.append(para)
    doc.multiBuild(flowables)
    return file_path

def jpg_to_pdf(jpg_files):
    merger = PyPDF2.PdfFileMerger()
    pdfs = []
    text_list = []
    for jpg_file in tqdm(jpg_files):
        pdf_name = imgfile_to_pdf(jpg_file)
        merger.append(pdf_name)
        pdfs.append(pdf_name)
        text = extract_text(pdf_name).replace(" ", "")
        text = text.replace("<","")
        text = text.replace(">","")
        text_list.append(text)

    code_regex = re.compile('[!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％]')

    text_pdf = make_text_pdf(folder=folder, text_list=text_list)
    pdfs.append(text_pdf)
    merger.append(text_pdf)
    merged_name = extract_text(pdfs[0])
    merged_name = merged_name.split("\n")[0]
    merged_name = merged_name.replace(" ", "")
    merged_name = code_regex.sub('', merged_name)
    if os.path.exists(f"{merged_name}.pdf"):
        print("Failure !!: Cannot save the same file name !")
        merger.close()
        for pdf_file in pdfs:
            os.remove(pdf_file)
    else:
        merger.write(f"{merged_name}.pdf")
        merger.close()
        for pdf_file in pdfs:
            os.remove(pdf_file)


folder = input("input scaned_file folder: ")
jpg_files = get_jpg_files(folder)
jpg_to_pdf(jpg_files=jpg_files)