-- Creación de la tabla departamentos en Redshift
CREATE TABLE IF NOT EXISTS departamentos (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    code VARCHAR(50),
    date_extracted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_generated TIMESTAMP
);
