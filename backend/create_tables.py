#!/usr/bin/env python3
"""
Database table creation script for MzeeChakula backend.
Run this to ensure all tables exist in the database.
"""
import sys
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from api.models import database, user, chat, food

    logger.info("Starting database table creation...")
    logger.info(f"Database URL: {database.SQLALCHEMY_DATABASE_URL.split('@')[0]}...")

    # Create tables in order (to respect foreign keys)
    logger.info("Creating user tables...")
    user.Base.metadata.create_all(bind=database.engine)
    logger.info("✓ User tables created")

    logger.info("Creating chat tables...")
    chat.Base.metadata.create_all(bind=database.engine)
    logger.info("✓ Chat tables created")

    logger.info("Creating food tables...")
    food.Base.metadata.create_all(bind=database.engine)
    logger.info("✓ Food tables created")

    logger.info("✓ All database tables created successfully!")

    # Verify tables exist
    from sqlalchemy import inspect
    inspector = inspect(database.engine)
    tables = inspector.get_table_names()
    logger.info(f"Tables in database: {tables}")

    sys.exit(0)

except Exception as e:
    logger.error(f"✗ Failed to create database tables: {e}")
    import traceback
    logger.error(traceback.format_exc())
    sys.exit(1)
