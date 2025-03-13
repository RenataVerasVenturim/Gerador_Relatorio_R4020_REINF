#GERADOR DE RELATÓRIO PARA LANÇAMENTOS R-4020 NO REINF , E-CAC

<h2>
  <b>Necessário:</b>
</h2>
<ul>
  <p>Python</p>
  <p>Vs Code</p>
  <p>Git</p>  
</ul>
<h2>
  <b>
    Comandos para geração de um app autoexecutável:
  </b>
</h2>
<p>
  baixar bibliotecas:
</p>
<b>pip install -r requirements.txt</b>
<p>
  Gerar autoexecutável:
</p>
<b>pyinstaller --onefile --add-data "ArquivosUnidos/Consolidado_Siafi_Tesouro.xml;ArquivosUnidos" --add-data "ExtracaoSiafi/153248DDHU771151-00001.xml;ExtracaoSiafi" --add-data "RelatorioGerado/Extracao_Siafi_Tesouro.xlsx;RelatorioGerado" --add-data "TesouroGerencialDocs/dadosTesouro.xml;TesouroGerencialDocs" --add-data "TesouroGerencialDocs/Ordens Bancárias REINF.xlsx;TesouroGerencialDocs" --add-data "requirements.txt;." --add-data "1XLSXtoXML.py;." --add-data "2unirXML.py;." --add-data "4GerarRelatorio.py;." interface.py


</b>
