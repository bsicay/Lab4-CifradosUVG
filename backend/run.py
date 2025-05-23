import os
import sys
from backend import create_app

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)