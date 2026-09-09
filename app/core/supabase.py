from supabase import create_client, Client, ClientOptions
from app.core.config import settings

custom_options = ClientOptions(
    auto_refresh_token=False, 
    persist_session=False      
)

supabase: Client = create_client(
    supabase_url=settings.SUPABASE_URL,
    supabase_key=settings.SUPABASE_KEY,
    options=custom_options
)

supabase_admin: Client = create_client(
    supabase_url=settings.SUPABASE_URL,
    supabase_key=settings.SUPABASE_KEY,
    options=custom_options
)