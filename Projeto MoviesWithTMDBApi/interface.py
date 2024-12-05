import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QScrollArea, 
                             QGridLayout, QMessageBox, QFrame, QDesktopWidget, 
                             QProgressBar)
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal
from functools import lru_cache
from main import recommend_movies, get_movie_id, get_similar_movies, API_KEY, BASE_URL

# caching de imagens de pôsteres
@lru_cache(maxsize=100)
def load_poster_image(poster_url):
    try:
        response = requests.get(poster_url, timeout=5)
        return response.content
    except Exception as e:
        print(f"Erro ao carregar poster: {e}")
        return None

class MovieFetchThread(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, movie_name):
        super().__init__()
        self.movie_name = movie_name

    def run(self):
        try:
            movie_id = get_movie_id(self.movie_name)
            
            if not movie_id:
                self.error.emit('Filme não encontrado')
                return
            
            similar_movies = get_similar_movies(movie_id)
            
            if not similar_movies:
                self.error.emit('Nenhum filme semelhante encontrado')
                return
            
            top_movies = sorted(similar_movies, key=lambda x: x['vote_average'], reverse=True)[:12]
            self.finished.emit(top_movies)
        
        except Exception as e:
            self.error.emit(f'Ocorreu um erro: {str(e)}')

class MoviePosterWidget(QFrame):
    def __init__(self, movie_data):
        super().__init__()
        self.movie_data = movie_data
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #2C2C2C;
                border-radius: 10px;
                padding: 10px;
                margin: 5px;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout()

        # imagem do filme
        self.poster_label = QLabel()
        self.poster_label.setAlignment(Qt.AlignCenter)
        self.poster_label.setFixedSize(200, 300)
        self.load_poster()
        layout.addWidget(self.poster_label)

        # título do filme
        title_label = QLabel(self.movie_data['title'])
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        rating_label = QLabel(f"Nota: {self.movie_data['vote_average']:.1f}")
        rating_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(rating_label)

        release_label = QLabel(f"Lançamento: {self.movie_data.get('release_date', 'Desconhecido')}")
        release_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(release_label)

        self.setLayout(layout)

    def load_poster(self):
        poster_path = self.movie_data.get('poster_path')
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w300{poster_path}"
            
            import threading
            threading.Thread(target=self.fetch_poster, args=(poster_url,), daemon=True).start()

    def fetch_poster(self, poster_url):
        image_data = load_poster_image(poster_url)
        
        if image_data:
            from PyQt5.QtCore import QByteArray
            from PyQt5.QtGui import QImage, QPixmap
            from PyQt5.QtCore import pyqtSignal, QObject

            # classe para emitir sinal de UI
            class PosterSignals(QObject):
                update_poster = pyqtSignal(QPixmap)

            signals = PosterSignals()
            signals.update_poster.connect(self.update_poster_ui)

            # converter dados da imagem
            image = QImage.fromData(image_data)
            pixmap = QPixmap.fromImage(image).scaled(
                200, 300, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            
            # emitir sinal para atualizar UI
            signals.update_poster.emit(pixmap)

    def update_poster_ui(self, pixmap):
        # atualizar UI
        self.poster_label.setPixmap(pixmap)

class MovieRecommenderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.center_on_screen()
        
    def center_on_screen(self):
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())
        
    def initUI(self):
        self.setWindowTitle('Recomendador de Filmes')
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #404040;
                border-radius: 8px;
                background-color: #2C2C2C;
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QProgressBar {
                border: 2px solid #404040;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
        """)
        
        main_layout = QVBoxLayout()
        
        title = QLabel('Recomendador de Filmes')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Segoe UI', 20, QFont.Bold))
        main_layout.addWidget(title)
        
        input_layout = QHBoxLayout()
        
        self.movie_input = QLineEdit()
        self.movie_input.setPlaceholderText('Digite o nome do filme...')
        input_layout.addWidget(self.movie_input)
        
        search_btn = QPushButton('Buscar')
        search_btn.clicked.connect(self.buscar_recomendacoes)
        input_layout.addWidget(search_btn)
        
        main_layout.addLayout(input_layout)

        # barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0) 
        self.progress_bar.hide()
        main_layout.addWidget(self.progress_bar)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        self.results_widget = QWidget()
        
        self.results_layout = QGridLayout(self.results_widget)
        self.results_layout.setAlignment(Qt.AlignCenter)
        
        scroll_area.setWidget(self.results_widget)
        
        main_layout.addWidget(scroll_area)
        
        self.setLayout(main_layout)
        
    def buscar_recomendacoes(self):
        # limpar resultados anteriores
        for i in reversed(range(self.results_layout.count())): 
            widget = self.results_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        filme = self.movie_input.text().strip()
        
        if not filme:
            QMessageBox.warning(self, 'Erro', 'Por favor, digite o nome de um filme.')
            return
        
        # mostrar barra de progresso
        self.progress_bar.show()
        
        self.fetch_thread = MovieFetchThread(filme)
        self.fetch_thread.finished.connect(self.exibir_resultados)
        self.fetch_thread.error.connect(self.exibir_erro)
        self.fetch_thread.start()
        
    def exibir_resultados(self, top_movies):
        # esconder barra de progresso
        self.progress_bar.hide()
        
        # exibir filmes em grade centralizada
        for i, movie in enumerate(top_movies):
            movie_widget = MoviePosterWidget(movie)
            row = i // 4
            col = i % 4
            self.results_layout.addWidget(movie_widget, row, col)
        
    def exibir_erro(self, mensagem):
        # esconder barra de progresso
        self.progress_bar.hide()
        QMessageBox.warning(self, 'Erro', mensagem)

def main():
    app = QApplication(sys.argv)
    ex = MovieRecommenderApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()