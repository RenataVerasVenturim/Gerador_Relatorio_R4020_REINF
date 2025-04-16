# Validação de XML em relação ao XSD feito em fase de teste em: https://www.freeformatter.com/xml-validator-xsd.html
# Verificação da árvore (tree) do XML, foi utilizado : https://myxml.in/xml-treeview.html
# Verificação da árvore(tree) do XSD, foi utilizado: https://myxml.in/xsd-treeview.html

import xml.etree.ElementTree as ET
from datetime import datetime
import random
import os
from xml.dom.minidom import parseString
from lxml import etree
import sys
#--------------------------PREENCHER MANUALMENTE------------------------------------#


# Verificar se os parâmetros foram passados corretamente
if len(sys.argv) < 3:
    print("Erro: CNPJ e Período de Apuração não fornecidos.")
    sys.exit(1)

# Obtendo os valores passados como argumentos
CnpjUnidade = sys.argv[1]
per_apur = sys.argv[2]

# Agora você pode usar CnpjUnidade e per_apur no restante do script
print(f"CNPJ: {CnpjUnidade}")
print(f"Período de Apuração: {per_apur}")

# Resto do seu código que usa essas variáveis

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

        codCredorDevedor = evento.find(".//dadosBasicos/codCredorDevedor", namespaces).text if evento.find(".//dadosBasicos/codCredorDevedor", namespaces) is not None else None

        # Agora você pode usá-lo corretamente em nrInscEstab
        eventos.append({
            "codCredorDevedor": codCredorDevedor,  # Definindo corretamente codCredorDevedor
            "nrInscEstab": cod_recolhedor.text.zfill(14) if cod_recolhedor is not None else codCredorDevedor,
            "cnpjBenef":cod_recolhedor.text.zfill(14) if cod_recolhedor is not None else codCredorDevedor,
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
    # Verificar se o evento tem retenção antes de gerar o XML
    if float(dados["vlrBaseAgreg"].replace(",", ".")) <= 0 or float(dados["vlrAgreg"].replace(",", ".")) <= 0:
        print(f"Evento sem retenção, não gerado para o CNPJ: {dados['cnpjBenef']}!")
        return None, None  # Retorna None se não houver retenção

    evento_id = gerar_id_evtRetPJ()
    reinf = ET.Element("Reinf", {        
        "xmlns:ds": "http://www.w3.org/2000/09/xmldsig#",
        "xmlns": "http://www.reinf.esocial.gov.br/schemas/evt4020PagtoBeneficiarioPJ/v2_01_02"  # Namespace default
    })
    
    evtRetPJ = ET.SubElement(reinf, "evtRetPJ", {"id": evento_id})

    ideEvento = ET.SubElement(evtRetPJ, "ideEvento")
    ET.SubElement(ideEvento, "indRetif").text = dados["indRetif"]
    ET.SubElement(ideEvento, "perApur").text = per_apur
    ET.SubElement(ideEvento, "tpAmb").text = "1"  # 1=Produção; 2=Pré-produção
    ET.SubElement(ideEvento, "procEmi").text = "2"  #1 - Aplicativo do contribuinte; 2 - Aplicativo governamental.
    ET.SubElement(ideEvento, "verProc").text = "REINF.Web"  # Versão do processo

    ideContri = ET.SubElement(evtRetPJ, "ideContri")
    ET.SubElement(ideContri, "tpInsc").text = "1"
    ET.SubElement(ideContri, "nrInsc").text = dados["nrInsc"]

    ideEstab = ET.SubElement(evtRetPJ, "ideEstab")
    ET.SubElement(ideEstab, "tpInscEstab").text = "1"
    ET.SubElement(ideEstab, "nrInscEstab").text = dados["nrInscEstab"]

    ideBenef = ET.SubElement(ideEstab, "ideBenef")
    ET.SubElement(ideBenef, "cnpjBenef").text = dados["cnpjBenef"]
    idePgto = ET.SubElement(ideBenef, "idePgto")
    ET.SubElement(idePgto, "natRend").text = dados["natRend"]

    infoPgto = ET.SubElement(idePgto, "infoPgto")
    ET.SubElement(infoPgto, "dtFG").text = dados["dtFG"]
    ET.SubElement(infoPgto, "vlrBruto").text = dados["vlrBruto"]
    ET.SubElement(infoPgto, "observ").text = dados["observ"]
    
    # Apenas adicionar retenções se houver valores maiores que zero
    retencoes = ET.SubElement(infoPgto, "retencoes")
    ET.SubElement(retencoes, "vlrBaseAgreg").text = dados["vlrBaseAgreg"]
    ET.SubElement(retencoes, "vlrAgreg").text = dados["vlrAgreg"]

    # Serialização
    #reinf_str = parseString(ET.tostring(reinf, encoding="unicode")).toprettyxml(indent="  ", newl="")
    xml_bytes = ET.tostring(reinf, encoding="utf-8")
    reinf_str = parseString(xml_bytes).toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")

    return reinf_str, evento_id

# Caminho do XML de origem
xml_path = "ArquivosUnidos/Consolidado_Siafi_Tesouro.xml"

def Agregar(eventos):
    eventos_agrupados = {}

    # Agrupar eventos por nrInscEstab
    for evento in eventos:
        chave = evento["cnpjBenef"]
        if chave not in eventos_agrupados:
            eventos_agrupados[chave] = {}

        # Agrupar também por natRend
        nat_rend = evento["natRend"]
        if nat_rend not in eventos_agrupados[chave]:
            eventos_agrupados[chave][nat_rend] = {
                "nrInscEstab": evento["nrInscEstab"],
                "nrInsc": evento["nrInsc"],
                "dtAcor": evento["dtAcor"],
                "indRetif": evento["indRetif"],
                "cnpjBenef":evento["cnpjBenef"],
                "natRend": nat_rend,
                "dtFG": evento["dtFG"],
                "vlrBaseAgreg": float(evento["vlrBaseAgreg"].replace(",", ".")),
                "vlrAgreg": float(evento["vlrAgreg"].replace(",", ".")),
                "vlrBruto": float(evento["vlrBruto"].replace(",", ".")),
                "observ": evento["observ"]
            }
        else:
            # Se já existe o natRend, somar os valores
            eventos_agrupados[chave][nat_rend]["vlrBaseAgreg"] += float(evento["vlrBaseAgreg"].replace(",", "."))
            eventos_agrupados[chave][nat_rend]["vlrAgreg"] += float(evento["vlrAgreg"].replace(",", "."))
            eventos_agrupados[chave][nat_rend]["vlrBruto"] += float(evento["vlrBruto"].replace(",", "."))
            eventos_agrupados[chave][nat_rend]["observ"] = "RECOLHIMENTO DE TRIBUTOS FEDERAIS SOBRE 2 OU MAIS NF-Es, EM ATENDIMENTO A IN/RFB 1234/2012."

    eventos_processados = []

    # Combina os eventos agrupados por nrInscEstab e natRend
    for cnpjBenef, nat_rend_dict in eventos_agrupados.items():
        for nat_rend, dados in nat_rend_dict.items():
            eventos_processados.append(dados)

    # Formatar valores numéricos para cada evento
    for evento in eventos_processados:
        evento["vlrBaseAgreg"] = formatar_valor(evento["vlrBaseAgreg"])
        evento["vlrAgreg"] = formatar_valor(evento["vlrAgreg"])
        evento["vlrBruto"] = formatar_valor(evento["vlrBruto"])

    return eventos_processados

# Extração e processamento
eventos = Agregar(extrair_dados_siafi(xml_path))

for i, dados in enumerate(eventos, start=1):
    xml_reinf, evento_id = gerar_xml_reinf(dados, per_apur)
    
    if xml_reinf is None:  # Ignora eventos sem retenção
        continue

    file_name = f"{output_dir}/{i}_{evento_id}.xml"

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(xml_reinf)

    print(f"XML gerado: {file_name}")


print("\nTodos os XMLs foram gerados com sucesso e salvos em 'XMLGerados'!")

#-----------------------------------------------------------------------------------#

#--Validar XML de cada evento com base nos parâmetros do XSD REINF------------------#

# Diretórios
xsd_path = "XSD/R-4020-evt4020PagtoBeneficiarioPJ-v2_01_02d_SemSignature.xsd"
xml_dir = "XMLGerados" 

# Carregar o XSD
with open(xsd_path, "rb") as xsd_file:
    xml_schema_doc = etree.parse(xsd_file)
    xml_schema = etree.XMLSchema(xml_schema_doc)

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
            
print("\nVerificação concluída para todos os arquivos XML de cada evento na pasta 'XMLGerados'.")

#-----------------------------------------------------------------------------------#
