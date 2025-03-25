
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
    pyinstaller --onefile --add-data "1XLSXtoXML.py;." --add-data "2unirXML.py;." --add-data "3ConfrontarXMLcomParametros.py;." --add-data "4GerarRelatorio.py;." --add-data "interface.py;." --add-data "LICENSE;." --add-data "requirements.txt;." --add-data "ArquivosUnidos/Consolidado_Siafi_Tesouro.xml;ArquivosUnidos" --add-data "ExtracaoSiafi/dez.2024.xml;ExtracaoSiafi" --add-data "RelatorioGerado/Relatorio.xlsx;RelatorioGerado" --add-data "TesouroGerencialDocs/dadosTesouro.xml;TesouroGerencialDocs" --add-data "TesouroGerencialDocs/Ordens Bancárias REINF.xlsx;TesouroGerencialDocs" --add-data "XSD/envioLoteEventosAssincrono-v1_00_00.xsd;XSD" --add-data "XSD/R-4020-evt4020PagtoBeneficiarioPJ-v2_01_02d.xsd;XSD"--add-data "XMLGerados/1_ID4595902373754770570610153440585285.xml;XMLGerados" interface.py
  </code>
</pre>
