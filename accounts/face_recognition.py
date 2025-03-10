import os
import cv2
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class FaceRecognition:
    def __init__(self, known_faces_dir='student image'):
        """
        Initialize face recognition system
        :param known_faces_dir: Directory to store known face images
        """
        self.known_faces_dir = os.path.join(settings.MEDIA_ROOT, known_faces_dir)
        os.makedirs(self.known_faces_dir, exist_ok=True)
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

    def detect_and_crop_face(self, image_path):
        """
        Detect and crop face from an image
        :param image_path: Path to the input image
        :return: Cropped face image or None
        """
        img = cv2.imread(image_path)
        if img is None:
            return None
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(30, 30)
        )
        if len(faces) == 0:
            return None
        (x, y, w, h) = faces[0]
        face_crop = gray[y:y+h, x:x+w]
        face_crop_resized = cv2.resize(face_crop, (100, 100))   
        return face_crop_resized


    def compare_faces(self, face1, face2):
        """
        Compare two face images using template matching
        :param face1: First face image
        :param face2: Second face image
        :return: Similarity score
        """
        face1_norm = cv2.normalize(face1, None, 0, 255, cv2.NORM_MINMAX)
        face2_norm = cv2.normalize(face2, None, 0, 255, cv2.NORM_MINMAX)        
        result = cv2.matchTemplate(face1_norm, face2_norm, cv2.TM_CCOEFF_NORMED)
        similarity = result[0][0]      
        return similarity


    def register_face(self, username, image_path):
        """
        Register a user's face
        :param username: Username to associate with the face
        :param image_path: Path to the user's face image
        :return: Boolean indicating success
        """
        # Detect and crop face
        face = self.detect_and_crop_face(image_path)
        if face is None:
            return False
        
        # Save the face image
        face_filename = f"{username}_face.jpg"
        face_save_path = os.path.join(self.known_faces_dir, face_filename)
        cv2.imwrite(face_save_path, face)
        
        return True

    def authenticate_by_face(self, image_path):
        """
        Authenticate a user by face
        :param image_path: Path to the input image
        :return: Username if authenticated, None otherwise
        """
        # Detect and crop input face
        input_face = self.detect_and_crop_face(image_path)
        if input_face is None:
            return None

        # Store potential matches
        matches = []

        # Check against all known faces
        for filename in os.listdir(self.known_faces_dir):
            # Skip any non-image files
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                continue

            try:
                known_face_path = os.path.join(self.known_faces_dir, filename)
                known_face = self.detect_and_crop_face(known_face_path)
                
                if known_face is not None:
                    # Compare faces
                    similarity = self.compare_faces(input_face, known_face)
                    print(f"Comparing with {filename}: Similarity = {similarity}")

                    # Adjust threshold as needed
                    if similarity > 0.4:
                        # Extract username from filename
                        username = filename.split('_')[0]
                        matches.append((username, similarity))

            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue

        # If matches found, return the match with highest similarity
        if matches:
            # Sort matches by similarity in descending order
            matches.sort(key=lambda x: x[1], reverse=True)
            print(f"Best match: {matches[0][0]} with similarity {matches[0][1]}")
            return matches[0][0]

        return None