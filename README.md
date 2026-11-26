# Banca dati Polizia di Stato

A project developed to extract, organize and practice with the question bank for the 2025 Vice Inspectors selection process.

The repository brings together two distinct parts of the workflow:

1. **Question-bank extraction** — OCR processing of the source PDF, segmentation of question blocks and storage in SQLite.
2. **Web quiz application** — a PHP/JavaScript application that retrieves questions from MySQL and provides a mobile-friendly quiz experience.

A Flask implementation is also retained as an experimental prototype; it is not the PHP/JavaScript application described above.

## Project structure

```text
.
├── parser/                 # PDF/OCR extraction and SQLite preparation
├── web-app/                # PHP API and JavaScript quiz frontend
├── flask-prototype/        # Alternative Flask implementation
└── docs/                   # Architecture and workflow notes
```

## Workflow

1. Process the PDF with the Python OCR pipeline.
2. Store extracted questions and answers in a SQLite database.
3. Review/mark the correct answers in a separate database step.
4. Export/import the data into MySQL for the hosted quiz application.
5. The browser requests questions from the PHP endpoint; quiz navigation, answer selection and result display are handled in JavaScript.

## Technology stack

- Python, OpenCV, NumPy, Tesseract OCR and pdf2image
- SQLite for local extraction output
- PHP and MySQL for the web application API
- HTML, CSS, JavaScript and Bootstrap 5 for the interface
- Flask for the alternative prototype

## Important notes

- The original PDF, generated database files and SQL dumps are not included. They may contain third-party copyrighted material or derived question-bank data; only distribute them when you have the right to do so.
- Configure database credentials through server-side environment/configuration values. Never commit production credentials.
- The OCR script currently initializes the SQLite database by deleting an existing database at its configured output path. Back up any database before running it.
- The extracted dataset and quiz results should be checked before relying on them for exam preparation.
- The PHP/JavaScript application was used as the hosted version; the Flask code is retained separately as a prototype.

## Documentation

See [docs/architecture.md](docs/architecture.md) for the component overview and data flow.
