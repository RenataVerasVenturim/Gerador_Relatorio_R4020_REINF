import os
import xml.etree.ElementTree as ET

def unir_xmls():
    # Caminhos para as pastas de entrada
    pasta_extracao_siafi = "ExtracaoSiafi"
    pasta_tesouro_gerencial = "TesouroGerencialDocs"
    
    # Criação da pasta "ArquivosUnidos" caso não exista
    pasta_arquivos_unidos = "ArquivosUnidos"
    os.makedirs(pasta_arquivos_unidos, exist_ok=True)
    
    # Carrega os arquivos XML da pasta "ExtracaoSiafi" e "TesouroGerencialDocs"
    arquivo_siafi = os.listdir(pasta_extracao_siafi)[0]  # Assume que há apenas um arquivo XML
    arquivo_tesouro = os.path.join(pasta_tesouro_gerencial, "dadosTesouro.xml")
    
    # Parse dos arquivos XML
    tree_siafi = ET.parse(os.path.join(pasta_extracao_siafi, arquivo_siafi))
    tree_tesouro = ET.parse(arquivo_tesouro)
    
    # Obtém as raízes dos documentos XML
    root_siafi = tree_siafi.getroot()
    root_tesouro = tree_tesouro.getroot()
    
    # Criar um dicionário para mapear os números NP do arquivo "dadosTesouro.xml"
    np_map = {}
    
    # Iterar sobre todos os elementos <Registro> em dadosTesouro.xml e mapear os <NP> para seus registros
    for registro in root_tesouro.findall(".//Registro"):
        np_value = registro.find("NP").text
        np_map[np_value] = registro
    
    # Iterar sobre todos os <numDH> no arquivo da ExtracaoSiafi e procurar correspondência
    for num_dh in root_siafi.findall(".//numDH"):
        num_dh_value = num_dh.text.strip()  # Pega o valor de <numDH>
        
        # Buscar o valor correspondente de <NP> em dadosTesouro.xml
        if num_dh_value in np_map:
            # Se encontrar, pegar o registro correspondente e adicioná-lo como subelemento de <numDH>
            registro = np_map[num_dh_value]
            
            # Criação do novo elemento <Registro> para adicionar dentro de <numDH>
            registro_element = ET.SubElement(num_dh, "Registro")
            
            # Copiar todos os subelementos de <Registro> para dentro do novo <Registro>
            for element in registro:
                subelement = ET.SubElement(registro_element, element.tag)
                subelement.text = element.text
    
    # Caminho para salvar o novo arquivo consolidado na pasta "ArquivosUnidos"
    novo_arquivo_xml = os.path.join(pasta_arquivos_unidos, "Consolidado_Siafi_Tesouro.xml")
    
    # Salvar o novo arquivo XML com as alterações
    tree_siafi.write(novo_arquivo_xml, encoding="utf-8", xml_declaration=True)
    
    print(f"Arquivo XML consolidado gerado com sucesso: {novo_arquivo_xml}")

if __name__ == "__main__":
    unir_xmls()
