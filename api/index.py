import sys
import os

# Ensure the root directory is on sys.path for Vercel Serverless Functions
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from aegis_recover.api.server import app
