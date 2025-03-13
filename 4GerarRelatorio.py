import xml.etree.ElementTree as ET
import openpyxl

# Função para ler o XML
def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    return root

# Função para extrair os dados de interesse do XML
# Função para extrair os dados de interesse do XML
def extract_data_from_xml(root):
    # Inicializar uma lista de registros
    records = []

    # Iterar sobre os elementos que contêm os dados necessários
    for cp in root.findall(".//ns2:CprDhConsultar", namespaces={"ns2": "http://services.docHabil.cpr.siafi.tesouro.fazenda.gov.br/"}):
        # Extrair dados dos registros
        ano_dh = cp.find(".//anoDH").text if cp.find(".//anoDH") is not None else ''
        cod_tipo_dh = cp.find(".//codTipoDH").text if cp.find(".//codTipoDH") is not None else ''
        num_dh = cp.find(".//numDH").text if cp.find(".//numDH") is not None else ''
        data_fato_gerador = cp.find(".//Data_fato_gerador").text if cp.find(".//Data_fato_gerador") is not None else ''
        ob = cp.find(".//OB").text if cp.find(".//OB") is not None else ''
        valor_ob = cp.find(".//VALOR_OB").text if cp.find(".//VALOR_OB") is not None else ''
        cod_sit = cp.find(".//codSit").text if cp.find(".//codSit") is not None else ''
        txt_inscr_a = cp.find(".//txtInscrA").text if cp.find(".//txtInscrA") is not None else ''
        txt_inscr_b = cp.find(".//txtInscrB").text if cp.find(".//txtInscrB") is not None else ''
        cod_recolhedor = cp.find(".//codRecolhedor").text if cp.find(".//codRecolhedor") is not None else ''

        # Agora buscar <vlr> dentro de <itemRecolhimento>
        vlr = ''
        item_recolhimento = cp.find(".//itemRecolhimento")
        if item_recolhimento is not None:
            vlr = item_recolhimento.find(".//vlr").text if item_recolhimento.find(".//vlr") is not None else ''

        vlr_base_calculo = cp.find(".//vlrBaseCalculo").text if cp.find(".//vlrBaseCalculo") is not None else ''
        vlr_multa = cp.find(".//vlrMulta").text if cp.find(".//vlrMulta") is not None else ''
        vlr_juros = cp.find(".//vlrJuros").text if cp.find(".//vlrJuros") is not None else ''
        vlr_outras_ent = cp.find(".//vlrOutrasEnt").text if cp.find(".//vlrOutrasEnt") is not None else ''
        vlr_atm_multa_juros = cp.find(".//vlrAtmMultaJuros").text if cp.find(".//vlrAtmMultaJuros") is not None else ''
        
        # Extrair o conteúdo de <txtObser> dentro de <predoc>
        predoc = cp.find(".//predoc")
        txt_obser = predoc.find(".//txtObser").text if predoc is not None and predoc.find(".//txtObser") is not None else ''
        
        # Adicionar os dados extraídos à lista de registros
        records.append([ano_dh, cod_tipo_dh, num_dh, data_fato_gerador, ob, valor_ob, cod_sit, txt_inscr_a, txt_inscr_b, cod_recolhedor, vlr, vlr_base_calculo, vlr_multa, vlr_juros, vlr_outras_ent, vlr_atm_multa_juros, txt_obser])

    return records

# Função para criar e salvar a planilha Excel
# Função para criar e salvar a planilha Excel com filtro na coluna E
def create_excel(data, output_file):
    # Criar um novo arquivo de planilha
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Extracao SIAFI"
    
    # Adicionar cabeçalhos
    headers = ["Ano DH", "Código Tipo DH", "Num DH", "Data Fato Gerador", "OB", "Valor OB", "Código Sit", 
               "Inscrição A", "Inscrição B", "Código Recolhedor", "Valor", "Valor Base Cálculo", 
               "Valor Multa", "Valor Juros", "Valor Outras Ent", "Valor Atm Multa Juros", "Observação"]
    ws.append(headers)

    # Filtrar dados: Manter apenas linhas onde a coluna E (índice 5) tem valor preenchido
    filtered_data = [record for record in data if record[5]]  # Índice 5 -> "Valor OB"

    # Adicionar os dados filtrados
    for record in filtered_data:
        ws.append(record)

    # Salvar a planilha como .xlsx
    wb.save(output_file)

# Função principal
def main():
    xml_file = "ArquivosUnidos/Consolidado_Siafi_Tesouro.xml"
    output_file = "RelatorioGerado/Extracao_Siafi_Tesouro.xlsx"

    # Ler o XML
    root = parse_xml(xml_file)

    # Extrair os dados
    extracted_data = extract_data_from_xml(root)

    # Criar e salvar o arquivo Excel
    create_excel(extracted_data, output_file)
    print(f"Arquivo {output_file} criado com sucesso!")

if __name__ == "__main__":
    main()
