# Swag2Curl

Este script Python gera comandos cURL com base na documentação Swagger/OpenAPI de uma API.

🚀 Funcionalidades

- Converte endpoints do Swagger/OpenAPI em comandos cURL

- Suporta autenticação via Basic Auth, Bearer Token e API Key

- Adiciona automaticamente parâmetros de query, headers e corpo da requisição

- Suporte para uploads de arquivos com multipart/form-data

- Mantém o formato de uma única linha para facilitar a cópia e execução
  
📌 Pré-requisitos

- Python 3.x

- Biblioteca requests (pode ser instalada com pip install requests)

🔧 Instalação

Clone o repositório:

 - git clone https://github.com/seu-usuario/swagger-to-curl.git
 - cd swagger-to-curl

🛠️ Uso

Execute o script passando a URL da documentação Swagger:

python3 script.py <swagger_url>

🔑 Autenticação

Basic Auth:

python3 script.py <swagger_url> --user <username> <password>

Bearer Token:

python3 script.py <swagger_url> --Bearer <your_token>

API Key:

python3 script.py <swagger_url> --key <your_api_key>

📌 Exemplo de saída

curl -X 'POST' 'https://api.exemplo.com/v1/upload' -H 'Accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@example.jpg'

📜 Licença

Este projeto é distribuído sob a licença MIT.

🤝 Contribuições

Sinta-se à vontade para abrir issues e pull requests! 😊
