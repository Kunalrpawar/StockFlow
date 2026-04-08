#!/usr/bin/env python
"""
Database initialization and management utility.
Run this script to initialize the database, apply migrations, and seed sample data.
"""

import os
from app import create_app
from app.extensions import db
from app.seed import seed_sample_data


def init_db():
    """Initialize the database."""
    app = create_app()

    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")


def seed_db():
    """Seed the database with sample data."""
    app = create_app()

    with app.app_context():
        print("Seeding sample data...")
        seed_sample_data()
        print("Sample data seeded successfully!")


def reset_db():
    """Reset the database (drop all tables and recreate)."""
    app = create_app()

    with app.app_context():
        print("WARNING: This will delete all data!")
        confirm = input("Type 'yes' to confirm: ")
        if confirm.lower() == "yes":
            print("Dropping all tables...")
            db.drop_all()
            print("Creating tables...")
            db.create_all()
            print("Database reset successfully!")
        else:
            print("Cancelled.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python manage.py [init|seed|reset]")
        print("\nCommands:")
        print("  init   - Create database tables")
        print("  seed   - Load sample data")
        print("  reset  - Drop and recreate all tables")
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        init_db()
    elif command == "seed":
        seed_db()
    elif command == "reset":
        reset_db()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
