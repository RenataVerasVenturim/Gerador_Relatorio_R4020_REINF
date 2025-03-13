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
<b>pyinstaller --onefile --add-data "ArquivosUnidos;ArquivosUnidos" --add-data "ExtracaoSiafi;ExtracaoSiafi" --add-data "RelatorioGerado;RelatorioGerado" --add-data "TesouroGerencialDocs;TesouroGerencialDocs" --add-data "requirements.txt;." --hidden-import "1XLSXtoXML" --hidden-import "2unirXML" --hidden-import "4GerarRelatorio" interface.py

</b>
