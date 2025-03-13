import xml.etree.ElementTree as ET

def gerar_xml_reinf():
    # Carregar o arquivo Consolidado_Siafi_Tesouro.xml
    tree_siafi = ET.parse('ExtracaoSiafi/Consolidado_Siafi_Tesouro.xml')

    root_siafi = tree_siafi.getroot()
    
    # Criar a estrutura do novo XML baseado no XSD da EFD-Reinf
    namespaces = {
        'xs': 'http://www.w3.org/2001/XMLSchema',
        'ds': 'http://www.w3.org/2000/09/xmldsig#',
        'reinf': 'http://www.reinf.esocial.gov.br/schemas/evt4020PagtoBeneficiarioPJ/v2_01_02'
    }
    
    # Criar o elemento raiz <Reinf>
    reinf = ET.Element('{http://www.reinf.esocial.gov.br/schemas/evt4020PagtoBeneficiarioPJ/v2_01_02}Reinf', 
                       xmlns_ds="http://www.w3.org/2000/09/xmldsig#", 
                       xmlns_xs="http://www.w3.org/2001/XMLSchema", 
                       xmlns="http://www.reinf.esocial.gov.br/schemas/evt4020PagtoBeneficiarioPJ/v2_01_02", 
                       targetNamespace="http://www.reinf.esocial.gov.br/schemas/evt4020PagtoBeneficiarioPJ/v2_01_02",
                       elementFormDefault="qualified", attributeFormDefault="unqualified")
    
    # Criar o elemento <evtRetPJ>
    evt_ret_pj = ET.SubElement(reinf, '{http://www.reinf.esocial.gov.br/schemas/evt4020PagtoBeneficiarioPJ/v2_01_02}evtRetPJ')
    
    # Criar o <ideEvento>
    ide_evento = ET.SubElement(evt_ret_pj, '{http://www.reinf.esocial.gov.br/schemas/evt4020PagtoBeneficiarioPJ/v2_01_02}ideEvento')
    
    # Preencher o <ideEvento> com dados
    ide_evento_id = ET.SubElement(ide_evento, '{http://www.w3.org/2001/XMLSchema}id')
    ide_evento_id.text = "ID1234567890"  # Exemplo de ID único do evento

    # Criar o <ideContri> (Identificação do contribuinte)
    ide_contri = ET.SubElement(evt_ret_pj, '{http://www.reinf.esocial.gov.br/schemas/evt4020PagtoBeneficiarioPJ/v2_01_02}ideContri')
    
    # Preencher os dados de identificação do contribuinte
    ide_contri_nome = ET.SubElement(ide_contri, '{http://www.w3.org/2001/XMLSchema}nome')
    ide_contri_nome.text = "Empresa XYZ LTDA"
    
    # Criar o <ideEstab> (Identificação do estabelecimento)
    ide_estab = ET.SubElement(evt_ret_pj, '{http://www.reinf.esocial.gov.br/schemas/evt4020PagtoBeneficiarioPJ/v2_01_02}ideEstab')
    
    # Preencher os dados de identificação do estabelecimento
    ide_estab_nome = ET.SubElement(ide_estab, '{http://www.w3.org/2001/XMLSchema}nome')
    ide_estab_nome.text = "Estabelecimento XYZ"
    
    # Criar os elementos de <Registro> do arquivo Consolidado_Siafi_Tesouro.xml
    for registro in root_siafi.findall(".//Registro"):  # Supondo que <Registro> seja o elemento de interesse
        np_value = registro.find("NP").text
        
        # Criar o elemento de pagamento de benefício PJ baseado em NP
        pagamento = ET.SubElement(evt_ret_pj, '{http://www.reinf.esocial.gov.br/schemas/evt4020PagtoBeneficiarioPJ/v2_01_02}pagtoBenef')
        
        # Preencher os dados de pagamento
        pagamento_valor = ET.SubElement(pagamento, '{http://www.w3.org/2001/XMLSchema}valor')
        pagamento_valor.text = registro.find("VALOR_OB").text
        
        pagamento_data = ET.SubElement(pagamento, '{http://www.w3.org/2001/XMLSchema}data')
        pagamento_data.text = registro.find("Data_fato_gerador").text
    
    # Salvar o arquivo XML gerado
    tree_reinf = ET.ElementTree(reinf)
    tree_reinf.write("efd_reinf_output.xml", encoding="utf-8", xml_declaration=True)

    print("Arquivo EFD-Reinf gerado com sucesso: efd_reinf_output.xml")

if __name__ == "__main__":
    gerar_xml_reinf()
