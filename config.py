import os

# Mode debug
DEBUG = os.environ.get("DEBUG", "true").lower() in ["true", "1"]

# Répertoires
INPUT_DIR = os.environ.get("INPUT_DIR", os.path.join(os.getcwd(), "input_data"))
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", os.path.join(os.getcwd(), "output"))

# Clés de paiement
STRIPE_API_KEY = os.environ.get("STRIPE_API_KEY", "your_stripe_api_key")
COINBASE_API_KEY = os.environ.get("COINBASE_API_KEY", "your_coinbase_api_key")

# Configuration Supabase (optionnel)
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

# Activation de l'IA FLAN-T5
USE_AI_COMMENTARY = os.environ.get("USE_AI_COMMENTARY", "false").lower() in ["true", "1"]
