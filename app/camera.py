import cv2

class VideoCamera:
    def __init__(self, camera_index=0):
        self.video = cv2.VideoCapture(camera_index)
        self.is_scanning = False
        self.last_scan_result = None

    def __del__(self):
        if self.video:
            self.video.release()

    def get_frame(self, qr_scanner=None, database_manager=None):
        success, image = self.video.read()
        
        if not success:
            return None

        # Optional: QR Code scanning during streaming
        if self.is_scanning and qr_scanner and database_manager:
            result = qr_scanner.read_qr_from_image(image, database_manager)
            if result != "No QR Code detected in the image.":
                self.is_scanning = False
                self.last_scan_result = result

        # Convert image to JPEG for streaming
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def start_scanning(self):
        self.is_scanning = True
        self.last_scan_result = None

    def stop_scanning(self):
        self.is_scanning = False