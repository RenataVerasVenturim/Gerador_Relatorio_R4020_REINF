import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import subprocess
import re

# Variáveis globais
xml_file_path = None
xlsx_file_path = None
root = None
download_button = None
gerarlote_button = None
CnpjUnidade = None
per_apur = None

# Função para carregar o arquivo XML
def carregar_xml():
    global xml_file_path
    xml_file_path = filedialog.askopenfilename(filetypes=[("Arquivos XML", "*.xml")])
    if xml_file_path:
        label_xml_file.config(text=f"Arquivo XML: {os.path.basename(xml_file_path)}")
    else:
        label_xml_file.config(text="Nenhum arquivo XML selecionado")

# Função para carregar o arquivo XLSX
def carregar_xlsx():
    global xlsx_file_path
    xlsx_file_path = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])
    if xlsx_file_path:
        label_xlsx_file.config(text=f"Arquivo XLSX: {os.path.basename(xlsx_file_path)}")
    else:
        label_xlsx_file.config(text="Nenhum arquivo XLSX selecionado")

# Função para obter valores do CNPJ e Período de Apuração
def obter_valores_manualmente():
    global CnpjUnidade, per_apur
    CnpjUnidade = entry_cnpj.get()  # Pega o valor do CNPJ
    per_apur = entry_periodo.get()  # Pega o valor do Período de Apuração

    if not CnpjUnidade or not per_apur:
        messagebox.showerror("Erro", "Por favor, preencha tanto o CNPJ quanto o período de apuração.")
    elif not validar_periodo(per_apur):
        messagebox.showerror("Erro", "Período de apuração inválido. Deve ser AAAA-mm")
    elif not validar_cnpj(CnpjUnidade):
        messagebox.showerror("Erro", "CNPJ inválido. Deve ser sem '- / .' e com 8, 11 ou 14 dígitos.")
    else:
        messagebox.showinfo("Sucesso", "Valores atualizados com sucesso!")


# Função para executar scripts
def executar_script(script_name, cnpj, periodo):
    try:
        # Executa o script passando os parâmetros necessários
        subprocess.run(["python", script_name, cnpj, periodo], check=True)
        
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Erro ao executar o script {script_name}: {e}")

# Função para mover os arquivos para as pastas corretas
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

# Função para limpar a pasta SIAFI
def limpar_pasta_siafi():
    diretorio = "ExtracaoSiafi"
    if os.path.exists(diretorio):
        for arquivo in os.listdir(diretorio):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            try:
                os.remove(caminho_arquivo) if os.path.isfile(caminho_arquivo) else shutil.rmtree(caminho_arquivo)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao limpar a pasta 'ExtracaoSiafi': {e}")

# Função para gerar os arquivos XML
def gerar_XML():
    if not CnpjUnidade or not per_apur:
        messagebox.showerror("Erro", "Por favor, preencha tanto o CNPJ quanto o período de apuração.")
        return  # Impede a execução do código abaixo, se CNPJ ou período não forem preenchidos
    

    if not validar_cnpj(CnpjUnidade):
        messagebox.showerror("Erro", "CNPJ inválido.")
        return
    
    if not validar_periodo(per_apur):
        messagebox.showerror("Erro", "Período de apuração inválido.")
        return
    
    if not xml_file_path or not xlsx_file_path:
        messagebox.showerror("Erro", "Carregue ambos os arquivos antes de gerar o XML para REINF.")
        return

    mover_arquivos()

    # Passando os valores de CnpjUnidade e per_apur ao chamar o script
    for script in ["1XLSXtoXML.py", "2unirXML.py", "3ConfrontarXMLcomParametros.py", "6AssinarXML.py"]:
        executar_script(script, CnpjUnidade, per_apur)
    
    aguardar_confirmacao()


# Função para aguardar confirmação do usuário
def aguardar_confirmacao():
    SurgirBotaoGerarLoteEventos()

# Função para gerar o lote de eventos

def fazer_LoteEventos():
    executar_script("7GerarLoteEventosEvalidar.py", CnpjUnidade, per_apur)
    SurgirBotaoBaixar()

# Função para fazer o download do arquivo gerado
def fazer_download():
    arquivo_Lote_Eventos = "XMLAssinados/LoteEventos.xml"
    if os.path.exists(arquivo_Lote_Eventos):
        caminho_destino = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML", "*.xml")])
        if caminho_destino:
            shutil.copy(arquivo_Lote_Eventos, caminho_destino)
            messagebox.showinfo("Sucesso", "Arquivo baixado com sucesso!")
    else:
        messagebox.showerror("Erro", "O arquivo não foi gerado ou não foi encontrado.")

# Função para exibir o botão de download
def SurgirBotaoBaixar():
    global root, download_button
    if root and download_button:
        download_button.pack(pady=10)
        root.update_idletasks()
        root.geometry(f"400x{root.winfo_reqheight()}") 

# Função para exibir o botão para gerar o lote de eventos
def SurgirBotaoGerarLoteEventos():
    global gerarlote_button
    if gerarlote_button:
        gerarlote_button.pack(pady=10)
        root.update_idletasks()  # Atualiza o layout da interface
        root.geometry(f"400x{root.winfo_reqheight()}") 

# Função para validar o CNPJ
def validar_cnpj(cnpj):
    # Expressão regular para validar CNPJ: 8, 11 ou 14 dígitos numéricos
    pattern = r"^[0-9]{8}$|^[0-9]{11}$|^[0-9]{14}$"
    return re.match(pattern, cnpj) is not None

# Função para validar o período de apuração
def validar_periodo(periodo):
    # Expressão regular para validar o formato de ano e mês: 2024-12
    pattern = r"^20([1-9][0-9])-(0[1-9]|1[0-2])$"
    return re.match(pattern, periodo) is not None
def validar_cnpj(P):
    # Remove qualquer caractere que não seja número
    P = ''.join(filter(str.isdigit, P))
    
    # Limita o tamanho do CNPJ para 14 caracteres
    if len(P) <= 14:
        return P
    return None
# Função para criar a interface gráfica
def criar_interface():
    global label_xml_file, label_xlsx_file, download_button, gerarlote_button, root, entry_cnpj, entry_periodo
    root = tk.Tk()  # Inicializa a interface gráfica
    root.title("Gerador de Lote de eventos REINF")
    root.geometry("400x600")
    root.config(bg="#f0f0f0")

    tk.Label(root, text="Gerador de Lote de eventos REINF", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#2c3e50").pack(pady=10)
    tk.Label(root, text="Selecione os arquivos extraídos", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)

    tk.Button(root, text="📁 Selecionar Arquivo SIAFI", command=carregar_xml, font=("Arial", 12), width=30, bg="#3498db", fg="white", relief="flat").pack(pady=10)
    label_xml_file = tk.Label(root, text="Nenhum arquivo XML selecionado", font=("Arial", 12), bg="#f0f0f0", fg="#7f8c8d")
    label_xml_file.pack()

    tk.Button(root, text="📁 Selecionar Arquivo Tesouro Gerencial", command=carregar_xlsx, font=("Arial", 12), width=32, bg="#3498db", fg="white", relief="flat").pack(pady=10)
    label_xlsx_file = tk.Label(root, text="Nenhum arquivo XLSX selecionado", font=("Arial", 12), bg="#f0f0f0", fg="#7f8c8d")
    label_xlsx_file.pack()
   
    vcmd_cnpj = root.register(validar_cnpj)

    # Inicializar o CNPJ
    CnpjUnidade = "28523215" # naõ precisa colocar cnpj completo '28523215003393'
    perApurManual = "2025-01"

    frame_secao = tk.Frame(root, bg="#e0e0e0", padx=20, pady=15)  # Fundo levemente diferente
    frame_secao.pack(pady=20, padx=20, fill="both", expand=True)

    # Campo CNPJ
    tk.Label(frame_secao, text="CNPJ da Unidade UFF", font=("Arial", 12), bg="#e0e0e0").pack(pady=5)
    entry_cnpj = tk.Entry(frame_secao, font=("Arial", 12), width=30)
    entry_cnpj.insert(0, CnpjUnidade)
    entry_cnpj.pack(pady=5)

    # Campo Período de Apuração
    tk.Label(frame_secao, text="Período de Apuração", font=("Arial", 12), bg="#e0e0e0").pack(pady=5)
    entry_periodo = tk.Entry(frame_secao, font=("Arial", 12), width=30)
    entry_periodo.insert(0, perApurManual)
    entry_periodo.pack(pady=5)

    # Botão de Salvar dentro da seção
    tk.Button(frame_secao, text="Salvar", command=obter_valores_manualmente,font=("Arial", 12), bg="#27ae60", fg="white", relief="flat").pack(pady=10)

    # Botões de gerar XML
    tk.Button(root, text="Gerar XMLs dos eventos", command=gerar_XML, font=("Arial", 12), width=20, bg="#e67e22", fg="white", relief="flat").pack(pady=5)
   
    gerarlote_button = tk.Button(root, text="Gerar Lote de eventos", command=fazer_LoteEventos, font=("Arial", 12), width=20, bg="#e67e22", fg="white", relief="flat")
    gerarlote_button.pack_forget()

    download_button = tk.Button(root, text="Baixar Lote de Eventos", command=fazer_download, font=("Arial", 12), width=20, bg="#e67e22", fg="white", relief="flat")
    download_button.pack_forget()

    tk.Label(root, text="Criado por Renata Veras Venturim", font=("Arial", 10), bg="#f0f0f0").pack(side="bottom", pady=5)
    root.mainloop()

# Executar a interface gráfica
criar_interface()
