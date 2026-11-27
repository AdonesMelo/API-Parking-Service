# 🚗 API Parking Service

Sistema completo de gerenciamento de estacionamento desenvolvido com **Django** e **Django REST Framework**, projetado com arquitetura orientada a eventos, processamento assíncrono, automação de consulta de placas veiculares e containerização completa com Docker.

   📌 Créditos: Projeto originalmente idealizado pela PycodeBR e reproduzido por Adones Melo para fins de estudo, prática e portfólio.

## 📋 Índice

* [Sobre o Projeto](#-sobre-o-projeto)
* [Como o Projeto Funciona (Fluxo da Arquitetura)](#-como-o-projeto-funciona-fluxo-da-arquitetura)
* [Funcionalidades Principais](#-funcionalidades-principais)
* [Tecnologias Utilizadas](#-tecnologias-utilizadas)
* [Estrutura do Projeto](#-estrutura-do-projeto)
* [Pré-requisitos](#-pré-requisitos)
* [Passo a Passo: Como Rodar com Docker (Recomendado)](#-passo-a-passo-como-rodar-com-docker-recomendado)
* [Passo a Passo: Como Rodar Localmente (Sem Docker)](#-passo-a-passo-como-rodar-localmente-sem-docker)
* [Acesso e Endpoints Principais](#-acesso-e-endpoints-principais)
* [Autenticação e Permissões](#-autenticação-e-permissões)
* [Filtros Dinâmicos (RQL)](#-filtros-dinâmicos-rql)
* [Qualidade de Código e Documentação](#-qualidade-de-código-e-documentação)
* [Autor](#-autor)

## 🎯 Sobre o Projeto

O **API Parking Service** gerencia o fluxo completo de um estacionamento: cadastro de clientes, controle de veículos e categorias, disponibilidade de vagas em tempo real e histórico de entradas e saídas.

Além do CRUD tradicional, o sistema automatiza tarefas críticas através de **Django Signals**, filas com **Celery + RabbitMQ/Redis** e web scraping com **Playwright** para enriquecimento automático dos dados dos veículos a partir da placa.

## ⚙️ Como o Projeto Funciona (Fluxo da Arquitetura)

1. **Autenticação (`authentication`):** O usuário faz login enviando suas credenciais e recebe um par de tokens **JWT** (`access` e `refresh`) para autenticar as próximas requisições.
2. **Automação de Cadastro de Veículos (`vehicles`):**
   * Ao cadastrar um novo veículo informando a placa, um **Django Signal** (`post_save`) é disparado automaticamente.
   * Esse signal envia uma tarefa assíncrona para a fila do **RabbitMQ**, que é consumida pelo **Celery Worker**.
   * O worker aciona o **Playwright** (navegador headless) para consultar os dados do veículo pela placa e atualiza o registro no **PostgreSQL**, salvando o status da tarefa no **Redis**.
3. **Controle de Vagas em Tempo Real (`parking`):**
   * Ao criar um registro de entrada (`ParkingRecord`) sem `exit_time`, um **Signal** marca automaticamente a vaga (`ParkingSpot`) como ocupada (`is_occupied = True`).
   * Ao registrar a saída (`exit_time` preenchido), a vaga é liberada automaticamente (`is_occupied = False`).
4. **Isolamento de Dados (`core/permissions.py`):** A permissão customizada `IsOwnerOfVehicleOrRecord` garante que cada cliente visualize apenas seus próprios veículos e registros, enquanto usuários `staff` têm acesso completo.

## ✨ Funcionalidades Principais

* **Gestão de Clientes (`customers`):** Cadastro e controle de proprietários vinculados aos usuários do sistema.
* **Gestão de Veículos (`vehicles`):** Registro de veículos e tipos de veículos (`VehicleType`), com **preenchimento automático de dados** via consulta assíncrona pela placa.
* **Controle de Estacionamento (`parking`):**
  * Gerenciamento de vagas (`ParkingSpot`) e registros de entrada/saída (`ParkingRecord`).
  * Atualização automática do status da vaga (`is_occupied`) via `post_save` signals ao registrar entrada ou saída.
  * Filtro inteligente no painel administrativo exibindo apenas vagas disponíveis no momento da criação de um novo registro.
* **Segurança e Controle de Acesso (`authentication` & `core`):** Autenticação stateless via JWT e permissões granulares por proprietário.
* **Consultas Avançadas:** Suporte a queries dinâmicas na URL utilizando **Django RQL**.
* **Documentação Interativa:** Interface **Swagger UI** e **ReDoc** integradas e servidas localmente (Sidecar), além de documentação técnica com **MkDocs**.
* **Painel Administrativo Moderno:** Interface customizada com **Django Jazzmin** configurada diretamente na rota raiz (`/`).

## 🛠 Tecnologias Utilizadas

### Backend & API
* **Python 3** & **Django 6.1**
* **Django REST Framework (DRF)**
* **Simple JWT** (`djangorestframework-simplejwt`) — Autenticação via Token
* **Django RQL** (`django-rql`) — Filtragem avançada na API
* **DRF Spectacular + Sidecar** (`drf-spectacular`) — Documentação OpenAPI 3.0
* **Django Jazzmin** (`django-jazzmin`) — Tema e customização do Django Admin

### Banco de Dados, Mensageria & Automação
* **PostgreSQL** (`psycopg2-binary`) — Banco de dados relacional
* **Celery** — Processamento de tarefas assíncronas em background
* **RabbitMQ** — Message Broker para filas do Celery
* **Redis** — Backend de resultados / cache
* **Playwright** — Automação de navegador para consulta de dados de placas

### Infraestrutura, Documentação & Qualidade
* **Docker** & **Docker Compose** — Orquestração dos serviços (Web, Worker, PostgreSQL, RabbitMQ, Redis)
* **Flake8** — Linter e padronização de código (PEP 8)
* **MkDocs** — Documentação estruturada do projeto

## 📂 Estrutura do Projeto

```text
Parking-Service-API/
├── authentication/          # Rotas e configurações de autenticação JWT
├── core/                    # Configurações centrais da aplicação
│   ├── __init__.py          # Carregamento do app Celery
│   ├── asgi.py              # Configuração ASGI
│   ├── celery.py            # Instância e configurações do Celery
│   ├── permissions.py       # Permissões customizadas (IsOwnerOfVehicleOrRecord)
│   ├── settings.py          # Configurações globais (DRF, Jazzmin, DB, Celery, RQL)
│   ├── urls.py              # Roteamento principal (Admin na raiz e endpoints v1)
│   └── wsgi.py              # Configuração WSGI
├── customers/               # App de gestão de clientes
│   ├── admin.py             # Registro no Django Admin
│   ├── apps.py              # Configuração do app
│   ├── filters.py           # Filtros dinâmicos (Django RQL)
│   ├── models.py            # Modelo Customer
│   ├── serializers.py       # Serializers DRF
│   ├── urls.py              # Rotas do app
│   └── views.py             # ViewSets da API
├── docs/                    # Arquivos fonte da documentação MkDocs
├── parking/                 # App de vagas e registros de estacionamento
│   ├── admin.py             # Admin com filtro de vagas livres
│   ├── apps.py              # Configuração e carregamento de signals
│   ├── filters.py           # Filtros dinâmicos (Django RQL)
│   ├── models.py            # Modelos ParkingSpot e ParkingRecord
│   ├── serializers.py       # Serializers DRF
│   ├── signals.py           # Automação de ocupação de vagas (post_save)
│   ├── urls.py              # Rotas do app
│   └── views.py             # ViewSets da API
├── static/                  # Arquivos estáticos próprios
│   └── images/              # Identidade visual SVG (login_logo, site_icon, site_logo)
├── staticfiles/             # Arquivos estáticos coletados (collectstatic)
├── vehicles/                # App de gestão de veículos
│   ├── admin.py             # Registro no Django Admin
│   ├── apps.py              # Configuração e carregamento de signals
│   ├── filters.py           # Filtros dinâmicos (Django RQL)
│   ├── models.py            # Modelos Vehicle e VehicleType
│   ├── serializers.py       # Serializers DRF
│   ├── signals.py           # Disparo de task assíncrona ao cadastrar veículo
│   ├── tasks.py             # Task Celery + Playwright para consulta de placa
│   ├── urls.py              # Rotas do app
│   └── views.py             # ViewSets da API
├── .dockerignore            # Arquivos ignorados no build da imagem Docker
├── .flake8                  # Regras de linting do Flake8
├── .gitignore               # Arquivos ignorados pelo Git
├── docker-compose.yml       # Orquestração dos containers (API, Worker, DB, Broker)
├── Dockerfile               # Receita da imagem Python + dependências do Playwright
├── manage.py                # Utilitário de linha de comando do Django
├── mkdocs.yml               # Configuração do MkDocs
└── requirements.txt         # Dependências Python do projeto
```

## 📦 Pré-requisitos

* **Para execução via Docker:** [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/) instalados.
* **Para execução local:** Python 3.11+, PostgreSQL, RabbitMQ e Redis instalados e rodando na máquina.

## 🚀 Passo a Passo: Como Rodar com Docker (Recomendado)

O Docker sobe toda a infraestrutura automaticamente (API Django, Worker Celery com Playwright, PostgreSQL, RabbitMQ e Redis).

1. **Clone o repositório e entre na pasta do projeto:**
   ```bash
   git clone <URL_DO_SEU_REPOSITORIO>
   cd API-Parking-Service
   ```

2. **Construa as imagens e inicie todos os containers:**
   ```bash
   docker-compose up --build -d
   ```

3. **Verifique se todos os containers estão ativos:**
   ```bash
   docker ps
   ```

4. **Aplique as migrações do banco de dados dentro do container:**
   ```bash
   docker-compose exec api_parking_service python manage.py migrate
   ```

5. **Colete os arquivos estáticos (Jazzmin e DRF Spectacular):**
   ```bash
   docker-compose exec api_parking_service python manage.py collectstatic --noinput
   ```

6. **Crie um superusuário para acessar o painel administrativo:**
   ```bash
   docker-compose exec api_parking_service python manage.py createsuperuser
   ```

7. **Comandos úteis do dia a dia com Docker:**
   ```bash
   # Subir os containers já construídos
   docker-compose up -d

   # Acompanhar os logs em tempo real (API e Worker Celery)
   docker-compose logs -f

   # Acessar o terminal (bash) de um container específico
   docker exec -it <ID_OU_NOME_DO_CONTAINER> /bin/bash

   # Parar todos os serviços
   docker-compose down
   ```

## 💻 Passo a Passo: Como Rodar Localmente (Sem Docker)

Caso queira rodar o ambiente de desenvolvimento diretamente na sua máquina:

1. **Crie e ative um ambiente virtual (`venv`):**
   ```bash
   # Criar ambiente virtual
   python -m venv venv

   # Ativar no Windows (PowerShell)
   .\venv\Scripts\Activate.ps1

   # Ativar no Linux / macOS
   source venv/bin/activate
   ```

2. **Atualize o `pip` e instale todas as bibliotecas do projeto:**
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
   > *Principais pacotes instalados pelo `requirements.txt`: `django`, `djangorestframework`, `djangorestframework-simplejwt`, `django-jazzmin`, `django-rql`, `drf-spectacular[sidecar]`, `psycopg2-binary`, `celery`, `playwright` e `flake8`.*

3. **Instale os navegadores necessários para o Playwright:**
   ```bash
   playwright install
   ```

4. **Configure o banco de dados em `core/settings.py`:**
   Certifique-se de que o `HOST` do PostgreSQL aponte para `localhost` (ou `127.0.0.1`) e que o PostgreSQL, RabbitMQ e Redis estejam ativos localmente.

5. **Gere e aplique as migrações no banco de dados:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Colete os arquivos estáticos e crie o superusuário:**
   ```bash
   python manage.py collectstatic
   python manage.py createsuperuser
   ```

7. **Inicie o servidor Django e o Worker do Celery (em dois terminais separados):**
   ```bash
   # Terminal 1: Servidor web do Django
   python manage.py runserver

   # Terminal 2: Worker do Celery (adicione --pool=solo no Windows)
   celery -A core worker -l info --pool=solo
   ```

## 🔗 Acesso e Endpoints Principais

Com a aplicação em execução, acesse os recursos pelos endereços abaixo:

| Serviço / Recurso | URL | Descrição |
| :--- | :--- | :--- |
| **Painel Administrativo** | `http://localhost:8000/` | Interface Django Admin estilizada com Jazzmin |
| **Swagger UI** | `http://localhost:8000/api/v1/docs/` | Documentação interativa para testar os endpoints |
| **ReDoc** | `http://localhost:8000/api/v1/redoc/` | Documentação técnica detalhada da API |
| **Autenticação (Token)** | `http://localhost:8000/api/v1/authentication/token/` | Geração de `access` e `refresh` tokens JWT |
| **Clientes** | `http://localhost:8000/api/v1/customers/` | CRUD de clientes |
| **Veículos** | `http://localhost:8000/api/v1/vehicles/` | CRUD de veículos e tipos |
| **Estacionamento** | `http://localhost:8000/api/v1/parking/` | CRUD de vagas (`spots`) e registros (`records`) |

## 🔐 Autenticação e Permissões

1. Faça uma requisição `POST` para `http://localhost:8000/api/v1/authentication/token/` enviando `username` e `password`.
2. Copie o valor de `access` retornado.
3. Nas requisições seguintes, inclua o cabeçalho HTTP:
   ```http
   Authorization: Bearer <seu_token_access>
   ```

* **Usuários comuns:** Podem visualizar e gerenciar apenas veículos e registros de estacionamento vinculados ao seu perfil.
* **Administradores (`is_staff`):** Têm acesso irrestrito a todos os registros e recursos da API.

## 🔍 Filtros Dinâmicos (RQL)

Todos os endpoints de listagem suportam filtragem dinâmica via query params utilizando **RQL (Resource Query Language)**. Exemplos:

```http
# Buscar vagas livres
GET /api/v1/parking/spots/?eq(is_occupied,false)

# Buscar veículos por placa parcial
GET /api/v1/vehicles/?like(license_plate,*ABC*)

# Ordenar registros por data de entrada mais recente
GET /api/v1/parking/records/?ordering(-entry_time)
```

## 🧹 Qualidade de Código e Documentação

* **Verificar padronização PEP 8 com Flake8:**
  ```bash
  flake8
  ```

* **Atualizar o arquivo de dependências após instalar novos pacotes:**
  ```bash
  pip freeze > requirements.txt
  ```

* **Visualizar a documentação técnica localmente com MkDocs:**
  ```bash
  mkdocs serve -a localhost:8001
  ```

## 👨‍💻 Créditos e Autor

- Projeto Original: PycodeBR

- Reproduzido e implementado por: Adones Melo
