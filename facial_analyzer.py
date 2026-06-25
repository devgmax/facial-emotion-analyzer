import cv2
import mediapipe as mp
from deepface import DeepFace
import time

# -- CONFIGURAÇÕES E INICIALIZAÇÃO --
""" Inicia o MediaPipe para detecção de rostos."""
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

# --- 2. CLASSE DA IA (O CÉREBRO) ---
class FacialAnalyzer:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.emotion = "Analisando..."
        self.tipo = "Desconhecido"