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

O endpoint `POST /forecast_var` é utilizado para obter previsões de variação de preços de ativos financeiros com base em seus _tickers_.

#### Detalhes do Endpoint

- **Método HTTP**: `POST`
- **URL**: `/forecast_var`
- **Cabeçalhos obrigatórios**:
  - `Content-Type: application/json`

#### Corpo da Requisição

O corpo da requisição deve ser enviado em formato JSON e conter o campo obrigatório `tickers`, que é uma lista de símbolos (_tickers_) representando os ativos financeiros.

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
  "data": [
    {
      "ativo": "PETR4.SA",
      "historical_metrics": {
        "Retorno Anualizado (%)": 36.13662678530957,
        "Volatilidade Anualizada (%)": 46.31684817679753
      },
      "historical_allocation": 34.320402577246675,
      "forecast_metrics": {
        "Retorno Anualizado (%)": 35.85450619216293,
        "Volatilidade Anualizada (%)": 0.035459660671444425
      },
      "forecast_allocation": 12.919066906482621
    },
    {
      "ativo": "WEGE3.SA",
      "historical_metrics": {
        "Retorno Anualizado (%)": 29.11819607149696,
        "Volatilidade Anualizada (%)": 32.60396261263342
      },
      "historical_allocation": 39.28600259949897,
      "forecast_metrics": {
        "Retorno Anualizado (%)": 29.31191317945293,
        "Volatilidade Anualizada (%)": 0.029082293069874848
      },
      "forecast_allocation": 12.877676061742257
    },
    {
      "ativo": "VALE3.SA",
      "historical_metrics": {
        "Retorno Anualizado (%)": 25.594350505217463,
        "Volatilidade Anualizada (%)": 42.65690376424875
      },
      "historical_allocation": 26.39359482325435,
      "forecast_metrics": {
        "Retorno Anualizado (%)": 25.25205924432003,
        "Volatilidade Anualizada (%)": 0.00434806280348854
      },
      "forecast_allocation": 74.20325703177511
    },
    {
      "ativo": "GLD",
      "historical_metrics": {
        "Retorno Anualizado (%)": 29.11819607149696,
        "Volatilidade Anualizada (%)": 32.60396261263342
      },
      "historical_allocation": 39.28600259949897,
      "forecast_metrics": {
        "Retorno Anualizado (%)": 29.31191317945293,
        "Volatilidade Anualizada (%)": 0.029082293069874848
      },
      "forecast_allocation": 12.877676061742257
    },
    {
      "ativo": "BRL=X",
      "historical_metrics": {
        "Retorno Anualizado (%)": 36.13662678530957,
        "Volatilidade Anualizada (%)": 46.31684817679753
      },
      "historical_allocation": 34.320402577246675,
      "forecast_metrics": {
        "Retorno Anualizado (%)": 35.85450619216293,
        "Volatilidade Anualizada (%)": 0.035459660671444425
      },
      "forecast_allocation": 12.919066906482621
    }
  ]
}
```

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
