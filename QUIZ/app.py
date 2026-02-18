from flask import Flask, render_template, request, g
import mysql.connector
import os
import random

app = Flask(__name__)

# Configurazione MySQL Altervista
# Nota: Su Altervista l'host è quasi sempre 'localhost'
MYSQL_CONFIG = {
    'host': 'localhosst',
    'user': 'giuliam', # Es: 'my_nomeutente'
    'password': '',        # Spesso vuota se configurata così su Altervista
    'database': 'my_giuliam',    # Es: 'my_nomeutente'
    'raise_on_warnings': True
}

def get_db():
    """Connessione a MySQL con cursore a dizionario per ogni richiesta"""
    db = getattr(g, '_database', None)
    if db is None:
        # Creiamo la connessione a MySQL
        db = g._database = mysql.connector.connect(**MYSQL_CONFIG)
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Chiude la connessione MySQL alla fine della richiesta"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['POST'])
def start_quiz():
    try:
        num_domande = int(request.form.get('num_domande', 10))
    except ValueError:
        num_domande = 10
    
    argomento = request.form.get('argomento', 'random')
    conn = get_db()
    # Utilizziamo dictionary=True per emulare il comportamento di sqlite3.Row
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM domande"
    if argomento == 'costituzionale':
        query += " WHERE id BETWEEN 1 AND 1000"
    elif argomento == 'penale':
        query += " WHERE id BETWEEN 1001 AND 3000"
    elif argomento == 'processuale':
        query += " WHERE id BETWEEN 3001 AND 5000"

    # In MySQL si usa RAND() e il segnaposto %s
    query += " ORDER BY RAND() LIMIT %s"
    cursor.execute(query, (num_domande,))
    domande_rows = cursor.fetchall()

    quiz_data = []
    labels = ['A', 'B', 'C', 'D', 'E', 'F']

    for domanda in domande_rows:
        d_id = domanda['id']
        # Query con segnaposto %s
        cursor.execute('SELECT * FROM risposte WHERE domanda_id = %s', (d_id,))
        risposte_list = [dict(row) for row in cursor.fetchall()]
        random.shuffle(risposte_list)
        
        for i, r in enumerate(risposte_list):
            r['lettera_visuale'] = labels[i] if i < len(labels) else '?'
        
        quiz_data.append({
            'id': d_id,
            'testo': domanda['testo'],
            'risposte': risposte_list
        })

    return render_template('quiz.html', domande=quiz_data, total_questions=len(quiz_data))

@app.route('/risultato', methods=['POST'])
def check_result():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    punteggio = 0
    totale = 0
    dettagli = []

    for key, value in request.form.items():
        if key.startswith('q_'):
            try:
                domanda_id = key.split('_')[1]
                risposta_scelta_id = value 
                
                tua_lettera = request.form.get(f'L_{risposta_scelta_id}', '?')

                # Query MySQL con segnaposto %s
                cursor.execute('SELECT id, testo FROM risposte WHERE domanda_id = %s AND corretta = 1', (domanda_id,))
                corretta_row = cursor.fetchone()
                id_corretta = corretta_row['id'] if corretta_row else None
                testo_corretto = corretta_row['testo'] if corretta_row else "N/D"

                corretta_lettera_visuale = request.form.get(f'L_{id_corretta}', '?')

                cursor.execute('SELECT testo FROM risposte WHERE id = %s', (risposta_scelta_id,))
                risposta_utente_row = cursor.fetchone()
                testo_utente = risposta_utente_row['testo'] if risposta_utente_row else "Nessuna risposta"

                cursor.execute('SELECT testo FROM domande WHERE id = %s', (domanda_id,))
                domanda_row = cursor.fetchone()
                domanda_text = domanda_row['testo'] if domanda_row else "Domanda non trovata"

                is_correct = False
                if id_corretta and int(risposta_scelta_id) == id_corretta:
                    punteggio += 1
                    is_correct = True
                
                d_id_int = int(domanda_id)
                if 1 <= d_id_int <= 1000:
                    categoria = "Diritto Costituzionale"
                elif 1001 <= d_id_int <= 3000:
                    categoria = "Diritto Penale"
                elif 3001 <= d_id_int <= 5000:
                    categoria = "Diritto Processuale Penale"
                else:
                    categoria = "Altro"

                dettagli.append({
                    'domanda': domanda_text,
                    'categoria': categoria,
                    'tua_lettera': tua_lettera,
                    'tua_risposta': testo_utente,
                    'corretta_lettera': corretta_lettera_visuale,
                    'corretta_testo': testo_corretto,
                    'esito': is_correct
                })
                totale += 1
            except Exception as e:
                print(f"Errore: {e}")
                continue

    return render_template('result.html', punteggio=punteggio, totale=totale, dettagli=dettagli)

if __name__ == '__main__':
    # Nota: Su Altervista l'app non viene lanciata con app.run() 
    # ma gestita tramite il loro pannello/WSGI. Per test locale:
    app.run(debug=True)