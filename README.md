# 🤖 Facial Emotion Analyzer

> Um analisador de emoções faciais em tempo real utilizando Visão Computacional e Inteligência Artificial, desenvolvido em Python.

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Face%20Detection-FF6F00?style=for-the-badge)
![DeepFace](https://img.shields.io/badge/DeepFace-Emotion%20Recognition-00C853?style=for-the-badge)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Deep%20Learning-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

---

## 📖 Sobre o Projeto

O **Facial Emotion Analyzer** é uma aplicação desktop desenvolvida em Python que utiliza técnicas de **Visão Computacional** e **Deep Learning** para detectar rostos e identificar emoções em tempo real através da webcam.

A arquitetura foi projetada para oferecer uma experiência fluida, utilizando processamento assíncrono e uma interface gráfica nativa, reduzindo travamentos e garantindo estabilidade mesmo durante análises contínuas.

O sistema combina:

- 🎯 **MediaPipe** para detecção facial de alta velocidade;
- 🧠 **DeepFace** para classificação emocional baseada em Redes Neurais Convolucionais (CNNs);
- 📷 **OpenCV** para captura e manipulação dos frames;
- 🖥️ **Tkinter** para uma interface desktop simples e eficiente.

---

# ✨ Funcionalidades

- ✅ Detecção facial em tempo real
- ✅ Reconhecimento automático de emoções
- ✅ Interface gráfica em Dark Mode
- ✅ Controle completo da webcam
- ✅ Pausar captura
- ✅ Encerrar câmera com segurança
- ✅ Tratamento de exceções
- ✅ Compatível com CPU
- ✅ Suporte a aceleração por GPU (quando disponível)

---

# 🎯 Emoções Detectadas

O modelo consegue identificar emoções como:

|---------------|-----------------|
| 😀 Feliz | `happy` |
| 😐 Neutro | `neutral` |
| 😢 Triste | `sad` |
| 😠 Raiva | `angry` |
| 😨 Medo | `fear` |
| 😮 Surpreso | `surprise` |
| 🤢 Nojo | `disgust` |

---

# 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade |
|------------|------------|
| Python 3.12+ | Linguagem principal |
| OpenCV | Captura e processamento de imagem |
| MediaPipe | Detecção facial |
| DeepFace | Reconhecimento emocional |
| TensorFlow / Keras | Inferência da IA |
| Tkinter | Interface Desktop |
| Pillow (PIL) | Conversão e renderização de imagens |

---

# 🏗️ Arquitetura

```
                Webcam
                   │
                   ▼
             OpenCV (Frames)
                   │
                   ▼
       MediaPipe Face Detection
                   │
                   ▼
      Recorte da Região Facial
                   │
                   ▼
             DeepFace CNN
                   │
                   ▼
        Predição da Emoção
                   │
                   ▼
      Interface Tkinter (UI)
```

---

# 📂 Estrutura do Projeto

```
facial-emotion-analyzer/
│
├── facial_analyzer.py
├── requirements.txt
├── .gitignore
├── README.md
└── venv/
```

---

# 🚀 Instalação

## 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/facial-emotion-analyzer.git

cd facial-emotion-analyzer
```

---

## 2. Crie um ambiente virtual

### Windows

```bash
python -m venv venv
```

### Ativação (Prompt)

```bash
venv\Scripts\activate
```

### Ativação (PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 3. Atualize o pip

```bash
python -m pip install --upgrade pip
```

---

## 4. Instale o runtime do Visual C++

Necessário para o TensorFlow funcionar corretamente no Windows.

```bash
pip install msvc-runtime
```

---

## 5. Instale as dependências

```bash
pip install -r requirements.txt
```

---

# ▶️ Executando

```bash
python facial_analyzer.py
```

Na primeira execução o **DeepFace** fará automaticamente o download dos modelos neurais (~200 MB).

Esse processo acontece apenas uma vez.

---

# ⚙️ Dependências

Exemplo de `requirements.txt`

```txt
opencv-python
mediapipe
deepface
tensorflow
numpy
Pillow
msvc-runtime
```

---

# 💻 Build para Windows (.exe)

Para gerar um executável standalone utilizando o **PyInstaller**:

```bash
pyinstaller ^
--onefile ^
--noconsole ^
--collect-all mediapipe ^
--collect-all deepface ^
facial_analyzer.py
```

Após a compilação:

```
dist/
    facial_analyzer.exe
```

---

# 🧠 Como Funciona

1. A webcam captura os frames em tempo real.
2. O OpenCV processa as imagens.
3. O MediaPipe detecta a posição do rosto.
4. A região facial é recortada.
5. O DeepFace realiza a inferência usando uma CNN treinada.
6. A emoção dominante é exibida instantaneamente na interface.

---

# 📈 Possíveis Melhorias Futuras

- Reconhecimento de múltiplos rostos
- Histórico de emoções
- Dashboard estatístico
- Exportação para CSV
- API REST
- Reconhecimento por vídeo gravado
- Captura de screenshots automáticas
- Gráficos em tempo real
- Banco de dados SQLite
- Integração com PostgreSQL
- Dashboard Web

---

# 📸 Demonstração

```
📷 Webcam

😀 Emotion:
Happy

Confidence:
98.37%

Face Detected:
Yes
```

---

# 📚 Aprendizados

Durante o desenvolvimento deste projeto foram explorados conceitos como:

- Visão Computacional
- Inteligência Artificial
- Redes Neurais Convolucionais
- Processamento de Imagens
- Inferência em Tempo Real
- Arquitetura Desktop
- Tratamento de Threads
- Gerenciamento de Recursos
- Ambientes Virtuais
- Empacotamento de aplicações Python

---

# 🤝 Contribuição

Contribuições são bem-vindas!

Caso tenha sugestões de melhorias:

1. Faça um Fork
2. Crie uma Branch

```bash
git checkout -b feature/nova-feature
```

3. Faça seus commits

```bash
git commit -m "feat: nova funcionalidade"
```

4. Envie para sua branch

```bash
git push origin feature/nova-feature
```

5. Abra um Pull Request 🚀

---

# 👨‍💻 Autor

**Gabriel Max**

Desenvolvedor Full Stack com foco em Python, Automações, Inteligência Artificial e Computação em Nuvem.

- 💼 LinkedIn: *https://www.linkedin.com/in/devgmax/*
- 🐙 GitHub: https://github.com/devgmax

---

# ⭐ Apoie o Projeto

Se este projeto foi útil para você, deixe uma ⭐ no repositório.

Isso ajuda bastante na divulgação e incentiva o desenvolvimento de novos projetos.

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License**.

Sinta-se livre para estudar, modificar e utilizar o código em seus próprios projetos.