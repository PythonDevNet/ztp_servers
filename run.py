import os
import sys

sys.path.append(os.path.dirname(__name__))

from imageapp import create_app
app = create_app(__name__)

if app.config['DEBUG']:
    app.debug = True

app.run(**app.config['IMAGE_WERKZEUG_OPTS'])
