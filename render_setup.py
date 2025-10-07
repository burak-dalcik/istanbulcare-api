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
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
        
        # Run create_sample_data.py directly
        import subprocess
        result = subprocess.run([sys.executable, "create_sample_data.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Sample data created successfully!")
            print(result.stdout)
        else:
            print(f"Sample data creation failed: {result.stderr}")
        
    except Exception as e:
        print(f"Setup error: {e}")
        import traceback
        traceback.print_exc()
        # Don't fail deployment if sample data creation fails
        pass

if __name__ == "__main__":
    setup_database()
