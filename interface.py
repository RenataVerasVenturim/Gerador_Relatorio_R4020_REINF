import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import subprocess

# Variáveis globais para armazenar os arquivos carregados
xml_file_path = None
xlsx_file_path = None

# Função para carregar arquivo XML
def carregar_xml():
    global xml_file_path
    xml_file_path = filedialog.askopenfilename(filetypes=[("Arquivos XML", "*.xml")])
    if xml_file_path:
        label_xml_file.config(text=f"Arquivo XML: {os.path.basename(xml_file_path)}")
    else:
        label_xml_file.config(text="Nenhum arquivo XML selecionado")

# Função para carregar arquivo XLSX
def carregar_xlsx():
    global xlsx_file_path
    xlsx_file_path = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])
    if xlsx_file_path:
        label_xlsx_file.config(text=f"Arquivo XLSX: {os.path.basename(xlsx_file_path)}")
    else:
        label_xlsx_file.config(text="Nenhum arquivo XLSX selecionado")

# Função para limpar a pasta ExtracaoSiafi antes de mover os arquivos
def limpar_pasta_siafi():
    diretorio = "ExtracaoSiafi"
    if os.path.exists(diretorio):
        for arquivo in os.listdir(diretorio):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            try:
                os.remove(caminho_arquivo) if os.path.isfile(caminho_arquivo) else shutil.rmtree(caminho_arquivo)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao limpar a pasta 'ExtracaoSiafi': {e}")

# Função para mover arquivos para as pastas correspondentes
def mover_arquivos():
    if not xml_file_path or not xlsx_file_path:
        messagebox.showerror("Erro", "Ambos os arquivos XML e XLSX devem ser carregados antes de mover.")
        return

    limpar_pasta_siafi()
    os.makedirs("ExtracaoSiafi", exist_ok=True)
    os.makedirs("TesouroGerencialDocs", exist_ok=True)

    try:
        shutil.copy(xml_file_path, os.path.join("ExtracaoSiafi", os.path.basename(xml_file_path)))
        shutil.copy(xlsx_file_path, os.path.join("TesouroGerencialDocs", "Ordens Bancárias REINF.xlsx"))
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao mover arquivos: {e}")

# Função para executar scripts externos
def executar_script(script_nome):
    try:
        subprocess.run(["python", script_nome], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Erro ao executar {script_nome}: {e}")

# Função para gerar o relatório
def gerar_relatorio():
    if not xml_file_path or not xlsx_file_path:
        messagebox.showerror("Erro", "Carregue ambos os arquivos antes de gerar o relatório.")
        return

    mover_arquivos()
    for script in ["1XLSXtoXML.py", "2unirXML.py", "4GerarRelatorio.py"]:
        executar_script(script)
    
    messagebox.showinfo("Sucesso", "Relatório REINF gerado com sucesso!")
    SurgirBotaoBaixar()

# Função para mostrar o botão de download do relatório
def SurgirBotaoBaixar():
    download_button.pack(pady=10)

# Função para realizar o download do arquivo
def fazer_download():
    arquivo_relatorio = "RelatorioGerado/Relatorio.xlsx"  
    if os.path.exists(arquivo_relatorio):
        caminho_destino = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("XLSX", "*.xlsx")])
        if caminho_destino:
            shutil.copy(arquivo_relatorio, caminho_destino)
            messagebox.showinfo("Sucesso", "Relatório baixado com sucesso!")
    else:
        messagebox.showerror("Erro", "O relatório não foi gerado ou não foi encontrado.")

# Configuração da interface gráfica
def criar_interface():
    global label_xml_file, label_xlsx_file, download_button
    root = tk.Tk()
    root.title("Gerador de Relatório REINF")
    root.geometry("400x400")
    root.config(bg="#f0f0f0")

    # Título
    tk.Label(root, text="Gerador de Relatório REINF", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#2c3e50").pack(pady=10)

    # Texto explicativo
    tk.Label(root, text="Selecione os arquivos XML e XLSX", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)

    # Botões para carregar os arquivos
    carregar_xml_button = tk.Button(root, text="Carregar XML", command=carregar_xml, font=("Arial", 12), width=20, bg="#3498db", fg="white", relief="flat", cursor="hand2")
    carregar_xml_button.pack(pady=10)

    label_xml_file = tk.Label(root, text="Nenhum arquivo XML selecionado", font=("Arial", 12), bg="#f0f0f0", fg="#7f8c8d")
    label_xml_file.pack()

    carregar_xlsx_button = tk.Button(root, text="Carregar XLSX", command=carregar_xlsx, font=("Arial", 12), width=20, bg="#3498db", fg="white", relief="flat", cursor="hand2")
    carregar_xlsx_button.pack(pady=10)

    label_xlsx_file = tk.Label(root, text="Nenhum arquivo XLSX selecionado", font=("Arial", 12), bg="#f0f0f0", fg="#7f8c8d")
    label_xlsx_file.pack()

    # Botão para gerar relatório
    gerar_relatorio_button = tk.Button(root, text="Gerar Relatório", command=gerar_relatorio, font=("Arial", 12), width=20, bg="#27ae60", fg="white", relief="flat", cursor="hand2")
    gerar_relatorio_button.pack(pady=20)

    # Botão para baixar o relatório, inicialmente oculto
    download_button = tk.Button(root, text="Baixar Relatório", command=fazer_download, font=("Arial", 12), width=20, bg="#e67e22", fg="white", relief="flat", cursor="hand2")
    download_button.pack_forget()

    tk.Label(root, text="Criado por Renata Veras Venturim", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    criar_interface()