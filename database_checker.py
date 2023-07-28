import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("SUPABASE_URL")
key =  os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)
response = supabase.table('bot_users').select("*").execute()
try:

    user_database_info = supabase.table('bot_users').select("*").eq("user_id" , "Kante").execute()
    count = user_database_info.data[0]['count']
    # data , counter = supabase.table
    count -= 1
    r   = supabase.table("bot_users").update({ "count":count}).eq("user_id" , "Kante").execute()
    print("Successfully created , " , r)

except supabase.exceptions.ClientError as error:

    print(error)

