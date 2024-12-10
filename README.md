# alm-
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
