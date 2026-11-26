import sqlite3
import os

DB_PATH = os.environ.get("OUTPUT_DB", "data/banca_dati_blocchi.db")

def main():
    if not os.path.exists(DB_PATH):
        print(f"Errore: database non trovato: {os.path.abspath(DB_PATH)}")
        return
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        print("Connessione al database stabilita.")
        print("Aggiornamento risposte con lettera 'A'...")
        cursor.execute("UPDATE risposte SET corretta = 1 WHERE lettera = 'A'")
        print(f" -> Impostate {cursor.rowcount} risposte 'A' come corrette.")
        cursor.execute("UPDATE risposte SET corretta = 0 WHERE lettera != 'A'")
        conn.commit()
        print("Modifiche salvate nel database con successo.")
    except sqlite3.Error as exc:
        print(f"Errore durante l'operazione SQL: {exc}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
