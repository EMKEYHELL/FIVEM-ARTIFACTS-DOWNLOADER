import requests
import os
import re
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser
import py7zr

def get_latest_artifact_url():
    artifacts_page_url = "https://runtime.fivem.net/artifacts/fivem/build_server_windows/master/"
    response = requests.get(artifacts_page_url)
    response.raise_for_status()
    
    match = re.search(r'href="([^"]+\.7z)"', response.text)
    if match:
        return artifacts_page_url + match.group(1)
    else:
        raise Exception("Nessun file .7z trovato.")

def download_artifacts(url):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    artifact_folder = os.path.join(desktop_path, "artifact")
    os.makedirs(artifact_folder, exist_ok=True)

    archive_file_path = os.path.join(artifact_folder, "artifact.7z")

    try:
        response = requests.get(url)
        response.raise_for_status()
        
        with open(archive_file_path, 'wb') as f:
            f.write(response.content)
        messagebox.showinfo("Download completato", "Artifact scaricati con successo!")

        try:
            with py7zr.SevenZipFile(archive_file_path, mode='r') as archive:
                archive.extractall(path=artifact_folder)
            messagebox.showinfo("Estrazione completata", "Artifact estratti nella cartella.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'estrazione: {str(e)}")
    except requests.RequestException as e:
        messagebox.showerror("Errore nel download", str(e))
    except Exception as e:
        messagebox.showerror("Errore", str(e))

def download_latest():
    try:
        url = get_latest_artifact_url()
        download_artifacts(url)
    except Exception as e:
        messagebox.showerror("Errore", str(e))

# Funzione per aprire GitHub
def open_github():
    webbrowser.open("https://github.com/EMKEYHELL")

# Funzione per aprire Discord
def open_discord():
    webbrowser.open("https://discord.gg/jjsQU2bFBP")

# Crea la finestra principale
root = tk.Tk()
root.title("Artifact Downloader")

# Aggiungi l'icona personalizzata
icon_path = r"C:\Users\Matti\Desktop\ARTIFACT-DOWNLOADER\hc.ico"
root.iconbitmap(icon_path)

# Aggiungi lo sfondo personalizzato
bg_image_path = r"C:\Users\Matti\Desktop\ARTIFACT-DOWNLOADER\hc.png"
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((500, 300), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Aggiungi una label che contiene l'immagine di sfondo
background_label = tk.Label(root, image=bg_photo)
background_label.place(relwidth=1, relheight=1)

# Crea il pulsante per scaricare gli ultimi artifact e centrali
latest_button = tk.Button(root, text="Scarica Ultimi Artifact", command=download_latest)
latest_button.pack(pady=30)  # Usa pack() con padding per centrarlo verticalmente

# Carica e aggiungi il pulsante GitHub con l'icona
github_icon_path = r"C:\Users\Matti\Desktop\ARTIFACT-DOWNLOADER\github.png"  # Percorso dell'icona GitHub
github_icon = Image.open(github_icon_path)
github_icon = github_icon.resize((40, 40), Image.Resampling.LANCZOS)
github_photo = ImageTk.PhotoImage(github_icon)

github_button = tk.Button(root, image=github_photo, command=open_github)
github_button.place(x=150, y=200)  # Posizione del pulsante

# Carica e aggiungi il pulsante Discord con l'icona
discord_icon_path = r"C:\Users\Matti\Desktop\ARTIFACT-DOWNLOADER\discord.png"  # Percorso dell'icona Discord
discord_icon = Image.open(discord_icon_path)
discord_icon = discord_icon.resize((40, 40), Image.Resampling.LANCZOS)
discord_photo = ImageTk.PhotoImage(discord_icon)

discord_button = tk.Button(root, image=discord_photo, command=open_discord)
discord_button.place(x=300, y=200)  # Posizione del pulsante

# Esegui il loop principale dell'interfaccia grafica
root.geometry("500x300")  # Dimensioni della finestra
root.mainloop()
