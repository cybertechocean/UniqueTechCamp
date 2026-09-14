"""
Passenger WSGI configuration for UniqueTechCamp (cPanel / CloudLinux Deployment).
Target Domain: uniquetechcamp.org
Document Root: /home2/genzcons/uniquetechcamp
"""

import os
import sys

# Ensure the project root directory is in sys.path
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

# Optional: Load environment variables from .env if python-dotenv is installed
try:
    from dotenv import load_dotenv
    env_path = os.path.join(PROJECT_DIR, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
except ImportError:
    pass

# Ensure PyMySQL acts as MySQLdb if mysqlclient is not natively compiled
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniquetechcamp.settings')

# Import and expose the WSGI application
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
