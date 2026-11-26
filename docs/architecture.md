# Architecture and data flow

## 1. OCR extraction

The Python extraction pipeline converts PDF pages to images, preprocesses them with OpenCV, splits each page into two columns, detects horizontal separators and crops individual question blocks. Tesseract performs Italian OCR on each block. A regular-expression parser separates the question text from answer options A–E.

The extracted records are written to SQLite using two tables:

- `domande(id, testo)`
- `risposte(id, domanda_id, testo, lettera, corretta)`

The current script uses a fixed 773-page input assumption and Windows-specific Poppler/Tesseract paths that must be configured for the machine running it.

## 2. Correct-answer marking

A separate script updates the `corretta` field in SQLite. In the recovered version, it marks answer A as correct and all other letters as incorrect. This is a dataset-specific assumption, not a general answer-validation algorithm; validate the source data before using it.

## 3. Hosted quiz application

The PHP endpoint connects to MySQL, selects a random set of questions according to the selected subject range, loads the related answers and returns JSON. The browser frontend fetches that JSON and manages question navigation, answer selection, shuffling and score display.

The application is a client-side quiz interface backed by PHP/MySQL. The database was populated separately by importing SQL data.

## 4. Alternative Flask prototype

The repository also contained a Flask/MySQL implementation with Jinja templates and a CGI entry point. It is preserved under `flask-prototype/` as an alternative implementation and should not be confused with the PHP/JavaScript version used for the hosted quiz.

## Operational and security considerations

- Keep MySQL credentials outside version control.
- Do not expose the `corretta` field to untrusted clients if quiz answers must remain hidden until submission.
- Validate and cap request parameters on the server.
- Keep source PDFs, database exports and other potentially copyrighted datasets out of the public repository unless distribution is authorized.
- Back up the SQLite database before running the OCR script, which recreates its output database.
