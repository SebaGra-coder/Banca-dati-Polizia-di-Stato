import sqlite3
import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_path
import re
import os

# Input/output paths can be overridden for different environments.
PDF_PATH = os.environ.get("SOURCE_PDF", "Banca-dati-2025-Vice-Ispettori.pdf")
DB_PATH = os.environ.get("OUTPUT_DB", "data/banca_dati_blocchi.db")
POPPLER_BIN_PATH = os.environ.get("POPPLER_BIN_PATH", "")
TESSERACT_CMD = os.environ.get("TESSERACT_CMD", "")
if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
if POPPLER_BIN_PATH and POPPLER_BIN_PATH not in os.environ.get("PATH", ""):
    os.environ["PATH"] += os.pathsep + POPPLER_BIN_PATH

SPLIT_RATIO = 0.445

def init_db():
    # NOTE: this intentionally recreates the output DB, matching the recovered script.
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS domande (id INTEGER PRIMARY KEY AUTOINCREMENT, testo TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS risposte (id INTEGER PRIMARY KEY AUTOINCREMENT, domanda_id INTEGER, testo TEXT, lettera TEXT, corretta INTEGER, FOREIGN KEY(domanda_id) REFERENCES domande(id))""")
    conn.commit()
    return conn

def preprocess_image(pil_image):
    img = np.array(pil_image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    return thresh

def split_columns(image, ratio):
    height, width = image.shape
    split_point = int(width * ratio)
    return image[:, 0:split_point], image[:, split_point:width]

def find_horizontal_lines_and_crop(image_col):
    inverted = cv2.bitwise_not(image_col)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 1))
    detected_lines = cv2.morphologyEx(inverted, cv2.MORPH_OPEN, kernel, iterations=1)
    contours, _ = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    y_coords = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        y_coords.append(y)
    height, width = image_col.shape
    y_coords.extend([0, height])
    y_coords.sort()
    filtered_y = [y_coords[0]]
    for y in y_coords[1:]:
        if y - filtered_y[-1] > 20:
            filtered_y.append(y)
    crops = []
    for i in range(len(filtered_y) - 1):
        y_top, y_bottom = filtered_y[i], filtered_y[i + 1]
        crop = image_col[y_top:y_bottom, :]
        if crop.shape[0] >= 50:
            crops.append(crop)
    return crops

def parse_single_block(text, conn):
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if not lines:
        return
    cursor = conn.cursor()
    re_answer = re.compile(r"^([A-E])\)\s+(.*)")
    question_text = ""
    answers = []
    is_parsing_answers = False
    for line in lines:
        match = re_answer.match(line)
        if match:
            is_parsing_answers = True
            answers.append({"lettera": match.group(1), "testo": match.group(2)})
            continue
        if not is_parsing_answers:
            if question_text == "":
                line = re.sub(r"^([|\d]+)[\.,\)\s]*\s*", "", line)
            question_text += line + " "
        elif answers:
            answers[-1]["testo"] += " " + line
    if question_text and answers:
        question_text = question_text.strip()
        cursor.execute("INSERT INTO domande (testo) VALUES (?)", (question_text,))
        q_id = cursor.lastrowid
        for answer in answers:
            cursor.execute("INSERT INTO risposte (domanda_id, testo, lettera, corretta) VALUES (?, ?, ?, 0)",
                           (q_id, answer["testo"], answer["lettera"]))
        conn.commit()
        print(f"    -> [OK] Inserita domanda ID {q_id}: {question_text[:40]}...")

def main():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = init_db()
    total_pages = int(os.environ.get("TOTAL_PAGES", "773"))
    chunk_size = 5
    print(f"Totale pagine configurate: {total_pages}")
    for i in range(1, total_pages + 1, chunk_size):
        last = min(i + chunk_size - 1, total_pages)
        print(f"--- Elaborazione Chunk Pagine {i}-{last} ---")
        try:
            kwargs = {"first_page": i, "last_page": last, "dpi": 300}
            if POPPLER_BIN_PATH:
                kwargs["poppler_path"] = POPPLER_BIN_PATH
            images = convert_from_path(PDF_PATH, **kwargs)
            for idx, img_pil in enumerate(images):
                print(f"  > Elaborazione Pagina {i + idx}...")
                processed = preprocess_image(img_pil)
                for col_idx, col in enumerate(split_columns(processed, SPLIT_RATIO)):
                    blocks = find_horizontal_lines_and_crop(col)
                    print(f"    Colonna {col_idx + 1}: {len(blocks)} blocchi trovati.")
                    for block_img in blocks:
                        text = pytesseract.image_to_string(block_img, lang="ita", config="--psm 6")
                        parse_single_block(text, conn)
        except Exception as exc:
            print(f"Errore: {exc}")
    conn.close()
    print("Finito.")

if __name__ == "__main__":
    main()
