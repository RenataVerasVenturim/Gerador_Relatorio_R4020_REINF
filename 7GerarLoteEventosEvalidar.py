import xml.etree.ElementTree as ET
from datetime import datetime
import random
import os
from xml.dom.minidom import parseString
from lxml import etree
import shutil  
import tkinter as tk  
from tkinter import messagebox
import time

#-----------------------------------------------------------------------------------#
#---------------------------CRIAR LOTE DE EVENTOS-----------------------------------#
# Função para gerar um ID único para o evento
def gerar_id_evtRetPJ():
    return "ID" + "".join([str(random.randint(0, 9)) for _ in range(34)])
    
# Diretórios
xml_dir = "XMLAssinados"
output_lote = "XMLAssinados/LoteEventos.xml"

# Dados do contribuinte
CnpjUnidade = "28523215003393"

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
            messagebox.showinfo("Validação XML", "Lote de eventos gerado com sucesso! O XML do Lote de Eventos está válido de acordo com o XSD.")
        else:
            print("O XML do Lote de Eventos não está válido. Erros encontrados:")
            messagebox.showinfo("Validação XML", "Lote de eventos gerado com sucesso! O XML do Lote de Eventos NÃO está válido de acordo com o XSD.")
            for error in xml_schema.error_log:
                print(error.message)

    except etree.XMLSyntaxError as e:
        print(f"Erro de sintaxe XML: {e}")
    except etree.DocumentInvalid as e:
        print(f"Erro de validação XML: {e}")

# Caminhos para o XML e XSD
xml_path = "XMLAssinados/LoteEventos.xml"
xsd_path = "XSD/envioLoteEventosAssincrono-v1_00_00.xsd"

# Validar o XML contra o XSD
validar_xml(xml_path, xsd_path)

#-----------------------------------------------------------------------------------#
