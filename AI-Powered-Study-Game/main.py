import sys
import os
import datetime
import PyPDF2
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QTextEdit, QComboBox, QStackedWidget, QMessageBox, QFileDialog, QFrame)
from PyQt6.QtCore import (Qt, QThread, pyqtSignal, QTimer, QUrl,
                          QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, QSize)
from PyQt6.QtGui import QFont, QCursor, QPixmap
from PyQt6.QtMultimedia import QSoundEffect
from ai_agent import EduAgent

# =====================================================================
# HOJA DE ESTILOS CSS (DISEÑO WEB)
# =====================================================================
STYLESHEET = """
QMainWindow {
    background-color: #0f172a;
}
QWidget {
    font-family: 'Ubuntu', 'Segoe UI', sans-serif;
    color: #f8fafc;
}
QFrame#Card {
    background-color: #1e293b;
    border-radius: 15px;
    border: 1px solid #334155;
}
QLabel#Title {
    font-size: 32px;
    font-weight: bold;
    color: #a855f7;
    margin-bottom: 5px;
}
QLabel#Subtitle {
    font-size: 14px;
    color: #94a3b8;
    margin-bottom: 20px;
}
QLabel#HudText {
    font-size: 16px;
    font-weight: bold;
}
QPushButton {
    background-color: #334155;
    color: white;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    font-weight: bold;
    border: none;
}
QPushButton:hover {
    background-color: #475569;
}
QPushButton#PrimaryBtn {
    background-color: #9333ea;
}
QPushButton#PrimaryBtn:hover {
    background-color: #7e22ce;
}
QPushButton#OptionBtn {
    background-color: #1e293b;
    border: 2px solid #334155;
    text-align: left;
    padding-left: 20px;
    font-size: 16px;
}
QPushButton#OptionBtn:hover {
    background-color: #9333ea;
    border: 2px solid #a855f7;
}
QTextEdit {
    background-color: #020617;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
    color: #e2e8f0;
}
QComboBox {
    background-color: #020617;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px;
    font-size: 14px;
    color: white;
}
QComboBox::drop-down {
    border: none;
}
"""

# =====================================================================
# HILO SECUNDARIO PARA LA IA (Evita que la ventana se congele)
# =====================================================================
class AIWorker(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, material, diff_name, num_q, language):
        super().__init__()
        self.agent = EduAgent()
        self.material = material
        self.diff_name = diff_name
        self.num_q = num_q
        self.language = language

    def run(self):
        try:
            questions = self.agent.generate_quiz(
                study_material=self.material,
                difficulty=self.diff_name,
                num_questions=self.num_q,
                language=self.language
            )
            self.finished.emit(questions)
        except Exception as e:
            self.error.emit(str(e))

# =====================================================================
# VENTANA PRINCIPAL DEL JUEGO
# =====================================================================
class StudyGameApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Study RPG - Desktop Edition")
        self.setMinimumSize(900, 700)
        self.setStyleSheet(STYLESHEET)

        # Variables lógicas
        self.questions = []
        self.current_index = 0
        self.score = 0
        self.lives = 3
        self.max_lives = 3
        self.time_elapsed = 0
        
        self.difficulty_settings = {
            "Fácil": {"q": 10, "lives": 3, "name": "Easy"},
            "Medio": {"q": 15, "lives": 4, "name": "Medium"},
            "Difícil": {"q": 20, "lives": 5, "name": "Hard"}
        }

        # Temporizador
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        # ---------------------------------------------------------------
        # MEJORA 1: Cargar efectos de sonido (QSoundEffect)
        # ---------------------------------------------------------------
        self.init_sounds()

        # Sistema de pantallas (Stack)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Inicializar pantallas
        self.init_menu_screen()
        self.init_loading_screen()
        self.init_game_screen()
        self.init_result_screen()

        self.stacked_widget.setCurrentIndex(0) # Iniciar en Menú

    # ===================================================================
    # MEJORA 1: EFECTOS DE SONIDO
    # ===================================================================
    def init_sounds(self):
        """Prepara 3 efectos de sonido. Si los .wav no existen, simplemente
        no suenan (no lanza error), así que es seguro usar rutas genéricas."""
        def make_effect(path):
            effect = QSoundEffect()
            effect.setSource(QUrl.fromLocalFile(path))
            effect.setVolume(0.7)
            return effect

        self.snd_correct = make_effect("sounds/hit.wav")     # Golpe crítico (acierto)
        self.snd_wrong = make_effect("sounds/damage.wav")    # Daño recibido (error)
        self.snd_end = make_effect("sounds/end.wav")         # Victoria / Game Over

    # --- PANTALLA 1: MENÚ ---
    def init_menu_screen(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        
        # --- TARJETA PRINCIPAL (CENTRO) ---
        card = QFrame()
        card.setObjectName("Card")
        card.setFixedSize(700, 550)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("AI STUDY RPG")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Sube tu archivo PDF y conviertelo en una batalla")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_file = QPushButton("BUSCAR ARCHIVO (PDF / TXT)")
        btn_file.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_file.clicked.connect(self.load_file)

        self.txt_material = QTextEdit()
        self.txt_material.setPlaceholderText("O pega directamente el texto o tema aqui...")

        # Opciones
        opts_layout = QHBoxLayout()
        
        diff_layout = QVBoxLayout()
        diff_layout.addWidget(QLabel("Dificultad:"))
        self.combo_diff = QComboBox()
        self.combo_diff.addItems(["Fácil", "Medio", "Difícil"])
        diff_layout.addWidget(self.combo_diff)
        
        lang_layout = QVBoxLayout()
        lang_layout.addWidget(QLabel("Idioma:"))
        self.combo_lang = QComboBox()
        self.combo_lang.addItems(["Español", "Inglés"])
        lang_layout.addWidget(self.combo_lang)

        opts_layout.addLayout(diff_layout)
        opts_layout.addLayout(lang_layout)

        btn_start = QPushButton("INICIAR PARTIDA")
        btn_start.setObjectName("PrimaryBtn")
        btn_start.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_start.clicked.connect(self.start_generation)

        # Ensamblar tarjeta principal
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(btn_file)
        card_layout.addWidget(self.txt_material)
        card_layout.addLayout(opts_layout)
        card_layout.addSpacing(20)
        card_layout.addWidget(btn_start)

        # --- SECCIÓN DEL CÓDIGO QR (ESQUINA INFERIOR DERECHA) ---
        qr_layout = QVBoxLayout()
        
        lbl_qr_text = QLabel("¡Escanea esto para ver algo genial! ")
        lbl_qr_text.setStyleSheet("color: #a855f7; font-size: 12px; font-weight: bold;")
        
        self.lbl_qr_img = QLabel("[QR de tu IG]")
        self.lbl_qr_img.setFixedSize(100, 100)
        self.lbl_qr_img.setStyleSheet("background-color: #1e293b; color: #64748b; font-size: 11px; border-radius: 8px; border: 2px dashed #475569;")
        self.lbl_qr_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # ==============================================================================
        # AQUI PUEDES AGREGAR TU IMAGEN DEL CÓDIGO QR DE INSTAGRAM:
        # Cuando descargues tu QR, descomenta estas dos líneas y pon el nombre del archivo
        # 
        qr_pixmap = QPixmap("igqr.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        self.lbl_qr_img.setPixmap(qr_pixmap)
        # ==============================================================================
        
        qr_layout.addWidget(lbl_qr_text, alignment=Qt.AlignmentFlag.AlignHCenter)
        qr_layout.addWidget(self.lbl_qr_img, alignment=Qt.AlignmentFlag.AlignHCenter)

        # --- ENSAMBLAJE FINAL DE LA PANTALLA ---
        main_layout.addStretch(1) # Empuja la tarjeta hacia el centro
        
        # Centrar la tarjeta horizontalmente
        center_h_layout = QHBoxLayout()
        center_h_layout.addStretch(1)
        center_h_layout.addWidget(card)
        center_h_layout.addStretch(1)
        main_layout.addLayout(center_h_layout)
        
        main_layout.addStretch(1) # Empuja el QR hacia abajo
        
        # Alinear el QR a la derecha
        bottom_h_layout = QHBoxLayout()
        bottom_h_layout.addStretch(1)
        bottom_h_layout.addLayout(qr_layout)
        bottom_h_layout.setContentsMargins(0, 0, 20, 10) # Márgenes para que no quede pegado al borde
        
        main_layout.addLayout(bottom_h_layout)

        self.stacked_widget.addWidget(page)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecciona tu material", "", "Archivos soportados (*.pdf *.txt)")
        if not file_path:
            return
        
        content = ""
        try:
            if file_path.lower().endswith(".pdf"):
                with open(file_path, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            content += text + "\n"
            else:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            
            self.txt_material.setPlainText(content)
            QMessageBox.information(self, "Exito", f"Archivo cargado correctamente ({len(content)} caracteres).")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo leer el archivo: {e}")

    # --- PANTALLA 2: CARGANDO ---
    def init_loading_screen(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("GENERANDO CALABOZO...")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("La IA esta analizando tu material y creando enemigos.\nPor favor espera unos segundos.")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        self.stacked_widget.addWidget(page)

    def start_generation(self):
        material = self.txt_material.toPlainText().strip()
        if not material:
            QMessageBox.warning(self, "Falta Material", "Por favor ingresa o carga un texto.")
            return

        diff_key = self.combo_diff.currentText()
        lang_key = self.combo_lang.currentText()
        settings = self.difficulty_settings[diff_key]
        
        self.max_lives = settings["lives"]
        self.lives = settings["lives"]
        
        # Cambiar a pantalla de carga
        self.stacked_widget.setCurrentIndex(1)
        
        # Iniciar hilo de IA
        self.worker = AIWorker(material, settings["name"], settings["q"], lang_key)
        self.worker.finished.connect(self.on_generation_finished)
        self.worker.error.connect(self.on_generation_error)
        self.worker.start()

    def on_generation_error(self, error_msg):
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            msg = "Has excedido el limite de la IA. Espera 2 minutos."
        elif "503" in error_msg or "UNAVAILABLE" in error_msg:
            msg = "Los servidores de Google Gemini estan muy saturados en este momento (Error 503).\n\nPor favor, espera unos segundos y vuelve a intentarlo."
        else:
            msg = f"Error de conexion:\n{error_msg}"
        QMessageBox.critical(self, "Error", msg)
        self.stacked_widget.setCurrentIndex(0)

    def on_generation_finished(self, questions):
        if not questions:
            QMessageBox.warning(self, "Error", "La IA no pudo procesar este texto.")
            self.stacked_widget.setCurrentIndex(0)
            return
            
        self.questions = questions
        self.score = 0
        self.current_index = 0
        self.time_elapsed = 0
        
        self.timer.start(1000)
        self.load_question()
        self.stacked_widget.setCurrentIndex(2)

    # --- PANTALLA 3: JUEGO ---
    def init_game_screen(self):
        self.game_page = QWidget()
        layout = QVBoxLayout(self.game_page)
        
        # HUD Top
        hud = QHBoxLayout()
        self.lbl_lives = QLabel()
        self.lbl_lives.setObjectName("HudText")
        self.lbl_lives.setStyleSheet("color: #ef4444;")
        
        self.lbl_timer = QLabel("TIEMPO: 00:00")
        self.lbl_timer.setObjectName("HudText")
        self.lbl_timer.setStyleSheet("color: #38bdf8;")
        self.lbl_timer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.lbl_score = QLabel("PTS: 0")
        self.lbl_score.setObjectName("HudText")
        self.lbl_score.setStyleSheet("color: #facc15;")
        self.lbl_score.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        hud.addWidget(self.lbl_lives)
        hud.addWidget(self.lbl_timer, 1)
        hud.addWidget(self.lbl_score)
        
        # Panel Enemigo
        self.enemy_frame = QFrame()
        self.enemy_frame.setObjectName("Card")
        enemy_layout = QVBoxLayout(self.enemy_frame)
        enemy_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.lbl_enemy_phase = QLabel()
        self.lbl_enemy_phase.setStyleSheet("font-weight: bold; color: white;")
        
        # AQUI VA TU IMAGEN PNG EN EL FUTURO
        self.lbl_enemy_img = QLabel("[Espacio para imagen PNG]")
        self.lbl_enemy_img.setStyleSheet("color: rgba(255,255,255,0.3); font-style: italic;")
        self.lbl_enemy_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Cuando pongas tu PNG, el escalado hará que la animación se vea bien:
        self.lbl_enemy_img.setScaledContents(True)
        # self.lbl_enemy_img.setPixmap(QPixmap("enemigo.png"))  # <-- descomenta y usa tu PNG
        
        # ---------------------------------------------------------------
        # MEJORA 3: ANIMACIÓN DE "RESPIRACIÓN" DEL ENEMIGO (QPropertyAnimation)
        # Anima minimumSize y maximumSize en paralelo para que la imagen
        # crezca y encoja suavemente, dando sensación de estar viva.
        # ---------------------------------------------------------------
        self.setup_enemy_animation()
        
        self.lbl_enemy_name = QLabel()
        self.lbl_enemy_name.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        
        enemy_layout.addWidget(self.lbl_enemy_phase, 0, Qt.AlignmentFlag.AlignCenter)
        enemy_layout.addWidget(self.lbl_enemy_img, 0, Qt.AlignmentFlag.AlignCenter)
        enemy_layout.addWidget(self.lbl_enemy_name, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Pregunta y Botones
        self.question_frame = QFrame()
        self.question_frame.setObjectName("Card")
        self.q_layout = QVBoxLayout(self.question_frame)
        self.q_layout.setContentsMargins(30, 30, 30, 30)
        
        self.lbl_question = QLabel()
        self.lbl_question.setWordWrap(True)
        self.lbl_question.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-bottom: 20px;")
        
        self.options_layout = QVBoxLayout()
        
        self.q_layout.addWidget(self.lbl_question)
        self.q_layout.addLayout(self.options_layout)
        self.q_layout.addStretch()
        
        # Ensamblaje
        layout.addLayout(hud)
        layout.addWidget(self.enemy_frame)
        layout.addWidget(self.question_frame, 1)
        
        self.stacked_widget.addWidget(self.game_page)

    # ===================================================================
    # MEJORA 3: CONFIGURACIÓN DE LA ANIMACIÓN DEL ENEMIGO
    # ===================================================================
    def setup_enemy_animation(self):
        base = QSize(150, 150)   # tamaño mínimo (exhala)
        grow = QSize(178, 178)   # tamaño máximo (inhala)

        self.lbl_enemy_img.setMinimumSize(base)
        self.lbl_enemy_img.setMaximumSize(base)

        # Animamos minimumSize y maximumSize a la vez para forzar el tamaño real.
        anim_min = QPropertyAnimation(self.lbl_enemy_img, b"minimumSize", self)
        anim_min.setDuration(1600)
        anim_min.setStartValue(base)
        anim_min.setKeyValueAt(0.5, grow)
        anim_min.setEndValue(base)
        anim_min.setEasingCurve(QEasingCurve.Type.InOutSine)

        anim_max = QPropertyAnimation(self.lbl_enemy_img, b"maximumSize", self)
        anim_max.setDuration(1600)
        anim_max.setStartValue(base)
        anim_max.setKeyValueAt(0.5, grow)
        anim_max.setEndValue(base)
        anim_max.setEasingCurve(QEasingCurve.Type.InOutSine)

        self.enemy_anim = QParallelAnimationGroup(self)
        self.enemy_anim.addAnimation(anim_min)
        self.enemy_anim.addAnimation(anim_max)
        self.enemy_anim.setLoopCount(-1)  # bucle infinito
        self.enemy_anim.start()

    def update_timer(self):
        self.time_elapsed += 1
        mins = self.time_elapsed // 60
        secs = self.time_elapsed % 60
        self.lbl_timer.setText(f"TIEMPO: {mins:02d}:{secs:02d}")

    def load_question(self):
        self.lbl_lives.setText(f"VIDAS: {self.lives}/{self.max_lives}")
        self.lbl_score.setText(f"PTS: {self.score}")
        
        # Logica de Enemigo
        total = len(self.questions)
        idx = self.current_index
        
        if total <= 10:
            type_code = "tarea" if idx < 2 else ("proyecto" if idx < 6 else "examen")
        elif total <= 15:
            type_code = "tarea" if idx < 5 else ("proyecto" if idx < 10 else "examen")
        else:
            type_code = "tarea" if idx < 7 else ("proyecto" if idx < 14 else "examen")
            
        if type_code == "tarea":
            self.enemy_frame.setStyleSheet("QFrame#Card { background-color: #475569; border-radius: 15px; }")
            self.lbl_enemy_phase.setText(f">> FASE 1: TAREA (Nivel {idx+1}/{total}) <<")
            self.lbl_enemy_name.setText("Enemigo Menor: Tarea Pendiente")
        elif type_code == "proyecto":
            self.enemy_frame.setStyleSheet("QFrame#Card { background-color: #1d4ed8; border-radius: 15px; }")
            self.lbl_enemy_phase.setText(f">> FASE 2: PROYECTO (Nivel {idx+1}/{total}) <<")
            self.lbl_enemy_name.setText("Enemigo Fuerte: Proyecto Semestral")
        else:
            self.enemy_frame.setStyleSheet("QFrame#Card { background-color: #b91c1c; border-radius: 15px; }")
            self.lbl_enemy_phase.setText(f">> FASE 3: JEFE FINAL (Nivel {idx+1}/{total}) <<")
            self.lbl_enemy_name.setText("EL EXAMEN FINAL")
            
        # Limpiar botones anteriores
        for i in reversed(range(self.options_layout.count())): 
            self.options_layout.itemAt(i).widget().setParent(None)
            
        q_data = self.questions[self.current_index]
        self.lbl_question.setText(q_data["q"])
        
        for opt in q_data["options"]:
            btn = QPushButton(opt)
            btn.setObjectName("OptionBtn")
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.clicked.connect(lambda checked, o=opt: self.check_answer(o))
            self.options_layout.addWidget(btn)

    def check_answer(self, selected):
        q_data = self.questions[self.current_index]
        is_correct = (selected == q_data["correct"])
        
        # Limpiar opciones
        for i in reversed(range(self.options_layout.count())): 
            self.options_layout.itemAt(i).widget().setParent(None)
            
        feedback_frame = QFrame()
        feedback_layout = QVBoxLayout(feedback_frame)
        
        title = QLabel()
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        
        if is_correct:
            self.snd_correct.play()  # MEJORA 1: sonido de golpe crítico
            self.score += 100
            self.lbl_score.setText(f"PTS: {self.score}")
            title.setText("GOLPE CRITICO! Respuesta Correcta")
            title.setStyleSheet("font-size: 20px; font-weight: bold; color: #4ade80;")
        else:
            self.snd_wrong.play()  # MEJORA 1: sonido de daño recibido
            self.lives -= 1
            self.lbl_lives.setText(f"VIDAS: {self.lives}/{self.max_lives}")
            title.setText("ATAQUE FALLIDO! El enemigo te daño")
            title.setStyleSheet("font-size: 20px; font-weight: bold; color: #f87171;")
            
        rationale = QLabel(f"Explicacion: {q_data['rationale']}")
        rationale.setWordWrap(True)
        rationale.setStyleSheet("font-size: 16px; margin-top: 10px;")
        
        ref = QLabel(f"Referencia: \"{q_data['reference']}\"")
        ref.setWordWrap(True)
        ref.setStyleSheet("font-size: 14px; font-style: italic; color: #94a3b8;")
        
        feedback_layout.addWidget(title)
        feedback_layout.addWidget(rationale)
        feedback_layout.addWidget(ref)
        self.options_layout.addWidget(feedback_frame)
        
        btn_next = QPushButton()
        btn_next.setObjectName("PrimaryBtn")
        btn_next.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        if self.lives <= 0:
            self.timer.stop()
            btn_next.setText("VER RESULTADOS (GAME OVER)")
            btn_next.clicked.connect(self.show_results)
        elif self.current_index + 1 >= len(self.questions):
            self.timer.stop()
            btn_next.setText("RECLAMAR VICTORIA")
            btn_next.clicked.connect(self.show_results)
        else:
            btn_next.setText("SIGUIENTE BATALLA >>")
            btn_next.clicked.connect(self.next_question)
            
        self.options_layout.addWidget(btn_next)

    def next_question(self):
        self.current_index += 1
        self.load_question()

    # --- PANTALLA 4: RESULTADOS ---
    def init_result_screen(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.res_card = QFrame()
        self.res_card.setObjectName("Card")
        self.res_card.setFixedSize(600, 450)
        res_layout = QVBoxLayout(self.res_card)
        res_layout.setContentsMargins(40, 40, 40, 40)
        
        self.lbl_res_title = QLabel()
        self.lbl_res_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.lbl_res_sub = QLabel()
        self.lbl_res_sub.setObjectName("Subtitle")
        self.lbl_res_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.lbl_res_stats = QLabel()
        self.lbl_res_stats.setStyleSheet("font-size: 18px; line-height: 1.5; margin-top: 20px;")
        self.lbl_res_stats.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn_menu = QPushButton("VOLVER AL MENU PRINCIPAL")
        btn_menu.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_menu.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        
        res_layout.addWidget(self.lbl_res_title)
        res_layout.addWidget(self.lbl_res_sub)
        res_layout.addWidget(self.lbl_res_stats)
        res_layout.addStretch()
        res_layout.addWidget(btn_menu)
        
        layout.addWidget(self.res_card)
        self.stacked_widget.addWidget(page)

    def show_results(self):
        self.snd_end.play()  # MEJORA 1: sonido al llegar a Victoria / Game Over

        is_win = self.lives > 0 and (self.current_index + 1 >= len(self.questions))
        
        if is_win:
            self.lbl_res_title.setText("MAZMORRA SUPERADA")
            self.lbl_res_title.setStyleSheet("font-size: 32px; font-weight: bold; color: #facc15;")
            self.lbl_res_sub.setText("Has derrotado al Examen Final y dominado el tema.")
            self.res_card.setStyleSheet("QFrame#Card { background-color: #1e1b4b; border: 2px solid #a855f7; border-radius: 15px; }")
        else:
            self.lbl_res_title.setText("GAME OVER")
            self.lbl_res_title.setStyleSheet("font-size: 32px; font-weight: bold; color: #f87171;")
            self.lbl_res_sub.setText("El Examen ha reclamado tu alma. Necesitas estudiar mas.")
            self.res_card.setStyleSheet("QFrame#Card { background-color: #450a0a; border: 2px solid #ef4444; border-radius: 15px; }")
            
        mins = self.time_elapsed // 60
        secs = self.time_elapsed % 60
        
        stats_text = (
            f"Puntuacion Final: {self.score} pts\n"
            f"Tiempo de Supervivencia: {mins:02d}:{secs:02d}\n"
            f"Batallas Alcanzadas: {self.current_index + 1} de {len(self.questions)}"
        )
        self.lbl_res_stats.setText(stats_text)

        # ---------------------------------------------------------------
        # MEJORA 2: PERSISTENCIA DE PUNTUACIÓN (File I/O en modo 'append')
        # Guarda fecha, resultado, puntos y tiempo en historial_partidas.txt
        # ---------------------------------------------------------------
        try:
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            resultado = "VICTORIA" if is_win else "DERROTA"
            with open("historial_partidas.txt", "a", encoding="utf-8") as f:
                f.write(f"{fecha} | {resultado} | Puntos: {self.score} | Tiempo: {mins:02d}:{secs:02d}\n")
        except Exception as e:
            print(f"No se pudo guardar el historial: {e}")

        self.stacked_widget.setCurrentIndex(3)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudyGameApp()
    window.show()
    sys.exit(app.exec())