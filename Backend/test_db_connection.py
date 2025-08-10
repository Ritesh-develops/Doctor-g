#!/usr/bin/env python3
import asyncio
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from app.db.session import sessionmanager
from sqlalchemy import text

async def test_connection():
    """Test database connection"""
    print(f"Testing connection to: {settings.DATABASE_URL}")
    
    try:
        # Initialize connection
        sessionmanager.init(settings.DATABASE_URL)
        
        # Test basic connection
        async with sessionmanager.session() as session:
            result = await session.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            print(f"✅ Database connection successful! Test query result: {row[0]}")
            
            # Test user creation table
            result = await session.execute(text("SELECT current_user"))
            user = result.fetchone()
            print(f"✅ Connected as user: {user[0]}")
            
            # Test if we can create a simple table
            await session.execute(text("""
                CREATE TABLE IF NOT EXISTS test_table (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50)
                )
            """))
            await session.commit()
            print("✅ Can create tables")
            
            # Clean up
            await session.execute(text("DROP TABLE IF EXISTS test_table"))
            await session.commit()
            print("✅ Database permissions working correctly")
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print(f"Connection string: {settings.DATABASE_URL}")
        return False
    finally:
        await sessionmanager.close()
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_connection())
    if success:
        print("\n🎉 Database is ready for user registration!")
    else:
        print("\n💥 Fix database connection before proceeding")