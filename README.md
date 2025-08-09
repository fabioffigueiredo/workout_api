# Workout API

## 💡 Descrição
Este projeto implementa uma API RESTful para gerenciar dados de treinos, incluindo atletas, categorias e centros de treinamento. A API permite a criação, consulta, atualização e exclusão de registros, com validação de dados robusta e paginação para listagem de recursos.

## 🔧 Tecnologias Utilizadas
- **Python**: Linguagem de programação principal.
- **FastAPI**: Framework web de alta performance para construção da API.
- **SQLAlchemy**: ORM (Object-Relational Mapper) para interação com o banco de dados.
- **PostgreSQL**: Banco de dados relacional.
- **Alembic**: Ferramenta de migração de banco de dados.
- **Pydantic**: Biblioteca para validação de dados e serialização.
- **fastapi-pagination**: Extensão para adicionar paginação aos endpoints da API.
- **Uvicorn**: Servidor ASGI para rodar a aplicação FastAPI.
- **Docker**: Plataforma para conteinerização da aplicação e do banco de dados.

## 📊 Resultados
- API RESTful completa para gerenciamento de atletas, categorias e centros de treinamento.
- Integração com banco de dados PostgreSQL para persistência de dados.
- Validação automática de dados de entrada e saída com Pydantic.
- Paginação eficiente para listagem de grandes volumes de dados.
- Ambiente de desenvolvimento e produção conteinerizado com Docker.

## 🚀 Como Executar

### Pré-requisitos
Certifique-se de ter o [Docker](https://www.docker.com/get-started) e o [Docker Compose](https://docs.docker.com/compose/install/) instalados em sua máquina.

### 1. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/workout_api.git
cd workout_api
```

### 2. Configurar Ambiente Local (Opcional, recomendado para desenvolvimento)

Se você preferir rodar a aplicação Python diretamente sem Docker para o backend da API (o banco de dados ainda pode ser via Docker), siga estes passos:

```bash
# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No Windows
.\venv\Scripts\activate
# No macOS/Linux
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 3. Subir os Containers com Docker Compose

Para iniciar o banco de dados PostgreSQL e a aplicação FastAPI (se configurada no `docker-compose.yml` para rodar a API também), execute:

```bash
docker-compose up --build -d
```
Este comando irá construir as imagens (se necessário), criar e iniciar os serviços definidos no `docker-compose.yml` em segundo plano.

### 4. Executar Migrações do Banco de Dados (Alembic)

Após o banco de dados estar em execução, você precisará aplicar as migrações para criar as tabelas.

Se você estiver rodando a API via Docker Compose, você pode executar as migrações dentro do container da API:

```bash
docker-compose exec api alembic upgrade head
```

Se você estiver rodando a API localmente (passo 2), execute as migrações a partir do seu ambiente virtual ativado:

```bash
alembic upgrade head
```

### 5. Acessar a API

A API estará disponível em `http://localhost:8000` (ou a porta configurada no seu `docker-compose.yml`).

Você pode acessar a documentação interativa (Swagger UI) em `http://localhost:8000/docs`.