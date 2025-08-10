#!/usr/bin/env python3
import asyncio
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.session import sessionmanager
from app.db.models import Base, User
from app.core.config import settings
from app.core.security import SecurityManager

async def create_tables():
    """Create all database tables"""
    print(f"Creating tables for: {settings.DATABASE_URL}")
    
    sessionmanager.init(settings.DATABASE_URL)
    
    try:
        async with sessionmanager._engine.begin() as conn:
            print("Dropping existing tables...")
            await conn.run_sync(Base.metadata.drop_all)
            
            print("Creating new tables...")
            await conn.run_sync(Base.metadata.create_all)
        
        print("✅ Database tables created successfully!")
        
        # Create a test user
        await create_test_user()
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await sessionmanager.close()

async def create_test_user():
    """Create a test user for development"""
    async with sessionmanager.session() as db:
        try:
            # Check if test user already exists
            from sqlalchemy import select
            stmt = select(User).where(User.email == "test@doctorg.com")
            result = await db.execute(stmt)
            existing_user = result.scalar_one_or_none()
            
            if not existing_user:
                test_user = User(
                    email="test@doctorg.com",
                    hashed_password=SecurityManager.get_password_hash("test123"),
                    full_name="Test User",
                    is_active=True,
                    is_verified=True
                )
                
                db.add(test_user)
                await db.commit()
                print("✅ Test user created: test@doctorg.com / test123")
            else:
                print("ℹ️ Test user already exists")
                
        except Exception as e:
            print(f"❌ Error creating test user: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(create_tables())