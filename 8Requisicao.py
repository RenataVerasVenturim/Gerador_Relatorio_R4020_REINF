import pycurl
from io import BytesIO

# URL da API do REINF
url = "https://pre-reinf.receita.economia.gov.br/recepcao/lotes"

# Caminho do XML do lote
xml_path = "C:\\Users\\PROPPI-RENATA\\Desktop\\ProgramaREINFWebService2.0\\XMLAssinados\\LoteEventos.xml"

# Ler o XML
with open(xml_path, "rb") as file:
    xml_data = file.read()

# Buffer para armazenar a resposta
buffer = BytesIO()

# Criar a requisição
c = pycurl.Curl()
c.setopt(c.URL, url)

# Configurar headers
c.setopt(c.HTTPHEADER, ["Content-Type: application/xml"])

# Enviar XML
c.setopt(c.POSTFIELDS, xml_data)

# Caminho da biblioteca PKCS#11 do Token USB
pkcs11_lib = "C:/Arquivos de Programas/SafeSign/ptkcs11.dll"  # Ajuste conforme o seu middleware

# Configurar o Token USB como certificado
c.setopt(c.SSLENGINE, "pkcs11")
c.setopt(c.SSLENGINE_DEFAULT, 1)
c.setopt(c.SSLCERTTYPE, "ENG")  # Usar o Token USB diretamente
c.setopt(c.SSLCERT, "pkcs11:slot_0")  # Ajuste conforme o seu Token

# Senha do Token USB (será solicitada na execução)
c.setopt(c.SSLKEYPASSWD, "SENHA_DO_TOKEN")

# Salvar resposta no buffer
c.setopt(c.WRITEDATA, buffer)

# Executar a requisição
c.perform()

# Exibir resposta
status_code = c.getinfo(c.RESPONSE_CODE)
response_data = buffer.getvalue().decode('utf-8')

print("Status Code:", status_code)
print("Resposta:", response_data)

# Fechar conexão
c.close()
