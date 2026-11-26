# OCR parser

This directory is reserved for the Python PDF/OCR pipeline and the separate SQLite answer-marking utility.

## Dependencies

The recovered extraction script imports:

- opencv-python
- numpy
- pytesseract
- pdf2image

It also requires external installations of Tesseract OCR (Italian language data) and Poppler. Configure their executable paths and the input PDF path for your operating system before running.

## Data safety

The current extraction implementation deletes the database at its configured output path when initializing it. Make a backup before execution. The answer-marking utility assumes that option A is the correct answer for each extracted question; verify that assumption against the source data.
