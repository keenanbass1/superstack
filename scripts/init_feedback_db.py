#!/usr/bin/env python3
"""
Initialize the feedback database for DSP context module optimization.
This script creates the necessary database tables if they don't exist.
"""

import os
import sqlite3
import argparse
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("init_feedback_db")

def create_database(db_path):
    """Create the feedback database and required tables."""
    # Ensure directory exists
    db_dir = os.path.dirname(db_path)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        logger.info(f"Created directory: {db_dir}")
    
    # Connect to database (creates if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create module_feedback table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS module_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        module_name TEXT NOT NULL,
        model TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        feedback_type TEXT NOT NULL,
        message TEXT,
        source TEXT,
        effectiveness REAL
    )
    ''')
    
    # Create optimization_results table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS optimization_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        module_name TEXT NOT NULL,
        target_model TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        original_tokens INTEGER,
        optimized_tokens INTEGER,
        token_reduction REAL,
        improvement_score REAL,
        applied BOOLEAN DEFAULT FALSE
    )
    ''')
    
    # Create indices for faster queries
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_module_name ON module_feedback (module_name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_module_opt ON optimization_results (module_name)')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    logger.info(f"Database initialized at {db_path}")

def main():
    parser = argparse.ArgumentParser(description="Initialize the feedback database for DSP context module optimization.")
    parser.add_argument("--db-path", type=str, default="data/context_feedback.db",
                        help="Path to the SQLite database file (default: data/context_feedback.db)")
    
    args = parser.parse_args()
    db_path = args.db_path
    
    try:
        create_database(db_path)
        logger.info("Database initialization completed successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 