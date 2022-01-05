# jpg_to_pdf

## Overview

フォルダにあるjpgファイルに対してOCR処理を行い、一つのPDFにする。  

## Requirement

- python3.7以上
- tesseract
- pytesseract

## Usage

あらかじめ、ひとつのPDFにしたいjpgファイルをフォルダ内に入れておく  
以下のコマンドをコマンドラインに入力する。  
  
`python jpg_to_pdf.py`

pdf化したいフォルダを聞かれるので相対パスで入力する。

## Feature

## Preparation

### [tessaract](https://github.com/tesseract-ocr/tesseract)

- [The Mannheim University Library](https://github.com/UB-Mannheim/tesseract/wiki) が用意したexeファイルで入れる
  - [https://github.com/tesseract-ocr/tessdata] から日本語の学習済みデータをダウンロードする
  - ダウンロードしたデータを tessaract の tessdata に入れる
  - 例: C:\Users\<username>\AppData\Local\Programs\Tesseract-OCR\tessdata
  - Tesseract-OCR にパスを通す

## Author

[Yoshida Fumiaki](https://github.com/fumiaki-yoshida)

## Licence

MIT License
