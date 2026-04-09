# 🌐 IP API 

API REST desenvolvida em Python para consulta de informações de endereços IP, utilizando a API externa do **ipwhois.io**, com persistência em MongoDB, processamento assíncrono com Celery/Redis e autenticação híbrida (Token Estático + JWT).

---

# 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e rodar a aplicação em seu ambiente local:

### 1. Clonar o Repositório e Acessar a Pasta
```bash
git clone https://github.com/victorlrpf/ip_api
cd ip_api
```

### 2. Configurar o Ambiente Virtual
```bash
# Criar o ambiente
python -m venv .venv

# Ativar no Windows:
.venv\Scripts\activate

# Ativar no Linux/Mac:
source .venv/bin/activate
```

### 3. Instalar as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente (.env)
Crie um arquivo `.env` na raiz do projeto com as seguintes chaves:
```env
APP_NAME=IP API
APP_TOKEN=7f3a9c2e-91ab-4c8d-bf21-9d8a7c5e1234

#Mongo
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB=ip_tracker

#Redis
REDIS_URL=redis://localhost:6379/0

#URL base
IPWHOIS_BASE_URL=https://ipwho.is

# Configurações para o novo JWT
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Iniciar os Serviços (Docker)
Certifique-se de ter o Docker rodando para subir o Banco de Dados e o Broker:
```bash
docker-compose up -d
```
Isso iniciará:
MongoDB → porta 27017
Redis → porta 6379

### 6. Executar a Aplicação e Workers
Em terminais separados, execute:
* **API:** `uvicorn app.main:app --reload`
* **Worker:** `celery -A app.workers.celery_app.celery_app worker --loglevel=info`
* **Beat:** `celery -A app.workers.celery_app.celery_app beat --loglevel=info`

---

# 🔄 Funcionamento

A aplicação centraliza a consulta de IPs, otimizando o uso de APIs externas e garantindo a atualização dos dados.

1.  **Consulta de IP (`POST /ips`):** O usuário envia um IP. O sistema valida o formato, verifica se já existe no MongoDB. Se existir, retorna o dado local; caso contrário, consulta o `ipwhois.io`, salva no banco e retorna.
2.  **Listagem (`GET /ips`):** Permite visualizar todos os IPs consultados com suporte a paginação e filtros por prefixo de IP.
3.  **Atualização Periódica:** Através do Celery Beat, a cada 12 horas, todos os IPs da base são reconsultados automaticamente para garantir que as informações geográficas e de ASN estejam sempre atualizadas.
4.  **Atualização Manual (`POST /ips/refresh`):** Permite disparar a tarefa de atualização de toda a base sob demanda.

---

# 🧠 Solução Adotada

A implementação foi focada em **performance, escalabilidade e segurança**:

### 1. Arquitetura em Camadas
Utilizei o padrão de separação de responsabilidades (API, Service, Repository, Models) para facilitar a manutenção e os testes unitários/integração.

### 2. Cache Persistente com MongoDB
Em vez de um cache volátil, optei por persistir as consultas no MongoDB. Isso garante que, mesmo após um restart do sistema, não perderemos os dados já pagos/consultados na API externa.

### 3. Processamento Assíncrono (Celery + Redis)
As tarefas de atualização em massa são delegadas para workers em background. Isso evita que a API fique lenta ou sofra timeout ao processar grandes volumes de dados.

### 4. Autenticação Híbrida Inteligente
Implementei uma camada de segurança no `app/core/seguranca.py` que aceita dois tipos de credenciais no header `Authorization: Bearer`:
*   **Token Estático:** Para integrações legadas ou scripts administrativos.
*   **JWT com Expiração (30 min):** Para acessos temporários e mais seguros, gerados através do novo endpoint `POST /auth/login`.
Essa abordagem permite evoluir a segurança do projeto sem quebrar as integrações que já utilizavam o token fixo.

### 5. Validação 
Uso de Pydantic para garantir que apenas dados válidos entrem no sistema e que as respostas sigam um contrato estrito com o cliente da API.
