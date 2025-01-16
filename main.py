import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from rembg import remove
from PIL import Image, ImageTk

def ensure_output_folder():
    """Garante que a pasta de saída exista em 'Meus Documentos'."""
    documents_folder = os.path.expanduser("~/Documents")
    output_folder = os.path.join(documents_folder, "ImagensSemFundo")
    os.makedirs(output_folder, exist_ok=True)
    return output_folder

def remove_background(input_path):
    """Remove o fundo da imagem e salva no diretório de saída."""
    try:
        output_folder = ensure_output_folder()
        output_path = os.path.join(output_folder, os.path.basename(input_path))

        with open(input_path, "rb") as input_file:
            input_image = input_file.read()
            output_image = remove(input_image)

        with open(output_path, "wb") as output_file:
            output_file.write(output_image)

        messagebox.showinfo("Sucesso", f"Imagem processada e salva em: {output_path}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar a imagem:\n{str(e)}")

def select_file():
    """Abre o seletor de arquivos para escolher a imagem."""
    file_path = filedialog.askopenfilename(
        filetypes=[("Imagens", "*.jpg *.jpeg *.png")]
    )
    if file_path:
        remove_background(file_path)

def drop_file(event):
    """Trata o evento de arrastar e soltar uma imagem."""
    file_path = event.data.strip()
    if os.path.isfile(file_path):
        remove_background(file_path)

def create_gui():
    """Cria a interface gráfica."""
    root = TkinterDnD.Tk()
    root.title("Remove BackGround - TERMICOM")
    root.geometry("400x300")
    root.resizable(False, False)

    # Título
    title_label = tk.Label(root, text="Arraste uma imagem ou clique para selecionar", font=("Arial", 14))
    title_label.pack(pady=20)

    # Área para arrastar arquivos
    drop_frame = tk.Frame(root, width=350, height=150, bg="#f0f0f0", relief=tk.RIDGE, bd=2)
    drop_frame.pack(pady=10)
    drop_frame.pack_propagate(False)

    drop_label = tk.Label(drop_frame, text="Solte a imagem aqui", font=("Arial", 12))
    drop_label.pack(expand=True)

    drop_frame.drop_target_register(DND_FILES)
    drop_frame.dnd_bind("<Drop>", drop_file)

    # Botão para selecionar arquivo
    select_button = tk.Button(root, text="Selecionar Imagem", command=select_file, font=("Arial", 12), bg="#4CAF50", fg="white")
    select_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
