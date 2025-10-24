# 🌎 API de Turismo - Foz do Iguaçu

Sistema de gerenciamento de pontos turísticos, comércios e benefícios para turistas em Foz do Iguaçu.

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Tecnologias](#-tecnologias)
- [Instalação](#-instalação)
- [Endpoints da API](#-endpoints-da-api)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Autenticação](#-autenticação)

## 🎯 Visão Geral

O sistema oferece uma API REST completa para gerenciar:
- Pontos turísticos de Foz do Iguaçu
- Localização dos pontos e comércios
- Agências de turismo
- Chaves de acesso para turistas
- Cupons de desconto em estabelecimentos comerciais

## 🛠 Tecnologias

- Python 3.12
- Django 5.2.2
- Django REST Framework
- JWT Authentication
- SQLite (Desenvolvimento)

## 💻 Instalação

1. Clone o repositório:
```bash
git clone [url-do-repositorio]
cd hackaton_foz
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv nenv
source nenv/bin/activate  # Linux/Mac
nenv\Scripts\activate     # Windows
```

3. Crie o arquivo .env:
```bash
cp .env.example .env
```

4. Gere uma nova SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

5. Edite o arquivo .env:
   - Cole a SECRET_KEY gerada entre aspas
   - Ajuste outras configurações se necessário

6. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute as migrações:
```bash
python manage.py migrate
```

5. Inicie o servidor:
```bash
python manage.py runserver
```

## 🚀 Endpoints da API

### Autenticação
```
POST /api/token/
POST /api/token/refresh/
```

### Pontos Turísticos
```
GET    /api/tourism/tourist-spots/     # Lista todos os pontos turísticos
POST   /api/tourism/tourist-spots/     # Cria um novo ponto turístico
GET    /api/tourism/tourist-spots/{id} # Obtém detalhes de um ponto turístico
PUT    /api/tourism/tourist-spots/{id} # Atualiza um ponto turístico
DELETE /api/tourism/tourist-spots/{id} # Remove um ponto turístico
```

### Localizações
```
GET    /api/locations/locations/     # Lista todas as localizações
POST   /api/locations/locations/     # Cria uma nova localização
GET    /api/locations/locations/{id} # Obtém detalhes de uma localização
PUT    /api/locations/locations/{id} # Atualiza uma localização
DELETE /api/locations/locations/{id} # Remove uma localização
```

### Comércios
```
GET    /api/business/commerce/     # Lista todos os comércios
POST   /api/business/commerce/     # Cria um novo comércio
GET    /api/business/commerce/{id} # Obtém detalhes de um comércio
PUT    /api/business/commerce/{id} # Atualiza um comércio
DELETE /api/business/commerce/{id} # Remove um comércio
```

### Chaves
```
GET    /api/tourism/keys/     # Lista todas as chaves
POST   /api/tourism/keys/     # Cria uma nova chave
GET    /api/tourism/keys/{id} # Obtém detalhes de uma chave
PUT    /api/tourism/keys/{id} # Atualiza uma chave
DELETE /api/tourism/keys/{id} # Remove uma chave
```

### Cupons
```
GET    /api/business/coupons/     # Lista todos os cupons
POST   /api/business/coupons/     # Cria um novo cupom
GET    /api/business/coupons/{id} # Obtém detalhes de um cupom
PUT    /api/business/coupons/{id} # Atualiza um cupom
DELETE /api/business/coupons/{id} # Remove um cupom
```

### Agências
```
GET    /api/accounts/agency-profiles/     # Lista todas as agências
POST   /api/accounts/agency-profiles/     # Cria uma nova agência
GET    /api/accounts/agency-profiles/{id} # Obtém detalhes de uma agência
PUT    /api/accounts/agency-profiles/{id} # Atualiza uma agência
DELETE /api/accounts/agency-profiles/{id} # Remove uma agência
```

## 📝 Exemplos de Uso

### Autenticação
```json
POST /api/token/
{
    "username": "seu_usuario",
    "password": "sua_senha"
}
```

### Criar Ponto Turístico
```json
POST /api/tourism/tourist-spots/
{
    "nome": "Cataratas do Iguaçu",
    "location_id": 1,
    "descricao": "Uma das maiores quedas d'água do mundo"
}
```

### Criar Comércio
```json
POST /api/business/commerce/
{
    "name": "Restaurante do Bettes",
    "location_id": 1
}
```

### Criar Chave
```json
POST /api/tourism/keys/
{
    "tourist_spot_id": 1,
    "agency_id": 1  // Opcional
}
```

### Criar Cupom
```json
POST /api/business/coupons/
{
    "commerce_id": 1,
    "key_id": 1,
    "desconto": 15.00,
    "descricao": "15% de desconto",
    "validade": "2025-12-31T23:59:59Z"
}
```

## 🔐 Autenticação

A API utiliza autenticação JWT (JSON Web Token). Para acessar endpoints protegidos:

1. Obtenha um token:
```json
POST /api/token/
{
    "username": "seu_usuario",
    "password": "sua_senha"
}
```

2. Use o token nas requisições:
```
Headers:
Authorization: Bearer seu_token_aqui
```

## 🔄 Cache

O sistema implementa cache para otimizar o desempenho em:
- Detalhes dos pontos turísticos
- Listagem de chaves
- Informações de localização

## 🏗 Modelos de Dados

### Location
- numero (int)
- rua (string)
- bairro (string)
- cidade (string)
- estado (string)
- país (string)
- cep (string)
- is_active (boolean)

### TouristSpot
- nome (string)
- location (FK)
- descricao (text)
- is_active (boolean)

### Commerce
- name (string)
- location (FK)
- is_active (boolean)

### Key
- tourist_spot (FK)
- agency (FK, opcional)
- key (UUID)
- code (string)
- is_active (boolean)

### Coupon
- commerce (FK)
- key (FK)
- desconto (decimal)
- descricao (text)
- validade (datetime)
- is_active (boolean)

### AgencyProfile
- nome_agencia (string)
- cnpj (string)
- telefone (string)
- descricao (text)
- user (FK, opcional)
- registration_number (string, opcional)
- verified (boolean)

## 📈 Performance

- Indexação otimizada para consultas frequentes
- Cache implementado para recursos populares
- Paginação para grandes conjuntos de dados

## 🔒 Segurança

- Autenticação JWT
- Proteção contra CSRF
- Validação de dados em todas as entradas
- Sanitização de inputs
- Rate limiting para prevenção de abusos

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/sua-feature`)
3. Commit suas mudanças (`git commit -m 'Adicionando nova feature'`)
4. Push para a branch (`git push origin feature/sua-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.