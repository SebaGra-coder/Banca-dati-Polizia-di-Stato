# PHP / JavaScript quiz application

This is the PHP + JavaScript quiz application recovered from the project working copy and used as the hosted interface.

- `index.html`: mobile-friendly interface, question navigation, answer selection and result review.
- `data.php`: JSON endpoint that retrieves questions and answers from MySQL.

The database is populated separately by importing the generated SQL data. The API expects the `domande` and `risposte` tables.

## Configuration

Set `DB_HOST`, `DB_USER`, `DB_PASSWORD` and `DB_NAME` as server environment variables. The public source intentionally contains no production credentials. Do not expose a production database password in a committed file.

The endpoint limits the requested number of questions to 1–100 and uses prepared statements for query parameters.
