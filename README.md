# alm-assets (ativos)
Repositório destinado ao serviço de ativos do projeto ALM

## Estrutura do Projeto

```plaintext
assets/
│
├── docker-compose.yml      # Configuração do Docker Compose
├── Dockerfile              # Configuração do container da aplicação
├── assets
    └──   main.py           # Ponto de entrada da aplicação
    └── database.py             # Conexão com o banco de dados
    └── models/                 # Modelos de banco
       └── models
    └── controllers/            # Lógica de negócios
       └── controllers
    └── views/                  # Rotas
       └── views
└── requirements.txt        # Dependências do Python
```

## Requisitos

- Docker
- Docker Compose
- Python 3.10+

## Como Rodar a Aplicação

- docker-compose up --build


## Acesse a API
Depois de subir os containers, você pode acessar a API através dos seguintes endpoints:

Documentação interativa (Swagger): http://localhost:8000/docs
Raiz da aplicação: http://localhost:8000

### Exemplo de Uso do Endpoint `/forecast_var`

O endpoint `POST /forecast_var` é utilizado para obter previsões de variação de preços de ativos financeiros com base em seus *tickers*. 

#### Detalhes do Endpoint

- **Método HTTP**: `POST`
- **URL**: `/forecast_var`
- **Cabeçalhos obrigatórios**:
  - `Content-Type: application/json`

#### Corpo da Requisição

O corpo da requisição deve ser enviado em formato JSON e conter o campo obrigatório `tickers`, que é uma lista de símbolos (*tickers*) representando os ativos financeiros.

##### Exemplo de Corpo da Requisição

```json
{
  "tickers": ["BRL=X", "PETR4.SA", "VALE3.SA", "WEGE3.SA", "GLD"]
}
```

- **`tickers`**: Lista de tickers a serem processados pela API. 
  - `BRL=X`: Representa o câmbio Real/Dólar.
  - `PETR4.SA`, `VALE3.SA`, `WEGE3.SA`: Representam ações negociadas na bolsa brasileira (B3).
  - `GLD`: Representa um ETF de ouro.

#### Exemplo de Resposta

##### Sucesso (HTTP 200)

```json
{
  "forecast": {
    "BRL=X": {"predicted_change": 0.005, "confidence": 0.9},
    "PETR4.SA": {"predicted_change": -0.02, "confidence": 0.85},
    "VALE3.SA": {"predicted_change": 0.01, "confidence": 0.92},
    "WEGE3.SA": {"predicted_change": 0.015, "confidence": 0.88},
    "GLD": {"predicted_change": -0.005, "confidence": 0.91}
  }
}
```

- **`forecast`**: Objeto contendo as previsões para cada ativo solicitado.
  - Cada ticker possui:
    - **`predicted_change`**: Previsão da variação percentual do ativo (positiva ou negativa).
    - **`confidence`**: Grau de confiança da previsão (entre 0 e 1).

##### Erro (HTTP 400)

```json
{
  "error": "Invalid request. The 'tickers' field must be a non-empty array."
}
```

- Indica que a requisição possui um corpo inválido ou incompleto.

#### Notas

- Certifique-se de que os tickers fornecidos são válidos e suportados pela API do Yahoo
- A precisão dos dados pode variar dependendo da qualidade do modelo e do período analisado.
