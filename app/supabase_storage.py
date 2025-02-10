import os
from config import SUPABASE_URL, SUPABASE_KEY

def store_file_to_supabase(file_path):
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Identifiants Supabase non fournis, stockage ignoré.")
        return
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        bucket_name = "uploads"
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            file_data = f.read()
        response = supabase.storage.from_(bucket_name).upload(file_name, file_data)
        print(f"Fichier {file_name} stocké sur Supabase.")
    except Exception as e:
        print(f"Erreur lors du stockage sur Supabase : {e}")
