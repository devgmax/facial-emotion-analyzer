# ==============================================================================
# PROJETO: FACIAL EMOTION ANALYZER (DESKTOP)
# MÓDULO: Rastreamento, Classificação e Análise de Expressões em Tempo Real
# ==============================================================================

import tkinter as tk
from tkinter import Label, Button, Frame
import cv2
from PIL import Image, ImageTk
import mediapipe as mp
from deepface import DeepFace

# ==============================================================================
# CLASSE PRINCIPAL: GERENCIAMENTO DE INTERFACE E INTELIGÊNCIA ARTIFICIAL
# ==============================================================================
class FacialApp:
    def __init__(self, root):
        """
        Método construtor: Inicializa a janela do sistema, configura as 
        variáveis de controle e ativa os motores de Inteligência Artificial.
        """
        # --- Configurações da Janela Principal (Tkinter) ---
        self.root = root
        self.root.title("Facial Emotion Analyzer - Desktop")
        self.root.geometry("950x540")
        self.root.config(bg="#1e1e1e")      # Fundo escuro estilo moderno/Dark Mode
        self.root.resizable(False, False)   # Impede distorções no layout fixo

        # --- Inicialização da IA de Detecção Facial (MediaPipe) ---
        # model_selection=1: Otimizado para rostos localizados a até 5 metros da câmera
        # min_detection_confidence=0.5: Tolerância mínima de 50% de certeza para validar um rosto
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1, 
            min_detection_confidence=0.5
        )

        # --- Variáveis de Controle de Estado e Dados ---
        self.is_running = False    # Controla se a captura da webcam está ativa
        self.cap = None            # Objeto gerenciador da câmera física (OpenCV)
        self.tipo = "Aguardando..." # Guarda o resultado da classificação (Humano/Animal)
        self.emotion = "---"        # Guarda a expressão facial identificada pelo DeepFace

        # --- Construção dos Elementos Visuais ---
        self.setup_ui()

    # ==============================================================================
    # MÓDULO VISUAL: ESTRUTURAÇÃO DA INTERFACE GRÁFICA (UI)
    # ==============================================================================
    def setup_ui(self):
        """
        Desenha os painéis laterais, labels de texto e botões de comando do app.
        """
        # --- Painel Esquerdo: Tela de Exibição do Vídeo ---
        self.video_frame = Frame(self.root, bg="#000000", width=640, height=480)
        self.video_frame.place(x=20, y=30)
        
        # Elemento do Tkinter que receberá as matrizes de imagem convertidas
        self.label_video = Label(self.video_frame, bg="#000000")
        self.label_video.pack(fill=tk.BOTH, expand=True)

        # --- Painel Direito: Dashboard de Controles e Insights de IA ---
        self.control_frame = Frame(self.root, bg="#2d2d2d", width=250, height=480)
        self.control_frame.place(x=680, y=30)

        # Título da Seção de Controle
        title_label = Label(self.control_frame, text="Painel de IA", font=("Arial", 14, "bold"), fg="#ffffff", bg="#2d2d2d")
        title_label.pack(pady=20)

        # Label de Saída: Classificação de Espécie
        self.lbl_tipo = Label(self.control_frame, text="Tipo: ---", font=("Arial", 11, "bold"), fg="#00ffcc", bg="#2d2d2d")
        self.lbl_tipo.pack(anchor="w", padx=20, pady=10)

        # Label de Saída: Expressão Facial
        self.lbl_emocao = Label(self.control_frame, text="Emoção: ---", font=("Arial", 11, "bold"), fg="#ff5555", bg="#2d2d2d")
        self.lbl_emocao.pack(anchor="w", padx=20, pady=10)

        # --- Botões de Ação ---
        # Botão Iniciar: Gatilho para capturar fluxo de vídeo
        self.btn_iniciar = Button(self.control_frame, text="Iniciar Câmera", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", width=18, command=self.iniciar_camera)
        self.btn_iniciar.pack(pady=25)

        # Botão Parar: Congela o fluxo de vídeo e desconecta o hardware com segurança
        self.btn_parar = Button(self.control_frame, text="Parar Câmera", font=("Arial", 10, "bold"), bg="#f44336", fg="white", width=18, command=self.parar_camera)
        self.btn_parar.pack(pady=5)

        # Botão Sair: Fecha a janela principal do sistema
        self.btn_sair = Button(self.control_frame, text="Sair do App", font=("Arial", 10, "bold"), bg="#555555", fg="white", width=18, command=self.root.quit)
        self.btn_sair.pack(pady=35)

    # ==============================================================================
    # MÓDULO DE HARDWARE: GERENCIAMENTO DE ENTRADA DA WEBCAM
    # ==============================================================================
    def iniciar_camera(self):
        """
        Conecta com o hardware da câmera padrão e inicia o laço de captura contínua.
        """
        if not self.is_running:
            self.cap = cv2.VideoCapture(0)  # Abre o canal da webcam nativa (index 0)
            self.is_running = True
            self.atualizar_frame()          # Dispara o gatilho de processamento em tempo real

    def parar_camera(self):
        """
        Libera o hardware da câmera física eliminando riscos de deadlocks ou travamento de periféricos.
        """
        if self.is_running:
            self.is_running = False
            if self.cap:
                self.cap.release()          # Desconecta o driver da câmera
            
            # Limpa os elementos visuais da tela reiniciando o estado do painel
            self.label_video.config(image='')
            self.lbl_tipo.config(text="Tipo: ---")
            self.lbl_emocao.config(text="Emoção: ---")

    # ==============================================================================
    # PIPELINE DE INTELIGÊNCIA ARTIFICIAL: PROCESSAMENTO, VISÃO E DEEP LEARNING
    # ==============================================================================
    def atualizar_frame(self):
        """
        Captura o frame atual, roda os modelos de Deep Learning para detecção facial 
        e classificação de emoções, renderiza os gráficos e atualiza a interface.
        """
        if self.is_running and self.cap and self.cap.isOpened():
            sucesso, frame = self.cap.read()
            if sucesso:
                # --- Preparação Inicial da Imagem ---
                frame = cv2.flip(frame, 1)                      # Espelha o vídeo para experiência natural
                img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # OpenCV usa BGR; MediaPipe exige RGB
                
                # Executa o modelo de localização do MediaPipe
                results = self.face_detection.process(img_rgb)

                # --- Fluxo se um Rosto for Detectado ---
                if results.detections:
                    for detection in results.detections:
                        # Extrai a caixa de coordenadas relativas (%) geradas pela IA
                        bboxC = detection.location_data.relative_bounding_box
                        h, w, c = frame.shape
                        
                        # Converte frações percentuais em pixels inteiros absolutos da imagem
                        x, y, w_box, h_box = int(bboxC.xmin * w), int(bboxC.ymin * h), \
                                             int(bboxC.width * w), int(bboxC.height * h)
                        
                        # Renderiza o retângulo delimitador (Bounding Box) em verde
                        cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), (0, 255, 0), 2)
                        self.tipo = "Humano"
                        
                        # --- Análise de Sentimentos usando Redes Neurais Convolucionais ---
                        try:
                            # Recorta estritamente a região do rosto para poupar processamento
                            rosto_crop = frame[y:y+h_box, x:x+w_box]
                            
                            # Roda o algoritmo DeepFace analisando os pesos de expressões
                            analise = DeepFace.analyze(rosto_crop, actions=['emotion'], enforce_detection=False)
                            self.emotion = analise[0]['dominant_emotion']
                        except:
                            # Previne crash caso a matriz de corte falhe nas bordas do vídeo
                            self.emotion = "Indeterminado"
                
                # --- Fluxo se nenhum Rosto Humano for Mapeado ---
                else:
                    self.tipo = "Animal ou Objeto"
                    self.emotion = "---"

                # --- Sincronização e Atualização da Interface Gráfica ---
                self.lbl_tipo.config(text=f"Tipo: {self.tipo}")
                self.lbl_emocao.config(text=f"Emoção: {self.emotion}")

                # Converte a matriz de cores do OpenCV para objetos compatíveis com a engine do Tkinter
                img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                img_pil = img_pil.resize((640, 480))
                img_tk = ImageTk.PhotoImage(image=img_pil)

                # Aloca os dados em memória RAM para exibição fluida
                self.label_video.imgtk = img_tk
                self.label_video.config(image=img_tk)

            # Agenda recursivamente a execução do método daqui a 15 milissegundos (~60 FPS teóricos)
            self.root.after(15, self.atualizar_frame)

# ==============================================================================
# BLOCO DE EXECUÇÃO DO APLICATIVO
# ==============================================================================
if __name__ == "__main__":
    root = tk.Tk()             # Instancia o motor de janelas do sistema operacional
    app = FacialApp(root)       # Constrói o aplicativo de IA
    root.mainloop()            # Mantém o processo em execução escutando eventos do usuário