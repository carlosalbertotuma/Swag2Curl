import requests
import sys
import json

def exibir_banner():
    banner = r"""
    ============================================================
    
     .d8888b.                                   .d8888b.   .d8888b.                   888 
    d88P  Y88b                                 d88P  Y88b d88P  Y88b                  888 
    Y88b.                                             888 888    888                  888 
     "Y888b.   888  888  888  8888b.   .d88b.       .d88P 888        888  888 888d888 888 
        "Y88b. 888  888  888     "88b d88P"88b  .od888P"  888        888  888 888P"   888 
          "888 888  888  888 .d888888 888  888 d88P"      888    888 888  888 888     888 
    Y88b  d88P Y88b 888 d88P 888  888 Y88b 888 888"       Y88b  d88P Y88b 888 888     888 
     "Y8888P"   "Y8888888P"  "Y888888  "Y88888 888888888   "Y8888P"   "Y88888 888     888 
                                           888                                            
                                      Y8b d88P    By Bl4dsc4n  Version 0.1                                        
                                       "Y88P"                                             
    ============================================================
    
    Uso: python3 Swag2Curl.py https://petstore.swagger.io/v2/swagger.json

    
    Exemplos de uso:
      Montar as requisições sem utilizar autenticação:
          python3 Swag2Curl.py https://petstore.swagger.io/v2/swagger.json 

       Montar as requisições utilizando autenticação --user <username> <password>:
          python3 Swag2Curl.py https://petstore.swagger.io/v2/swagger.json --user <username> <password>

      Montar as requisições utilizando autenticação --Bearer <your_token>:
          python3 Swag2Curl.py https://petstore.swagger.io/v2/swagger.json --Bearer <your_token>

      Montar as requisições utilizando autenticação --key <your_api_key>:
          python3 Swag2Curl.py https://petstore.swagger.io/v2/swagger.json --key <your_api_key>
          
    * Este script Python gera comandos cURL com base na documentação Swagger/OpenAPI de uma API.

      Certifique-se de ter permissão antes de executar.

    Desenvolvido por Carlos Tuma - Bl4dsc4n - Version 0.1
    ============================================================
    """
    print(banner)


def generate_curl_commands(swagger_url, username=None, password=None, token=None, api_key=None):
    response = requests.get(swagger_url)
    if response.status_code != 200:
        print(f"Falha ao acessar a URL: {swagger_url}. Código de status: {response.status_code}")
        return

    swagger_data = response.json()
    base_url = swagger_data.get('host', '')
    if not base_url.startswith('http'):
        base_url = f"{swagger_data.get('schemes', ['https'])[0]}://{base_url}"
    base_url += swagger_data.get('basePath', '')

    for path, methods in swagger_data.get('paths', {}).items():
        for method, details in methods.items():
            full_url = f"{base_url}{path}"

            query_params = []
            headers = ["-H 'Accept: application/json'"]
            body_data = None
            form_data = []
            has_body = False

            if 'parameters' in details:
                for param in details['parameters']:
                    param_name = param.get('name')
                    param_value = param.get('example', '<value>')

                    if param['in'] == 'query':
                        query_params.append(f"{param_name}={param_value}")
                    elif param['in'] == 'header':
                        headers.append(f"-H '{param_name}: {param_value}'")
                    elif param['in'] == 'path':
                        full_url = full_url.replace(f"{{{param_name}}}", str(param_value))
                    elif param['in'] == 'body' and 'schema' in param:
                        has_body = True
                        schema = param['schema']
                        if 'example' in schema:
                            body_data = json.dumps(schema['example'])
                        elif 'properties' in schema:
                            body_data = json.dumps({k: v.get('example', '<value>') for k, v in schema['properties'].items()})
                    elif param['in'] == 'formData':
                        has_body = True
                        if param.get('type') == 'file':
                            form_data.append(f"-F '{param_name}=@example.jpg'")
                        else:
                            form_data.append(f"-F '{param_name}={param_value}'")

            if query_params:
                full_url += '?' + '&'.join(query_params)

            if 'requestBody' in details:
                has_body = True
                content = details['requestBody'].get('content', {})
                if 'application/json' in content:
                    schema = content['application/json'].get('schema', {})
                    if 'properties' in schema:
                        body_data = json.dumps({k: v.get('example', '<value>') for k, v in schema['properties'].items()})

            curl_command = f"curl -X '{method.upper()}' '{full_url}'"

            # Adicionando autenticação, se necessário
            if username and password:
                curl_command += f" --user '{username}:{password}'"
            elif token:
                curl_command += f" -H 'Authorization: Bearer {token}'"
            elif api_key:
                curl_command += f" -H 'x-api-key: {api_key}'"

            # Adicionando headers
            if headers:
                curl_command += ' ' + ' '.join(headers)

            # Se for um upload de arquivo, adicionar Content-Type: multipart/form-data
            if form_data:
                curl_command += " -H 'Content-Type: multipart/form-data'"

            # Adicionando corpo da requisição
            if body_data:
                curl_command += f" --data '{body_data}'"
            elif form_data:
                curl_command += ' ' + ' '.join(form_data)
            elif has_body:
                curl_command += " --data '{}'"

            print(curl_command)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        exibir_banner()
        
    else:
        swagger_url = sys.argv[1]
        username = None
        password = None
        token = None
        api_key = None

        # Verificando argumentos
        if '--user' in sys.argv:
            user_index = sys.argv.index('--user') + 1
            username = sys.argv[user_index]
            password = sys.argv[user_index + 1]

        if '--Bearer' in sys.argv:
            token_index = sys.argv.index('--Bearer') + 1
            token = sys.argv[token_index]

        if '--key' in sys.argv:
            api_key_index = sys.argv.index('--key') + 1
            api_key = sys.argv[api_key_index]

        # Gerar os comandos curl com os parâmetros fornecidos
        generate_curl_commands(swagger_url, username, password, token, api_key)
