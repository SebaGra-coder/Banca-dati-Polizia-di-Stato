# PHP / JavaScript quiz application

This folder documents the PHP + JavaScript application recovered from the project working copy and used as the hosted quiz interface.

## Components

- `index.html`: responsive quiz interface built with HTML, Bootstrap 5 and JavaScript.
- `data.php`: JSON endpoint that reads questions and answers from MySQL.

The application expects the MySQL tables `domande` and `risposte` described in [the architecture notes](../docs/architecture.md). Data is imported separately into the hosted MySQL database.

## Configuration

Set database connection values in server-side configuration or environment variables. Do not put production credentials in PHP source files or commit them to Git.

The original recovered PHP file contained hard-coded connection settings; those values must not be copied into a public repository. The deployable files should be reviewed and configured before publishing or deploying.
