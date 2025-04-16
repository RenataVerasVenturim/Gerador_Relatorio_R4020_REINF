import subprocess
import time
import os
import tkinter as tk  
from tkinter import messagebox
import shutil 
import sys
import xml.etree.ElementTree as ET
from lxml import etree

messagebox.showwarning("Atenção", "Assine, via Assinador Serpro , todos os xmls gerados que estão em XMLGerados da pasta do programa")

# Caminho do script BAT
caminho_bat = r"C:\Program Files (x86)\Assinador Serpro\signerDesktopAgent.bat"

# Pasta onde estão os XMLs a serem assinados
pasta_xmls = r"C:\Users\PROPPI-RENATA\Desktop\ProgramaREINFWebService\XMLGerados"

# Executa o batch sem bloquear a execução
processo = subprocess.Popen(f'"{caminho_bat}" "{pasta_xmls}"', shell=True)

#-------------------ESVAZIAR PASTA XML Assinados e mover assinados de XMLGerados para esta pasta---------------#
def esvaziar_pasta_xml_assinados():
    pasta_assinados = "XMLAssinados"
    if os.path.exists(pasta_assinados):
        arquivos_removidos = 0
        for arquivo in os.listdir(pasta_assinados):
            caminho_arquivo = os.path.join(pasta_assinados, arquivo)
            try:
                if os.path.isfile(caminho_arquivo):
                    os.remove(caminho_arquivo)  # Remove o arquivo
                    arquivos_removidos += 1
            except Exception as e:
                print(f"Erro ao remover arquivo {arquivo}: {e}")
        
        if arquivos_removidos > 0:
            print(f"Pasta esvaziada, {arquivos_removidos} arquivos removidos.")
        else:
            print("A pasta já está vazia.")
    else:
        print(f"A pasta {pasta_assinados} não existe.")
        


def mover_arquivos_assinados():
    pasta_gerados = "XMLGerados"
    pasta_assinados = "XMLAssinados"
    
    # Verifica se a pasta XMLGerados existe
    if os.path.exists(pasta_gerados):
        for arquivo in os.listdir(pasta_gerados):
            if arquivo.endswith("_assinado.xml"):  # Verifica se o arquivo termina com '_assinado.xml'
                caminho_origem = os.path.join(pasta_gerados, arquivo)
                caminho_destino = os.path.join(pasta_assinados, arquivo)
                try:
                    shutil.move(caminho_origem, caminho_destino)  # Move o arquivo para a pasta XMLAssinados
                    print(f"Arquivo {arquivo} movido para {pasta_assinados}")
                except Exception as e:
                    print(f"Erro ao mover arquivo {arquivo}: {e}")
    else:
        print(f"A pasta {pasta_gerados} não existe.")

def verificar_assinatura_completa():
    pasta_gerados = "XMLGerados"
    pasta_assinados = "XMLAssinados"

    esvaziar_pasta_xml_assinados()

    # Criar a janela de MessageBox
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    while True:
        # Obter o número de arquivos nas pastas
        num_arquivos_gerados = len([f for f in os.listdir(pasta_gerados) if os.path.isfile(os.path.join(pasta_gerados, f))])
        num_arquivos_assinados = len([f for f in os.listdir(pasta_assinados) if os.path.isfile(os.path.join(pasta_assinados, f))])

        print(f"Arquivos totais que devem ser assinados: {num_arquivos_gerados}")
        print(f"Arquivos assinados: {num_arquivos_assinados}")

        # Atualizar a mensagem com a quantidade de arquivos assinados
        if num_arquivos_gerados == num_arquivos_assinados:
            messagebox.showinfo("Status", "Todos os documentos foram assinados")
            break  # Sai do loop se as quantidades forem iguais
        else:
            # Apenas mostra a mensagem de aguarde sem usar messagebox repetidamente
            #messagebox.showinfo("Status",f"Aguarde até a assinatura completa dos arquivos. Assinados: {num_arquivos_assinados}/{num_arquivos_gerados}")           
            # Realiza a movimentação de arquivos
            mover_arquivos_assinados()
            
            # Aguarda um tempo antes de verificar novamente
            time.sleep(5)

# Chamar a função para verificar
verificar_assinatura_completa()

#-------------------VALIDAR XMLs ASSINADOS COM O XSD-------------------#
# Diretórios
xsd_path = "XSD/R-4020-evt4020PagtoBeneficiarioPJ-v2_01_02d.xsd"
xml_dir = "XMLAssinados" 

# Carregar o XSD
with open(xsd_path, "rb") as xsd_file:
    xml_schema_doc = etree.parse(xsd_file)
    xml_schema = etree.XMLSchema(xml_schema_doc)
def validar_xmls_gerados_e_assinados():
    # Iterar sobre os arquivos XML na pasta
    for filename in os.listdir(xml_dir):
        if filename.endswith(".xml") and filename != "LoteEventos.xml":
            xml_path = os.path.join(xml_dir, filename)

            # Carregar o XML
            with open(xml_path, "rb") as xml_file:
                xml_doc = etree.parse(xml_file)

            # Validar o XML contra o XSD
            try:
                # Tentativa de validar
                if xml_schema.validate(xml_doc):
                    print(f"✅ {filename} é válido!")
                else:
                    print(f"❌ {filename} é inválido!")
                    for error in xml_schema.error_log:
                        print(f"  → Linha {error.line}, Coluna {error.column}: {error.message}")

                    # Interromper o código se a validação falhar
                    raise Exception(f"A validação falhou para o arquivo: {filename}. O código será interrompido.")
            except etree.XMLSyntaxError as e:
                print(f"Erro de sintaxe XML no arquivo {filename}: {e}")
                
    print("\nVerificação concluída para todos os arquivos XML de cada evento na pasta 'XMLAssinados'.")

validar_xmls_gerados_e_assinados()