# OCR parser

Recovered Python OCR pipeline for extracting question blocks from the 2025 Vice Inspectors PDF, plus the separate script used to mark the correct option.

## Requirements

Install the packages in `requirements.txt`. Tesseract OCR with Italian language data and Poppler must also be installed separately.

## Configuration

The parser accepts these environment variables:

- `SOURCE_PDF`: source PDF path (default: `Banca-dati-2025-Vice-Ispettori.pdf`)
- `OUTPUT_DB`: SQLite output path (default: `data/banca_dati_blocchi.db`)
- `POPPLER_BIN_PATH`: optional Poppler binary directory
- `TESSERACT_CMD`: optional Tesseract executable path
- `TOTAL_PAGES`: page count (default: 773)

## Run

```bash
python Estrattore_dati.py
python test.py
```

**Important:** the extraction script recreates and deletes the existing database at `OUTPUT_DB` before processing. Back it up first. The answer-marking script marks every option labelled A as correct, matching the recovered project workflow; validate that assumption against the source material before using the generated data.
