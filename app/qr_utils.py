import cv2
import numpy as np

class QRCodeScanner:
    @staticmethod
    def read_qr_from_image(image, database_manager):
        """
        Read QR code from an image and match against database
        """
        detector = cv2.QRCodeDetector()
        
        # Handle image input (can be file path or numpy array)
        if isinstance(image, str):
            img = cv2.imread(image)
        else:
            img = image

        if img is None:
            return "Error: Unable to load the image."

        data, _, _ = detector.detectAndDecode(img)
        
        if data:
            # Query database to match QR code data
            result = database_manager.execute_query(
                "SELECT name FROM user WHERE qr_data = %s", 
                (data,)
            )
            
            if result and len(result) > 0:
                return f"User '{result[0]['name']}' is present!"
            else:
                return "No match found in the database."
        else:
            return "No QR Code detected in the image."