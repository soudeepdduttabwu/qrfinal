# app/routes.py
import os
import cv2
import numpy as np
from flask import Blueprint, request, jsonify, Response, render_template
from werkzeug.utils import secure_filename

routes = Blueprint('main', __name__)

class RouteHandler:
    def __init__(self, app_config, camera, qr_scanner, database_manager):
        self.config = app_config
        self.camera = camera
        self.qr_scanner = qr_scanner
        self.database = database_manager

    def setup_routes(self, blueprint):
        """
        Setup all routes for the application
        """
        blueprint.add_url_rule('/', 'home', self.home)
        blueprint.add_url_rule('/upload', 'upload', self.upload, methods=['POST'])
        blueprint.add_url_rule('/video_feed', 'video_feed', self.video_feed)
        blueprint.add_url_rule('/start_scan', 'start_scan', self.start_scan, methods=['POST'])
        blueprint.add_url_rule('/stop_scan', 'stop_scan', self.stop_scan, methods=['POST'])
        blueprint.add_url_rule('/scan_result', 'scan_result', self.scan_result)

    def home(self):
        return render_template('index.html')

    def upload(self):
        # Improved file upload handling
        if 'file' not in request.files and 'qr_image' not in request.files:
            return jsonify({'message': 'No file uploaded'}), 400

        file = request.files.get('file') or request.files.get('qr_image')
        
        if file.filename == '':
            return jsonify({'message': 'No file selected'}), 400

        # Secure filename and check extension
        filename = secure_filename(file.filename)
        if not self._allowed_file(filename):
            return jsonify({'message': 'Invalid file format'}), 400

        # Save and process file
        filepath = os.path.join(self.config.UPLOAD_FOLDER, filename)
        os.makedirs(self.config.UPLOAD_FOLDER, exist_ok=True)
        
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        result = self.qr_scanner.read_qr_from_image(img, self.database)
        return jsonify({'result': result})

    def video_feed(self):
        def generate():
            while True:
                frame = self.camera.get_frame(
                    self.qr_scanner, 
                    self.database
                )
                if frame is None:
                    break
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        return Response(generate(), 
                       mimetype='multipart/x-mixed-replace; boundary=frame')

    def start_scan(self):
        self.camera.start_scanning()
        return jsonify({'message': 'Scanning started'})

    def stop_scan(self):
        self.camera.stop_scanning()
        return jsonify({'message': 'Scanning stopped'})

    def scan_result(self):
        if self.camera.last_scan_result:
            return jsonify({
                'found': True, 
                'result': self.camera.last_scan_result
            })
        return jsonify({'found': False})

    def _allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.config.ALLOWED_EXTENSIONS 