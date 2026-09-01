import sys
import os
from pathlib import Path

# Add the snrproject directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent / 'snrproject'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'snrproject.settings')

from django.core.management import execute_from_command_line

if __name__ == "__main__":
    execute_from_command_line(sys.argv)
