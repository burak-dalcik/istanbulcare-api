#!/usr/bin/env python3
"""
Render deployment setup script
Creates database tables and sample data
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def setup_database():
    """Setup database and create sample data"""
    try:
        # Import after path setup
        from app.db.session import Base, engine
        from create_sample_data import create_sample_data
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
        
        # Create sample data
        create_sample_data()
        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Setup error: {e}")
        # Don't fail deployment if sample data creation fails
        pass

if __name__ == "__main__":
    setup_database()
