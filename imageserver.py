from flask import Flask, request, send_from_directory, render_template
from sql import load_db
import logging
import os


__all__ = ['create_app']

def load_config(app):
    app.config.from_object(__name__)
    app.config.from_object('default_settings')
    
def init_log(app):
    logging.basicConfig(filename=app.config['IMAGESERVER_LOG_FILE'], level=logging.DEBUG)
         
def create_app(name = __name__):
  
    app = Flask(__name__, static_path='/static')
    load_config(app) 
    init_log(app) 
    (db,Device) = load_db(app, 'device_table')                           
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def send_file(path):
        isONIESerial = request.headers.get("ONIE-SERIAL-NUMBER");
        isOnieInstall = request.headers.get("ONIE-OPERATION");
        logging.info("Request header: {}".format(request.headers))
        
         
        if(isONIESerial and isOnieInstall.lower() == 'os-install'.lower()):
            logging.info('{}:Original ONIE request path:{}.'.format(isONIESerial,request.path))
            
            try:
                device = Device.query.filter(Device.onie_id == isONIESerial).first()
                if device:
                    logging.info('{}:Updated ONIE request path:{}'.format(isONIESerial,device.image_name))
                    path = device.image_name
                else:
                    logging.warning('{}:No record found in db, proceed with original request: {}'.format(isONIESerial,request.path))
            except Exception as error:
                logging.error(error)
                pass 
            
            return send_from_directory(app.config['IMAGE_FOLDER'],path, as_attachment=True)
        
        return ("Sorry... We are only accepting requests from ONIE switches!", 404)
    
    return app
