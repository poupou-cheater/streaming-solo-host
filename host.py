import os
from flask import Flask, render_template_string, send_from_directory, request, url_for

app = Flask(__name__)
# Le chemin vers le dossier où se trouvent les vidéos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_DIR = os.path.join(BASE_DIR, 'video')

# --- Route 1: La Page d'Accueil avec les Boutons ---
@app.route('/')
def index():
    files = os.listdir(VIDEO_DIR)
    video_files = [f for f in files if f.lower().endswith('.mp4')]
    
    # Le template HTML pour la page d'accueil
    html_template_index = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Accueil Vidéos Local</title>
        <style>
            body { font-family: sans-serif; padding: 20px; background-color: #f4f4f4; }
            .video-button {
                display: block;
                width: 100%;
                padding: 15px;
                margin-bottom: 10px;
                background-color: #007bff;
                color: white;
                text-decoration: none;
                border: none;
                border-radius: 5px;
                text-align: left;
                font-size: 18px;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
            }
            .video-button:hover { background-color: #0056b3; }
        </style>
    </head>
    <body>
        <h1>Cliquez pour lire :</h1>
        {% for video in videos %}
            <a href="{{ url_for('play_video', filename=video) }}" class="video-button">{{ video }}</a>
        {% endfor %}
    </body>
    </html>
    """
    
    return render_template_string(html_template_index, videos=video_files)

# --- Route 2: La Page de Lecture Vidéo Minimaliste ---
@app.route('/play/<filename>')
def play_video(filename):
    # L'URL du fichier vidéo que le navigateur du téléphone doit lire
    # La fonction 'stream_file' va servir le fichier MP4
    video_url = url_for('stream_file', filename=filename)

    # Le template HTML ne contenant que le lecteur vidéo
    html_template_player = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>{filename}</title>
        <style>
            body {{ margin: 0; background-color: black; }}
            video {{ width: 100vw; height: 100vh; object-fit: contain; }}
        </style>
    </head>
    <body>
        <video controls autoplay src="{video_url}"></video>
    </body>
    </html>
    """
    return render_template_string(html_template_player)

# --- Route 3: Le Serveur de Fichiers (Sert le MP4 lui-même) ---
@app.route('/video/<path:filename>')
def stream_file(filename):
    # Ceci sert le fichier MP4 via HTTP
    return send_from_directory(VIDEO_DIR, filename)

if __name__ == '__main__':
    # Lance le serveur, accessible par le téléphone (0.0.0.0)
    app.run(host='0.0.0.0', port=8000, debug=True)