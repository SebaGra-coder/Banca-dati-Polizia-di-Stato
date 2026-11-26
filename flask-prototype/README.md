# Flask prototype

Alternative Flask/MySQL implementation retained from the repository's earlier deployment experiment. The hosted quiz application described in the root README was the separate PHP/JavaScript implementation.

## Local setup

1. Create a virtual environment and install `requirements.txt`.
2. Set `DB_HOST`, `DB_USER`, `DB_PASSWORD` and `DB_NAME` in the environment.
3. Ensure the MySQL database contains the `domande` and `risposte` tables.
4. Run with a WSGI server. For local development only, the module includes Flask's development server.

Do not use Flask's debug server in production. This prototype is preserved for reference and is not presented as the hosted PHP/JavaScript application.
