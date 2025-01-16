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

def remove_background(input_path, progress_var, root):
    """Remove o fundo da imagem e salva no diretório de saída."""
    try:
        output_folder = ensure_output_folder()
        output_path = os.path.join(output_folder, os.path.basename(input_path))

        progress_var.set(10)
        root.update_idletasks()

        with open(input_path, "rb") as input_file:
            input_image = input_file.read()
            progress_var.set(50)
            root.update_idletasks()

            output_image = remove(input_image)
            progress_var.set(80)
            root.update_idletasks()

        with open(output_path, "wb") as output_file:
            output_file.write(output_image)
            progress_var.set(100)
            root.update_idletasks()

        messagebox.showinfo("Sucesso", f"Imagem processada e salva em: {output_path}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar a imagem:\n{str(e)}")
        progress_var.set(0)

def select_file(progress_var, root):
    """Abre o seletor de arquivos para escolher a imagem."""
    file_path = filedialog.askopenfilename(
        title="Selecione uma imagem",
        filetypes=[("Imagens", "*.jpg *.jpeg *.png *.PNG")]  # Mostra apenas arquivos de imagem
    )
    if file_path and os.path.isfile(file_path):  # Certifica-se de que um arquivo foi selecionado
        progress_var.set(0)
        remove_background(file_path, progress_var, root)
    else:
        messagebox.showwarning("Atenção", "Por favor, selecione um arquivo de imagem válido.")

def create_gui():
    """Cria a interface gráfica."""
    root = TkinterDnD.Tk()
    root.title("TERMICOM - REMOVE BG")
    root.geometry("400x400")
    root.resizable(False, False)

    # Título
    title_label = tk.Label(root, text="Arraste uma imagem ou clique para selecionar", font=("Arial", 14))
    title_label.pack(pady=20)

    # Barra de progresso
    progress_var = tk.IntVar()
    progress_bar = tk.Scale(
        root, variable=progress_var, from_=0, to=100, orient="horizontal", length=300,
        showvalue=False, sliderlength=10, state="disabled", troughcolor="#e0e0e0",
        fg="#4CAF50", bg="#ffffff"
    )
    progress_bar.pack(pady=10)

    # Botão para selecionar arquivo
    select_button = tk.Button(root, text="Selecionar Imagem", command=lambda: select_file(progress_var, root), font=("Arial", 12), bg="#4CAF50", fg="white")
    select_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()