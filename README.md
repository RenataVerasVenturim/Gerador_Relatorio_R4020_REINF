<h4>
   Este programa gera um relatório reinf com a consolidação do xml gerado na extração siafi web com a relação de OB extraída do Tesouro Gerencial, para lançamento no E-CAC. O arquivo interface_API_REST.py é outro projeto, em desenvolvimento, para envio direto via WebService com API REST e token Dexon de autenticação serpro.
</h4>   
   <ul><h2>Programas necessários:</h2>
     <li>VS CODE</li>
     <li>Python</li>
     <li>Git</li>
   </ul>


Baixar dependências :
<pre>
  <code>
    pip install -r requirements.txt
  </code>
</pre>
  
Gerar autoexecutável:
<pre>
  <code>
pyinstaller --onefile ^
--add-data="1XLSXtoXML.py:." ^
--add-data="2unirXML.py:." ^
--add-data="3ConfrontarXMLcomParametros.py:." ^
--add-data="4GerarRelatorio.py:." ^
--add-data="6AssinarXML.py:." ^
--add-data="7GerarLoteEventosEvalidar.py:." ^
--add-data="8Requisicao.py:." ^
--add-data="interface_API_Rest.py:." ^
--add-data="LICENSE:." ^
--add-data="requirements.txt:." ^
--add-data="xmldsig-core-schema.xsd:." ^
--add-data="ArquivosUnidos/Consolidado_Siafi_Tesouro.xml:ArquivosUnidos" ^
--add-data="ExtracaoSiafi/Mar2025.xml:ExtracaoSiafi" ^
--add-data="RelatorioGerado/Relatorio.xlsx:RelatorioGerado" ^
--add-data="TesouroGerencialDocs/dadosTesouro.xml:TesouroGerencialDocs" ^
--add-data="TesouroGerencialDocs/Ordens Bancárias REINF.xlsx:TesouroGerencialDocs" ^
--add-data="XMLAssinados/1_ID5114486698708603551045259904862088_assinado.xml:XMLAssinados" ^
--add-data="XMLGerados/1_ID6847077064268710446788492188261396.xml:XMLGerados" ^
--add-data="XSD/envioLoteEventosAssincrono-v1_00_00.xsd:XSD" ^
--add-data="XSD/R-4020-evt4020PagtoBeneficiarioPJ-v2_01_02d_SemSignature.xsd:XSD" ^
--add-data="XSD/R-4020-evt4020PagtoBeneficiarioPJ-v2_01_02d.xsd:XSD" ^
--add-data="XSD/xmldsig-core-schema.xsd:XSD" ^
interface.py

  </code>
</pre>
