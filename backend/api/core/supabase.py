import os
from supabase import create_client, Client

# Initialize Supabase client
# This is useful for Storage, Auth management, or Realtime features
# For standard database operations, use the SQLAlchemy session in api.models.database

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None

if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    # Warn but don't crash if not configured (unless explicitly required)
    print("Warning: SUPABASE_URL or SUPABASE_KEY not set. Supabase client disabled.")

def get_supabase() -> Client:
    """Get the Supabase client instance"""
    return supabase
