# ==============================================================================
# PROJETO: FACIAL EMOTION ANALYZER (DESKTOP)
# MÓDULO: Rastreamento, Classificação e Análise de Expressões em Tempo Real
# ==============================================================================

import os
# Oculta avisos informativos e de warning do TensorFlow para manter o console limpo
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

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
        self.root.title("Facial Emotion Analyzer - Enterprise Edition")
        self.root.geometry("1000x560")
        self.root.config(bg="#121212")      # Fundo AMOLED/Pitch Black moderno
        self.root.resizable(False, False)   # Mantém a integridade do design fixo

        # --- Dicionário de Tradução das Emoções (Inglês -> PT-BR) ---
        self.tradutor_emocoes = {
            "angry": "Com Raiva",
            "disgust": "Nojo",
            "fear": "Com Medo",
            "happy": "Feliz",
            "sad": "Triste",
            "surprise": "Surpreso(a)",
            "neutral": "Neutro(a)"
        }

        # --- Inicialização da IA de Detecção Facial (MediaPipe) ---
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1, 
            min_detection_confidence=0.5
        )

        # --- Variáveis de Controle de Estado e Dados ---
        self.is_running = False    
        self.cap = None            
        self.tipo = "Aguardando..." 
        self.emotion = "---"        

        # --- Construção dos Elementos Visuais Refinados ---
        self.setup_ui()

    # ==============================================================================
    # MÓDULO VISUAL: ESTRUTURAÇÃO DA INTERFACE GRÁFICA PREMIUM (UI)
    # ==============================================================================
    def setup_ui(self):
        """
        Desenha os painéis laterais modernos, tipografia hierárquica e botões interativos.
        """
        # --- 1. Painel Esquerdo: Tela de Exibição da Webcam (Estilo Card) ---
        # Criamos uma borda/moldura sutil em tom grafite ao redor do feed de vídeo
        self.video_border_frame = Frame(self.root, bg="#1e1e1e", padx=4, pady=4)
        self.video_border_frame.place(x=25, y=35, width=648, height=488)

        self.video_frame = Frame(self.video_border_frame, bg="#0a0a0a")
        self.video_frame.pack(fill=tk.BOTH, expand=True)
        
        # Label placeholder com mensagem elegante enquanto a câmera está desligada
        self.label_video = Label(
            self.video_frame, 
            text="CÂMERA DESCONECTADA\n\nClique em 'Iniciar Fluxo' para ativar a IA",
            font=("Segoe UI", 11),
            fg="#666666",
            bg="#0a0a0a"
        )
        self.label_video.pack(fill=tk.BOTH, expand=True)

        # --- 2. Painel Direito: Dashboard Gerencial de Insights ---
        self.control_frame = Frame(self.root, bg="#1e1e1e")
        self.control_frame.place(x=695, y=35, width=280, height=488)

        # Título Principal do Painel (Estilo Minimalista)
        title_label = Label(
            self.control_frame, 
            text="Métricas de Visão AI", 
            font=("Segoe UI", 14, "bold"), 
            fg="#ffffff", 
            bg="#1e1e1e"
        )
        title_label.pack(pady=(25, 30))

        # --- Container Interno de Dados (Cards de Telemetria) ---
        # Card Tipo
        tipo_card = Frame(self.control_frame, bg="#262626", padx=15, pady=10)
        tipo_card.pack(fill="x", padx=20, pady=5)
        
        lbl_tipo_title = Label(tipo_card, text="CLASSIFICAÇÃO", font=("Segoe UI", 8, "bold"), fg="#888888", bg="#262626")
        lbl_tipo_title.pack(anchor="w")
        
        self.lbl_tipo = Label(tipo_card, text="Aguardando...", font=("Segoe UI", 13, "bold"), fg="#00ffcc", bg="#262626")
        self.lbl_tipo.pack(anchor="w", pady=(2, 0))

        # Card Emoção
        emocao_card = Frame(self.control_frame, bg="#262626", padx=15, pady=10)
        emocao_card.pack(fill="x", padx=20, pady=10)
        
        lbl_emocao_title = Label(emocao_card, text="EXPRESSÃO FACIAL", font=("Segoe UI", 8, "bold"), fg="#888888", bg="#262626")
        lbl_emocao_title.pack(anchor="w")
        
        self.lbl_emocao = Label(emocao_card, text="---", font=("Segoe UI", 14, "bold"), fg="#ff5555", bg="#262626")
        self.lbl_emocao.pack(anchor="w", pady=(2, 0))

        # --- 3. Seção Inferior de Controle (Botões Modernizados) ---
        # Botão Iniciar (Verde Esmeralda)
        self.btn_iniciar = Button(
            self.control_frame, text="Iniciar Fluxo", font=("Segoe UI", 10, "bold"), 
            bg="#10b981", fg="white", activebackground="#059669", activeforeground="white",
            bd=0, cursor="hand2", width=22, height=2, command=self.iniciar_camera
        )
        self.btn_iniciar.pack(pady=(40, 8))
        self.configurar_hover(self.btn_iniciar, "#10b981", "#059669")

        # Botão Parar (Cinza Escuro/Discreto)
        self.btn_parar = Button(
            self.control_frame, text="Interromper Câmera", font=("Segoe UI", 10, "bold"), 
            bg="#374151", fg="#d1d5db", activebackground="#1f2937", activeforeground="white",
            bd=0, cursor="hand2", width=22, height=2, command=self.parar_camera
        )
        self.btn_parar.pack(pady=5)
        self.configurar_hover(self.btn_parar, "#374151", "#1f2937")

        # Botão Sair (Outline/Vermelho sutil no encerramento)
        self.btn_sair = Button(
            self.control_frame, text="Fechar Sistema", font=("Segoe UI", 9, "bold"), 
            bg="#1e1e1e", fg="#9ca3af", activebackground="#ef4444", activeforeground="white",
            bd=1, relief="solid", highlightthickness=0, cursor="hand2", width=24, height=2, command=self.root.quit
        )
        self.btn_sair.pack(pady=(45, 0))
        self.configurar_hover(self.btn_sair, "#1e1e1e", "#ef4444", fg_normal="#9ca3af", fg_hover="white")

    # ==============================================================================
    # HELPER DE DESIGN: EFEITOS DINÂMICOS DE HOVER (INTERATIVIDADE)
    # ==============================================================================
    def configurar_hover(self, botao, cor_normal, cor_hover, fg_normal="white", fg_hover="white"):
        """
        Adiciona listeners de eventos para mudar a cor dos botões ao passar o rato.
        """
        botao.bind("<Enter>", lambda e: botao.config(bg=cor_hover, fg=fg_hover))
        botao.bind("<Leave>", lambda e: botao.config(bg=cor_normal, fg=fg_normal))

    # ==============================================================================
    # MÓDULO DE HARDWARE: GERENCIAMENTO DE ENTRADA DA WEBCAM
    # ==============================================================================
    def iniciar_camera(self):
        if not self.is_running:
            self.cap = cv2.VideoCapture(0)  
            self.is_running = True
            self.label_video.config(text="") # Remove o texto de placeholder
            self.atualizar_frame()          

    def parar_camera(self):
        if self.is_running:
            self.is_running = False
            if self.cap:
                self.cap.release()          
            
            # Restaura o estado visual padrão de forma limpa
            self.label_video.config(image='', text="CÂMERA DESCONECTADA\n\nClique em 'Iniciar Fluxo' para ativar a IA")
            self.lbl_tipo.config(text="Aguardando...")
            self.lbl_emocao.config(text="---")

    # ==============================================================================
    # PIPELINE DE INTELIGÊNCIA ARTIFICIAL: PROCESSAMENTO, VISÃO E DEEP LEARNING
    # ==============================================================================
    def atualizar_frame(self):
        if self.is_running and self.cap and self.cap.isOpened():
            sucesso, frame = self.cap.read()
            if sucesso:
                frame = cv2.flip(frame, 1)                      
                img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
                results = self.face_detection.process(img_rgb)

                if results.detections:
                    for detection in results.detections:
                        bboxC = detection.location_data.relative_bounding_box
                        h, w, c = frame.shape
                        
                        x, y, w_box, h_box = int(bboxC.xmin * w), int(bboxC.ymin * h), \
                                             int(bboxC.width * w), int(bboxC.height * h)
                        
                        # Renderiza o retângulo delimitador com a cor esmeralda do tema (RGB: 16, 185, 129)
                        cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), (129, 185, 16), 2)
                        self.tipo = "Humano Mapeado"
                        
                        try:
                            rosto_crop = frame[y:y+h_box, x:x+w_box]
                            analise = DeepFace.analyze(rosto_crop, actions=['emotion'], enforce_detection=False)
                            emocao_en = analise[0]['dominant_emotion']
                            self.emotion = self.tradutor_emocoes.get(emocao_en, "Indeterminado")
                        except:
                            self.emotion = "Analisando..."
                else:
                    self.tipo = "Animal ou Objeto"
                    self.emotion = "---"

                # Sincronização em tempo real das métricas nos Cards
                self.lbl_tipo.config(text=self.tipo)
                self.lbl_emocao.config(text=self.emotion)

                # Conversão matricial otimizada para o ecossistema Tkinter
                img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                img_pil = img_pil.resize((640, 480))
                img_tk = ImageTk.PhotoImage(image=img_pil)

                self.label_video.imgtk = img_tk
                self.label_video.config(image=img_tk)

            self.root.after(15, self.atualizar_frame)

# ==============================================================================
# BLOCO DE EXECUÇÃO DO APLICATIVO
# ==============================================================================
if __name__ == "__main__":
    root = tk.Tk()             
    app = FacialApp(root)       
    root.mainloop()