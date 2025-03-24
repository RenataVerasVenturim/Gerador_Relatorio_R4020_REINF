import os
import pandas as pd
import xml.etree.ElementTree as ET

def converter_xlsx_para_xml():
    pasta = "TesouroGerencialDocs"
    arquivo_xlsx = None
    
    # Verifica se a pasta existe
    if not os.path.exists(pasta):
        print(f"Pasta '{pasta}' não encontrada.")
        return
    
    # Busca um arquivo .xlsx na pasta
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".xlsx"):
            arquivo_xlsx = os.path.join(pasta, arquivo)
            break
    
    if not arquivo_xlsx:
        print("Nenhum arquivo .xlsx encontrado na pasta.")
        return
    
    # Lê a planilha a partir da linha 4 (linha 4 é o índice 3 no pandas)
    df = pd.read_excel(arquivo_xlsx, skiprows=3, usecols="A:D")
    
    # Limpar espaços extras nos nomes das colunas
    df.columns = df.columns.str.strip()
    
    # Renomeia as colunas para garantir que sigam a ordem desejada
    df.columns = ["Data do fato gerador", "OB", "NP", "VALOR OB"]
    
    # Verifica as colunas lidas
    print(df.columns)
    
    # Criando a estrutura XML
    root = ET.Element("Dados")
    
    for _, linha in df.iterrows():
        registro = ET.SubElement(root, "Registro")
        
        # Mapeia as colunas para os respectivos elementos XML
        data_fato_gerador = ET.SubElement(registro, "Data_fato_gerador")
        data_fato_gerador.text = str(linha["Data do fato gerador"])
        
        ob = ET.SubElement(registro, "OB")
        ob.text = str(linha["OB"])
        
        np = ET.SubElement(registro, "NP")
        np_texto = str(linha["NP"])

        # Extrai a parte após o "NP" e remove os zeros à esquerda
        if "NP" in np_texto:
            np_numero = np_texto.split("NP")[-1]  # Pega tudo após o "NP"
            np_texto_final = str(int(np_numero))  # Converte para número (remove os zeros à esquerda)
            np.text = np_texto_final
        else:
            np.text = "0"  # Caso não tenha "NP", coloca 0 (caso isso aconteça)
        
        valor_ob = ET.SubElement(registro, "VALOR_OB")
        valor_ob.text = str(linha["VALOR OB"])
    
    # Criar a árvore XML e salvar
    tree = ET.ElementTree(root)
    nome_arquivo_xml = os.path.join(pasta, "dadosTesouro.xml")
    tree.write(nome_arquivo_xml, encoding="utf-8", xml_declaration=True)
    
    print(f"Arquivo XML gerado com sucesso: {nome_arquivo_xml}")

if __name__ == "__main__":
    converter_xlsx_para_xml()
