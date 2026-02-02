# Sistemas Portfólio

Este é um projeto de portfólio que apresenta um sistema de autenticação de usuários e varios sistemas internos, esta sendo desenvolvido com Flask e SQLite.

## Funcionalidades Atuais

- **Autenticação de Usuários**: 
  - Registro de novos usuários com nome, nome de usuário e senha.
  - Login de usuários com validação de credenciais.
  - Logout de usuários.

- **Gerenciador de Tarefas (To-Do List)**:
  - Adicionar novas tarefas.
  - Listar tarefas pendentes e concluídas.
  - Marcar tarefas como concluídas.
  - Deletar tarefas.

## Estrutura do Projeto

```
.
├── app.py
├── static/
├── templates/
│   ├── inicial.html
│   ├── login.html
│   ├── registrar.html
│   ├── sistemas.html
│   ├── to_do_add.html
│   ├── to_do_list.html
```

- **app.py**: Arquivo principal que contém a lógica do backend e as rotas do Flask.
- **static/**: Diretório para arquivos estáticos como imagens, JavaScript e CSS.
- **templates/**: Diretório para os arquivos HTML do projeto.

## Pré-requisitos

- Python 3.7 ou superior
- Pip (gerenciador de pacotes do Python)

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/celsorma102/sistemas-portifolio.git
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd sistemas-portifolio
   ```

3. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   ```

4. Ative o ambiente virtual:
   - No Windows:
     ```bash
     venv\Scripts\activate
     ```
   - No Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

5. Instale as dependências:
   ```bash
   pip install flask werkzeug pytz
   ```

6. Inicie o servidor:
   ```bash
   python app.py
   ```

7. Acesse o sistema no navegador:
   ```
   http://127.0.0.1:5000
   ```

## Banco de Dados

O projeto utiliza dois bancos de dados SQLite:

- **usuarios.db**: Armazena informações dos usuários (nome, nome de usuário e senha).
- **tarefas.db**: Armazena as tarefas dos usuários (descrição, status de conclusão, data de criação e data de conclusão).

Os bancos de dados são criados automaticamente ao iniciar o projeto pela primeira vez.

## Estrutura das Tabelas

### Tabela: usuarios
- **id**: Identificador único do usuário (INTEGER, PRIMARY KEY, AUTOINCREMENT).
- **nome**: Nome do usuário (TEXT, NOT NULL).
- **usuario**: Nome de usuário único (TEXT, UNIQUE, NOT NULL).
- **senha**: Senha do usuário (TEXT, NOT NULL).

### Tabela: tarefas
- **id**: Identificador único da tarefa (INTEGER, PRIMARY KEY, AUTOINCREMENT).
- **usuario**: Nome do usuário associado à tarefa (TEXT, NOT NULL).
- **descricao**: Descrição da tarefa (TEXT, NOT NULL).
- **concluida**: Status da tarefa (BOOLEAN, NOT NULL, 0 para não concluída, 1 para concluída).
- **data_criacao**: Data e hora de criação da tarefa (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP).
- **data_conclusao**: Data e hora de conclusão da tarefa (TIMESTAMP, NULL).

## Licença

Este projeto é de uso livre e aberto para estudos e modificações.