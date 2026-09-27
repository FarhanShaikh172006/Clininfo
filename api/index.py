import sys
import os

# Add the project root to sys.path so modules like 'routes' and 'services' can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app