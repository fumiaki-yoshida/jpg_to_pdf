from PIL import Image
import sys
import cv2
import numpy as np
import pytesseract
import os
from glob import glob
from tqdm import tqdm
import PyPDF2
from pdfminer.high_level import extract_text
import re
import shutil

def imgfile_to_pdf(img_file):
    pdf = pytesseract.image_to_pdf_or_hocr(img_file,
                                    lang="jpn",
                                    extension='pdf'
                                    )
    root, ext = os.path.splitext(img_file)
    pdf_name = root + ".pdf"
    with open(pdf_name, 'w+b') as f:
        f.write(pdf) # pdf type is bytes by default
    return pdf_name

def get_jpg_files(folder):
    jpg_files = glob(folder+"/*.jpg")
    return jpg_files


folder = input("input scaned_file folder: ")
jpg_files = get_jpg_files(folder)
merger = PyPDF2.PdfFileMerger()
pdfs = []
for jpg_file in tqdm(jpg_files):
    pdf_name = imgfile_to_pdf(jpg_file)
    merger.append(pdf_name)
    pdfs.append(pdf_name)

merged_name = extract_text(pdfs[0])
merged_name = merged_name.split("\n")[0]
if os.path.exists(f"{merged_name}.pdf"):
    print("Cannot save the same file name !")
    merger.close()
    for pdf_file in pdfs:
        os.remove(pdf_file)
else:
    merger.write(f"{merged_name}.pdf")
    merger.close()
    for pdf_file in pdfs:
        os.remove(pdf_file)

