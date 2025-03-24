# Validação de XML em relação ao XSD feito em fase de teste em: https://www.freeformatter.com/xml-validator-xsd.html
# Verificação da árvore (tree) do XML, foi utilizado : https://myxml.in/xml-treeview.html
# Verificação da árvore(tree) do XSD, foi utilizado: https://myxml.in/xsd-treeview.html

import xml.etree.ElementTree as ET
from datetime import datetime
import random
import os
from xml.dom.minidom import parseString
from lxml import etree

#--------------------------PREENCHER MANUALMENTE------------------------------------#
CnpjUnidade = "28523215003393"  # CNPJ manual
per_apur = "2024-12"  # Período de apuração manual
#-----------------------------------------------------------------------------------#

# Criar pasta se não existir
output_dir = "XMLGerados"
os.makedirs(output_dir, exist_ok=True)

# Esvaziar a pasta "XMLGerados"
for arquivo in os.listdir(output_dir):
    caminho_arquivo = os.path.join(output_dir, arquivo)
    if os.path.isfile(caminho_arquivo):
        os.remove(caminho_arquivo)

# Função para formatar valores numéricos corretamente
def formatar_valor(valor):
    try:
        valor_float = float(valor)
        return f"{valor_float:.2f}".replace(".", ",")
    except ValueError:
        return "0,00"

# Função para gerar um ID único para o evento
def gerar_id_evtRetPJ():
    return "ID" + "".join([str(random.randint(0, 9)) for _ in range(34)])

# Função para extrair dados do XML SIAFI
def extrair_dados_siafi(xml_path):
    namespaces = {
        'reinf': 'http://www.reinf.esocial.gov.br/schemas/evt4020PagtoBeneficiarioPJ/v2_01_02',
        'ns2': 'http://services.docHabil.cpr.siafi.tesouro.fazenda.gov.br/'
    }
    
    tree = ET.parse(xml_path)
    root = tree.getroot()
    eventos = []

    for evento in root.findall(".//ns2:CprDhConsultar", namespaces):
        if evento.find(".//OB", namespaces) is None:
            continue  # Ignora eventos sem <OB>

        cod_recolhedor = evento.find(".//deducao/itemRecolhimento/codRecolhedor", namespaces)
        nr_insc = CnpjUnidade    
        data_fato_gerador = evento.find(".//numDH/Registro/Data_fato_gerador", namespaces)
        data_fato_gerador = data_fato_gerador.text.strip() if data_fato_gerador is not None else ""

        if data_fato_gerador:
            try:
                data_fato_gerador = datetime.strptime(data_fato_gerador, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Formato de data inválido: {data_fato_gerador}. Deve estar no formato YYYY-MM-DD.")

        txt_inscrB = evento.find(".//deducao/txtInscrB", namespaces)
        nat_rend = txt_inscrB.text if txt_inscrB is not None else "Não há retenção neste evento."
        vlr_base_calculo = evento.find(".//deducao/itemRecolhimento/vlrBaseCalculo", namespaces)
        vlr_base_calculo = vlr_base_calculo.text if vlr_base_calculo is not None else "0,00"
        vlr = evento.find(".//deducao/itemRecolhimento/vlr", namespaces)
        vlr = vlr.text if vlr is not None else "0,00"
        bruto = vlr_base_calculo if vlr_base_calculo is not None else "0,00"
        txt_obser = evento.find(".//deducao/predoc/txtObser", namespaces)
        txt_obser2 = evento.find(".//dadosPgto/predoc/txtObser", namespaces)
        observ = txt_obser.text[:200] if txt_obser is not None else (txt_obser2.text[:200] if txt_obser2 is not None else "")

        eventos.append({ 
            "nrInscEstab": cod_recolhedor.text.zfill(14) if cod_recolhedor is not None else "00000000000000",
            "nrInsc": nr_insc,
            "dtAcor": data_fato_gerador,
            "indRetif": "1",
            "natRend": nat_rend,
            "dtFG": data_fato_gerador,
            "vlrBaseAgreg": formatar_valor(vlr_base_calculo),
            "vlrAgreg": formatar_valor(vlr),
            "vlrBruto": formatar_valor(bruto),
            "observ": observ
        })

    return eventos

# Função para gerar XML REINF individualmente para cada evento
def gerar_xml_reinf(dados, per_apur):
    evento_id = gerar_id_evtRetPJ()
    reinf = ET.Element("Reinf", {        
        "xmlns:ds": "http://www.w3.org/2000/09/xmldsig#",
        "xmlns": "http://www.reinf.esocial.gov.br/schemas/evt4020PagtoBeneficiarioPJ/v2_01_02"  # Namespace default
    })
    
    evtRetPJ = ET.SubElement(reinf, "evtRetPJ", {"id": evento_id})

    ideEvento = ET.SubElement(evtRetPJ, "ideEvento")
    ET.SubElement(ideEvento, "indRetif").text = dados["indRetif"]
    ET.SubElement(ideEvento, "perApur").text = per_apur
    ET.SubElement(ideEvento, "tpAmb").text = "2"  # Ambiente de teste
    ET.SubElement(ideEvento, "procEmi").text = "1"  # Processo emissor
    ET.SubElement(ideEvento, "verProc").text = "1.0.0"  # Versão do processo

    ideContri = ET.SubElement(evtRetPJ, "ideContri")
    ET.SubElement(ideContri, "tpInsc").text = "1"
    ET.SubElement(ideContri, "nrInsc").text = dados["nrInsc"]

    ideEstab = ET.SubElement(evtRetPJ, "ideEstab")
    ET.SubElement(ideEstab, "tpInscEstab").text = "1"
    ET.SubElement(ideEstab, "nrInscEstab").text = dados["nrInscEstab"]

    ideBenef = ET.SubElement(ideEstab, "ideBenef")
    idePgto = ET.SubElement(ideBenef, "idePgto")
    ET.SubElement(idePgto, "natRend").text = dados["natRend"]

    infoPgto = ET.SubElement(idePgto, "infoPgto")
    ET.SubElement(infoPgto, "dtFG").text = dados["dtFG"]
    ET.SubElement(infoPgto, "vlrBruto").text = dados["vlrBruto"]
    ET.SubElement(infoPgto, "observ").text = dados["observ"]

    retencoes = ET.SubElement(infoPgto, "retencoes")
    ET.SubElement(retencoes, "vlrBaseAgreg").text = dados["vlrBaseAgreg"]
    ET.SubElement(retencoes, "vlrAgreg").text = dados["vlrAgreg"]

    # Serialização
    reinf_str = parseString(ET.tostring(reinf, encoding="unicode")).toprettyxml(indent="  ")
    return reinf_str, evento_id

# Caminho do XML de origem
xml_path = "ArquivosUnidos/Consolidado_Siafi_Tesouro.xml"

# Extração e processamento
eventos = extrair_dados_siafi(xml_path)

for i, dados in enumerate(eventos, start=1):
    xml_reinf, evento_id = gerar_xml_reinf(dados, per_apur)
    file_name = f"{output_dir}/{i}_{evento_id}.xml"

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(xml_reinf)

    print(f"XML gerado: {file_name}")

print("\nTodos os XMLs foram gerados com sucesso e salvos em 'XMLGerados'!")

#-----------------------------------------------------------------------------------#

#--Validar XML de cada evento com base nos parâmetros do XSD REINF------------------#

# Diretórios
xsd_path = "XSD/R-4020-evt4020PagtoBeneficiarioPJ-v2_01_02d.xsd"
xml_dir = "XMLGerados"

# Carregar o esquema XSD
with open(xsd_path, "rb") as xsd_file:
    xsd_doc = etree.parse(xsd_file)
    xml_schema = etree.XMLSchema(xsd_doc)

# Iterar sobre os arquivos XML na pasta "Iterar"
for filename in os.listdir(xml_dir):
    if filename.endswith(".xml") and filename != "LoteEventos.xml":
        xml_path = os.path.join(xml_dir, filename)

        # Carregar o XML
        with open(xml_path, "rb") as xml_file:
            xml_doc = etree.parse(xml_file)

        # Validar o XML contra o XSD
        if xml_schema.validate(xml_doc):
            print(f"✅ {filename} é válido!")
        else:
            print(f"❌ {filename} é inválido!")
            for error in xml_schema.error_log:
                print(f"  → Linha {error.line}, Coluna {error.column}: {error.message}")
            
            # Interromper o código se a validação falhar
            raise Exception(f"A validação falhou para o arquivo: {filename}. O código será interrompido.")

print("\nVerificação concluída para todos os arquivos XML de cada evento na pasta 'XMLGerados'.")

#-----------------------------------------------------------------------------------#
#---------------------------CRIAR LOTE DE EVENTOS-----------------------------------#

# Diretórios
xml_dir = "XMLGerados"
output_lote = "XMLGerados/LoteEventos.xml"

# Dados do contribuinte
CnpjUnidade = "12345678000199"  # Substitua pelo CNPJ correto

# Criar o elemento Reinf principal (lote de eventos) com o namespace correto
# Criar o elemento Reinf principal (lote de eventos) com o namespace correto
reinf_lote = ET.Element("Reinf", {
    "xmlns": "http://www.reinf.esocial.gov.br/schemas/envioLoteEventosAssincrono/v1_00_00",
    "xmlns:xs": "http://www.w3.org/2001/XMLSchema-instance",
    "xmlns:reinf": "http://www.reinf.esocial.gov.br/schemas/envioLoteEventosAssincrono/v1_00_00"  # Namespace adicional
})

# Criar envioLoteEventos dentro do Reinf principal
envio_lote = ET.SubElement(reinf_lote, "envioLoteEventos")

# Criar ideContribuinte dentro de envioLoteEventos
ide_contribuinte = ET.SubElement(envio_lote, "ideContribuinte")
ET.SubElement(ide_contribuinte, "tpInsc").text = "1"  # Tipo de inscrição (1 = CNPJ)
ET.SubElement(ide_contribuinte, "nrInsc").text = CnpjUnidade  # CNPJ informado

# Criar elemento <eventos> dentro de <envioLoteEventos>
eventos = ET.SubElement(envio_lote, "eventos")

# Iterar sobre os XMLs individuais e adicioná-los ao lote
for filename in os.listdir(xml_dir):
    if filename.endswith(".xml") and filename != "LoteEventos.xml":
        xml_path = os.path.join(xml_dir, filename)

        # Carregar o XML do evento
        with open(xml_path, "r", encoding="utf-8") as xml_file:
            xml_content = xml_file.read()

        # Remover a declaração XML do evento (<?xml version="1.0" encoding="UTF-8"?>)
        xml_content = xml_content.split("?>", 1)[-1].strip()

        # Adicionar o evento diretamente no lote como <evento>
        evento_element = ET.fromstring(xml_content)

        # Criar o elemento <evento> dentro de <eventos>
        evento = ET.SubElement(eventos, "evento", {
            "Id": gerar_id_evtRetPJ()  # Gerar o ID único para cada evento
        })
        
        # Adicionar o conteúdo do evento dentro do <evento> em <xs:any>
        any_element = ET.SubElement(evento, "{http://www.w3.org/2001/XMLSchema-instance}any")
        any_element.append(evento_element)  # Adiciona o conteúdo do evento dentro de <xs:any>

# Gerar XML formatado do lote
xml_lote_pretty = parseString(ET.tostring(reinf_lote, encoding="unicode")).toprettyxml(indent="  ")

# Salvar o XML do lote
with open(output_lote, "w", encoding="utf-8") as f:
    f.write(xml_lote_pretty)

print(f"Lote de eventos gerado com sucesso: {output_lote}")

#-----------------------------------------------------------------------------------#
#--------------------VALIDAÇÃO DO LOTE DE EVENTOS CONTRA XSD-----------------------#

def validar_xml(xml_path, xsd_path):
    try:
        # Carregar o esquema XSD
        with open(xsd_path, 'rb') as xsd_file:
            xsd_doc = etree.parse(xsd_file)
            xml_schema = etree.XMLSchema(xsd_doc)
            
        # Carregar o documento XML
        with open(xml_path, 'rb') as xml_file:
            xml_doc = etree.parse(xml_file)
            
        # Validar o XML
        if xml_schema.validate(xml_doc):
            print("O XML do Lote de Eventos está válido de acordo com o XSD.")
        else:
            # Exibir erros de validação se houver
            print("O XML do Lote de Eventos não está válido. Erros encontrados:")
            for error in xml_schema.error_log:
                print(error.message)

    except etree.XMLSyntaxError as e:
        print(f"Erro de sintaxe XML: {e}")
    except etree.DocumentInvalid as e:
        print(f"Erro de validação XML: {e}")

# Caminhos para o XML e XSD
xml_path = "XMLGerados/LoteEventos.xml"
xsd_path = "XSD/envioLoteEventosAssincrono-v1_00_00.xsd"

# Validar o XML contra o XSD
validar_xml(xml_path, xsd_path)

#-----------------------------------------------------------------------------------#
