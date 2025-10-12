# Projeto de Simulação: Ecossistema de Microsserviços para Regulação de Saúde (SUS Inteligente)

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95-green.svg)
![Docker](https://img.shields.io/badge/Docker-20.10-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue.svg)

## 📄 Visão Geral

Este projeto simula um ecossistema completo de microsserviços para um sistema de regulação de saúde digital, inspirado nos desafios do SUS. A arquitetura foi projetada para ser modular, escalável e resiliente, demonstrando como diferentes responsabilidades (autenticação, regulação, comunicação, feedback) podem ser desacopladas em serviços independentes.

O coração do sistema é um **agente inteligente** que automatiza o processo de agendamento, buscando a melhor vaga para o paciente com base em critérios de data e proximidade geográfica. Um **simulador** dinâmico gera carga de trabalho contínua, permitindo observar o comportamento do sistema em tempo real.

## ✨ Funcionalidades Principais

* **Arquitetura de Microsserviços:** Sistema desacoplado com 4 serviços de aplicação + banco de dados.
* **Autenticação Segura via JWT:** Um serviço dedicado (`auth-service`) gerencia a autenticação e protege os endpoints de negócio.
* **Agente Inteligente de Agendamento:** Lógica automatizada no `regulation-service` para encontrar a melhor vaga, simulando a função de um regulador.
* **Simulação de Vida do Sistema:** Um script (`simulator.py`) que atua como múltiplos atores (solicitantes, reguladores, pacientes) para gerar carga e testar o sistema de ponta a ponta.
* **Serviços de Apoio Desacoplados:** Serviços dedicados para comunicação (`communication-service`) e avaliações (`review-service`).
* **Containerização Completa:** Todo o ecossistema é orquestrado com Docker e Docker Compose, garantindo um ambiente de desenvolvimento e execução consistente.

## 🏗️ Arquitetura

O projeto é composto pelos seguintes serviços:

* **`auth-service`**: Responsável por validar credenciais e emitir tokens de acesso JWT. A porta de entrada do sistema.
* **`regulation-service`**: O serviço principal. Gerencia todo o ciclo de vida das solicitações, ofertas e marcações. Contém o agente inteligente.
* **`communication-service`**: Simula o envio de notificações para os pacientes (ex: confirmação de agendamento).
* **`review-service`**: Coleta as avaliações (notas e comentários) dos pacientes após a conclusão de um procedimento.
* **`postgres`**: O banco de dados PostgreSQL que provê a persistência de dados para todos os serviços.

## 🛠️ Stack Tecnológico

| Componente            | Tecnologia Utilizada                               |
| --------------------- | -------------------------------------------------- |
| **Backend** | Python 3.10, FastAPI                               |
| **Banco de Dados** | PostgreSQL                                         |
| **Autenticação** | JWT (`python-jose`)                                |
| **Containerização** | Docker, Docker Compose                             |
| **Comunicação API** | `httpx`                                            |
| **Simulação de Dados**| `Faker`                                            |
| **Assincronia** | `asyncio`                                          |

## 🚀 Como Executar o Projeto

Siga os passos abaixo para colocar todo o ecossistema no ar.

### Pré-requisitos

* Docker
* Docker Compose
* Python 3.10+ (para executar o simulador)

### 1. Configuração Inicial

**a. Clone o repositório:**
```bash
git clone <url_do_seu_repositorio>
cd <nome_da_pasta>
```

**b. Crie o arquivo de ambiente:**
Crie um arquivo chamado `.env` na raiz do projeto e cole o conteúdo abaixo.

```ini
# Conteúdo do arquivo .env

# Configuração do Banco de Dados
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=sus_hackathon_db

# Chave secreta para assinar os tokens JWT
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
JWT_ALGORITHM=HS256

# Credenciais de exemplo para o MVP
MVP_USER=regulador
MVP_PASSWORD=hackathon_password
```

### 2. Iniciando os Serviços

Com o Docker em execução, suba todos os containers. O comando `--build` garantirá que as imagens sejam construídas a partir do código mais recente.

```bash
docker-compose up --build
```
Aguarde até que todos os serviços (postgres, auth, regulation, etc.) exibam logs indicando que estão em execução e prontos.

### 3. Executando o Simulador

O simulador atua como um cliente externo que interage com a nossa API.

**a. Instale as dependências locais:**
Em um **novo terminal**, na mesma pasta raiz do projeto, instale as bibliotecas que o simulador precisa.
```bash
pip install httpx asyncio faker
```

**b. Rode o simulador:**
```bash
python simulator.py
```
Agora, observe os logs no terminal do simulador (mostrando as ações que ele está tomando) e no terminal do `docker-compose` (mostrando os serviços reagindo a essas ações).

## ઍ Acesso e Uso da API

Cada serviço possui sua própria documentação interativa (Swagger UI), acessível pelo navegador:

* **Auth Service:** `http://localhost:8000/docs`
* **Regulation Service:** `http://localhost:8001/docs`
* **Review Service:** `http://localhost:8002/docs`
* **Communication Service:** `http://localhost:8003/docs`

Para testar os endpoints protegidos, primeiro use o `POST /token` do `auth-service` para obter um token e, em seguida, use o botão "Authorize" no topo da página dos outros serviços para autenticar suas requisições.

### Exemplo de Teste Manual com `curl`

**1. Obter um token:**
```bash
TOKEN=$(curl -X POST "http://localhost:8000/token" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=regulador&password=hackathon_password" | jq -r .access_token)
```

**2. Criar uma nova solicitação:**
```bash
curl -X POST "http://localhost:8001/solicitacoes" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-d '{
  "paciente_id": "PACIENTE_CURL_001",
  "unidade_solicitante_id_cnes": "CNES_5",
  "procedimento_id": "PROC_3"
}'
```

## 🔮 Próximos Passos e Melhorias

* Implementar os atores restantes do simulador (confirmação de agendamento, avaliação).
* Conectar a um frontend para criar uma interface visual para o sistema.
* Substituir a lógica do agente por um modelo de Machine Learning treinado com dados reais.
* Evoluir o `communication-service` para se conectar a um provedor real de SMS ou e-mail.
