 import os

import re

import subprocess  # NOUVEAU: Pour exécuter les commandes système

from flask import Flask, render_template_string, send_from_directory, request, url_for


app = Flask(__name__)


# Le chemin du dossier où est le script (BASE_DIR)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Le chemin vidéo est le sous-dossier 'video'

VIDEO_DIR = os.path.join(BASE_DIR, 'video')

PORT = 8000


# --- Fonction d'Administration Système pour Libérer le Port ---

import os

import re

import subprocess  # Pour exécuter les commandes système

# ... (le reste des imports et variables) ...


PORT = 8000


# --- Fonction d'Administration Système pour Libérer le Port ---

def kill_blocking_process(port):

    """

    Trouve et termine SPECIFIQUEMENT les processus Python qui bloquent le port donné.

    Nécessite des permissions élevées (Administrateur) pour fonctionner.

    """

    current_pid = str(os.getpid())

    print(f"PID actuel du script: {current_pid}")


    try:

        # 1. Trouver les PID utilisant le port et inclure le nom de l'image (tasklist)

        # On utilise 'tasklist' qui est plus adapté pour obtenir le nom du processus (ImageName)

       

        # Commande pour trouver le PID et le nom du processus (ImageName)

        # Note : On doit trouver le PID via netstat, puis vérifier son nom via tasklist

       

        netstat_command = f'netstat -ano | findstr :"{port}"'

        result_netstat = subprocess.run(

            netstat_command,

            capture_output=True, text=True, check=False, shell=True

        )

       

        lines = result_netstat.stdout.strip().split('\n')

        pids_to_kill = []


        for line in lines:

            if 'LISTENING' in line:

                pid = line.split()[-1]

               

                # Ignorer le processus actuel

                if pid == current_pid:

                    continue

               

                # 2. Vérifier si le PID est un processus Python

                # tasklist /FI "PID eq [PID]" affiche le nom du processus

                tasklist_command = f'tasklist /FI "PID eq {pid}" /NH' # /NH = No Header

                result_tasklist = subprocess.run(

                    tasklist_command,

                    capture_output=True, text=True, check=False, shell=True

                )

               

                # Le résultat contient le nom de l'image (ex: python.exe)

                if result_tasklist.stdout:

                    process_name = result_tasklist.stdout.split()[0].lower()

                   

                    if process_name in ['python.exe', 'pythonw.exe']:

                        pids_to_kill.append(pid)



        if not pids_to_kill:

            print(f"Port {port} libre ou aucun processus Python bloquant trouvé.")

            return


        for pid in pids_to_kill:

            print(f"Processus PYTHON PID {pid} trouvé sur le port {port}. Tentative d'arrêt...")

           

            # 3. Tuer le processus

            taskkill_command = f'taskkill /PID {pid} /F'

            subprocess.run(taskkill_command, check=False, shell=True, capture_output=True, text=True)

           

            print(f"Processus PYTHON PID {pid} terminé.")

       

    except Exception as e:

        print(f"Erreur inattendue lors du nettoyage: {e}")



# --- Fonction pour le tri naturel (Natural Sort) ---

def natural_sort_key(s):

    """Sépare les parties numériques et non numériques d'une chaîne pour un tri correct."""

    return [int(text) if text.isdigit() else text.lower()

            for text in re.split(r'(\d+)', s)]


# --- Route 1: La Page d'Accueil avec les Boutons TRIÉS ---

@app.route('/')

def index():

    if not os.path.exists(VIDEO_DIR):

        return "Erreur : Le dossier 'video' n'existe pas ou n'est pas trouvé."

       

    files = os.listdir(VIDEO_DIR)

    video_files = [f for f in files if f.lower().endswith('.mp4')]

   

    video_files.sort(key=natural_sort_key)

   

    html_template_index = """

    <!DOCTYPE html>

    <html lang="fr">

    <head>

        <meta charset="UTF-8">

        <title>Accueil Vidéos Local</title>

        <meta name="viewport" content="width=device-width, initial-scale=1">

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

                text-align: center;

                font-size: 18px;

                box-shadow: 2px 2px 5px rgba(0,0,0,0.2);

                background: linear-gradient(180deg, #1e90ff, #007bff);

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


# ... (Routes play_video et stream_file restent les mêmes) ...


@app.route('/play/<filename>')

def play_video(filename):

    video_url = url_for('stream_file', filename=filename)


    html_template_player = f"""

    <!DOCTYPE html>

    <html lang="fr">

    <head>

        <meta charset="UTF-8">

        <title>{filename}</title>

        <meta name="viewport" content="width=device-width, initial-scale=1">

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


@app.route('/video/<path:filename>')

def stream_file(filename):

    return send_from_directory(VIDEO_DIR, filename)



if __name__ == '__main__':

    # EXÉCUTION DE LA TÂCHE DE NETTOYAGE AVANT LE DÉMARRAGE

    kill_blocking_process(PORT)

   

    # DÉMARRAGE DU SERVEUR FLASK

    app.run(host='0.0.0.0', port=PORT, debug=False) 
