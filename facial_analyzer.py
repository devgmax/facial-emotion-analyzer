import cv2
import mediapipe as mp
from deepface import DeepFace
import time

# -- CONFIGURAÇÕES E INICIALIZAÇÃO --
""" Inicia o MediaPipe para detecção de rostos."""
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

# -- CLASSE DA IA (O CÉREBRO) --
class FacialAnalyzer:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.emotion = "Analisando..."
        self.tipo = "Desconhecido"
    
    def processar_frame(self, frame):
        # Converte de BGR (OpenCV) para RGB (MediaPipe)
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(img_rgb)

        if results.detections:
            for detection in results.detections:
                # Desenha a caixa (Bounding Box)
                bboxC = detection.location_data.relative_bounding_box
                h, w, c = frame.shape
                x, y, w_box, h_box = int(bboxC.xmin * w), int(bboxC.ymin * h), \
                                     int(bboxC.width * w), int(bboxC.height * h)
                
                # Desenha o retângulo no rosto
                cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), (0, 255, 0), 2)
                
                # --- LÓGICA DE CLASSIFICAÇÃO (Humano/Animal/Emoção) ---
                # O MediaPipe detectou um rosto, logo é Humano
                self.tipo = "Humano"
                
                try:
                    # Recorta o rosto para analisar
                    rosto_crop = frame[y:y+h_box, x:x+w_box]
                    # Analisa emoção
                    analise = DeepFace.analyze(rosto_crop, actions=['emotion'], enforce_detection=False)
                    self.emotion = analise[0]['dominant_emotion']
                except:
                    self.emotion = "Indeterminado"
        else:
            self.tipo = "Animal ou Objeto"
            self.emotion = "---"

        return frame 
    
    def rodar(self):
        print("Iniciando sistema... Pressione 'q' para sair.")
        while True:
            sucesso, frame = self.cap.read()
            if not sucesso: break

            frame = cv2.flip(frame, 1)
            frame = self.processar_frame(frame)

            # Escreve os resultados na tela
            cv2.putText(frame, f"Tipo: {self.tipo}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            cv2.putText(frame, f"Emocao: {self.emotion}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow("Facial Emotion Analyzer - Open Source", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

# --- 3. BLOCO DE EXECUÇÃO ---
if __name__ == "__main__":
    analisador = FacialAnalyzer()
    analisador.rodar()        