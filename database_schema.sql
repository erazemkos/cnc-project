-- SQL schema for the CNC Machining database

-- Create a table for storing machine information
CREATE TABLE IF NOT EXISTS machines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_number TEXT NOT NULL
);

-- Create a table for storing process information
CREATE TABLE IF NOT EXISTS processes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    process_number TEXT NOT NULL
);

-- Create a table for storing labels (good or bad)
CREATE TABLE IF NOT EXISTS labels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT NOT NULL CHECK (label IN ('good', 'bad'))
);

-- Create a table for storing spindle load data
CREATE TABLE IF NOT EXISTS spindle_load_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_id INTEGER NOT NULL,
    process_id INTEGER NOT NULL,
    label_id INTEGER NOT NULL,
    filename TEXT NOT NULL,
    data BLOB,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (machine_id) REFERENCES machines(id),
    FOREIGN KEY (process_id) REFERENCES processes(id),
    FOREIGN KEY (label_id) REFERENCES labels(id)
);

-- Indexes to improve query performance
CREATE INDEX IF NOT EXISTS idx_machine ON spindle_load_data (machine_id);
CREATE INDEX IF NOT EXISTS idx_process ON spindle_load_data (process_id);
CREATE INDEX IF NOT EXISTS idx_label ON spindle_load_data (label_id);
