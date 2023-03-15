# BiblioteKA

# Documentação da API

- Link da documentação da API: https://biblioteka-production-be6a.up.railway.app/api/docs/swagger-ui/

## Tabela de Conteúdos

- [Visão Geral](#2-visão-geral)
- [Diagrama ER](#2-diagrama-er)
- [Início Rápido](#3-início-rápido)
  - [Instalando Dependências](#31-instalando-dependências)
  - [Variáveis de Ambiente](#32-variáveis-de-ambiente)
  - [Migrations](#33-migrations)
- [Autenticação](#4-autenticação)
- [Endpoints](#5-endpoints)

---

## 1. Visão Geral

Visão geral do projeto, um pouco das tecnologias usadas.

- [Python](https://docs.python.org/3/)
- [Django](https://docs.djangoproject.com/pt-br/4.1/)
- [Djangorestframework](https://www.django-rest-framework.org/)
- [Djangorestframework-simpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html)
- [PostgreSQL](https://www.postgresql.org/)

A URL base da aplicação:
https://biblioteka-production-be6a.up.railway.app

---

## 2. Diagrama ER

[ Voltar para o topo ](#tabela-de-conteúdos)

Diagrama ER da API definindo bem as relações entre as tabelas do banco de dados.

![DER](assets/biblioteka.drawio.png)

---

## 3. Início Rápido

[ Voltar para o topo ](#tabela-de-conteúdos)

### 3.1. Instalando Dependências

Clone o projeto em sua máquina e instale o ambiente virtual com o comando:

```shell
python -m venv venv

```

### 3.2. Aivar ambiente virtual

Ative seu venv:

```bash
# linux:
source venv/bin/activate

# windows:
.\venv\Scripts\activate
```

Em seguida, rode o comando:

```bash
pip install -r requirements.txt
```

Feito isso todos os framworks usados no projeto serão insatalados.

Crie um arquivo **.env**, copiando o formato do arquivo **.env.example**:

```
.env.example .env
```

Configure suas variáveis de ambiente com suas credenciais do Postgres e uma nova database da sua escolha.

### 3.3. Migrations

Execute as migrations com o comando:

```
python manage.py migrate
```

---

## 4. Autenticação

[ Voltar para o topo ](#tabela-de-conteúdos)

### Índice

- [Login](#1-login)
  - [POST - /login](#11-autenticação-de-usuário)

---

## 5. Endpoints

[ Voltar para o topo ](#tabela-de-conteúdos)

### Índice

- [Users](#2-users)
  - [POST - api/users/](#21-criação-de-usuário)
  - [GET - api/users/](#22-listando-usuários)
  - [GET - api/users/<user_id>](#23-Listar-usuário-por-id)
  - [PATCH - api/users/<user_id>](#24-atualizar-usuário-por-id)
  - [DELETE - api/users/<user_id>](#25-deletar-usuário-por-id)
- [Books](#3-books)

  - [POST - api/books/](#31-criação-de-livro)
  - [GET - api/books/](#32-listando-livros)
  - [PATCH - api/books/<book_id>/](#33-atualizar-livro-por-id)
  - [DELETE - api/books/<book_id>/](#34-deletar-livro-por-id)

- [Copy](#4-copy)

  - [POST - api/copy/](#41-criação-de-cópias)
  - [GET - api/copy/](#42-listando-cópias)
  - [DELETE - api/copy/<copy_id>/](#43-deletar-cópia-por-id)

- [Loan](#5-loans)

  - [POST - api/users/<user_id>/copy/<copy_id>/loan//](#51-criação-de-empréstimos)
  - [GET - api/loans/](#52-listando-empréstimos)
  - [PATCH - api/loans/<loan_id>/](#53-atualizar-empréstimos-por-id)

- [books_follow](#6-seguir-livros)
  - [POST - api/books/follow/<book_id>/](#61-seguir-livro)
  - [GET - /api/books/follow/<book_id>/ ](#62-lista-de-livros-seguidos)
  - [DELETE - /tasks/:task_id](#63-deixar-de-seguir-por-id)
-
---

---

## 1. **Login**

[ Voltar para Autenticação ](#4-autenticação)

O objeto User é definido como:

| Campo    | Tipo   | Descrição                    |
| -------- | ------ | ---------------------------- |
| email    | string | O e-mail do usuário.         |
| password | string | A senha de acesso do usuário |

### Endpoint

| Método | Rota       | Descrição                   |
| ------ | ---------- | --------------------------- |
| POST   | api/login/ | Autenticação de um usuário. |

---

### 1.1. **Autenticação de Usuário**

[ Voltar para Autenticação ](#4-autenticação)

### `api/login/`

### Exemplo de Request:

```
POST api/login/
Host: https://biblioteka-production-be6a.up.railway.app
Authorization: Bearer token
Content-type: application/json
```

### Corpo da Requisição:

```json
{
  "email": "seuemail@mail.com",
  "password": "123456"
}
```

### Exemplo de Response:

```
200 Ok
```

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc0FkbSI6dHJ1ZSwiaXNBY3RpdmUiOnRydWUsInR5cGVVc2VyIjoiRGV2IiwiaWF0IjoxNjc0MDQ5NTI1LCJleHAiOjE2NzQxMzU5MjUsInN1YiI6ImQyOWY2Mzk2LWQ1MDMtNDg3Ny04NWRhLWY1NTNhMWY2ODE3ZSJ9.wWeXDDMXcJ3mKMC9IEFmljgTC3sPt95U3UR_-i6dpsQ"
}
```

### Possíveis Erros:

| Código do Erro   | Descrição                                            |
| ---------------- | ---------------------------------------------------- |
| 401 Unauthorized | "No active account found with the given credentials. |

---

## 2. **Users**

[ Voltar para os Endpoints ](#5-endpoints)

O objeto User é definido como:

| Campo       | Tipo    | Descrição                                                        |
| ----------- | ------- | ---------------------------------------------------------------- | --- |
| id          | string  | Identificador único do usuário                                   |
| username    | string  | O nome do usuário.                                               |
| email       | string  | O e-mail do usuário.                                             |
| password    | string  | A senha de acesso do usuário                                     |
| first_name  | string  | O primeiro nome do usuário.                                      |
| last_name   | string  | O sobrenome do usuário.                                          |
| is_employee | boolean | Define se um usuário é Administrador ou não no caso Funcionário. |
| is_blocked  | boolean | Define se um usuário está bloqueado ou não.                      |     |

### Endpoints

| Método | Rota                 | Descrição                                        |
| ------ | -------------------- | ------------------------------------------------ |
| POST   | api/users/           | Criação de um usuário.                           |
| GET    | api/users/           | Listagem de todos os usuários                    |
| GET    | api/users/<user_id>/ | Lista um usuário usando seu ID como parâmetro    |
| PATCH  | api/users/<user_id>/ | Atualiza um usuário usando seu ID como parâmetro |
| DELETE | api/users/<user_id>/ | Deleta um usuário usando seu ID como parâmetro   |

---

### 2.1. **Criação de Usuário**

[ Voltar para os Endpoints ](#5-endpoints)

### `api/users/`

### Exemplo de Request:

```
POST api/users/
Host: https://biblioteka-production-be6a.up.railway.appv
Authorization: none
Content-type: application/json
```

### Corpo da Requisição:

```json
{
  "username": "Seu username",
  "password": "1234",
  "email": "seuemail@mail.com",
  "first_name": "seu nome",
  "last_name": "seu sobrenome",
  "is_employee": true,
  "is_blocked": false
}
```

### Exemplo de Response:

```
201 Created
```

```json
{
  "username": "Seu username",
  "password": "1234",
  "email": "seuemail@mail.com",
  "first_name": "seu nome",
  "last_name": "seu sobrenome",
  "is_employee": true,
  "is_blocked": false
}
```

### Possíveis Erros:

| Código do Erro  | Descrição                                                  |
| --------------- | ---------------------------------------------------------- |
| 400 Bad Request | "username": [ "A user with that username already exists."] |
| 400 Bad Request | "email": ["This field must be unique."]                    |

### 2.2. **Listando Usuários**

[ Voltar aos Endpoints ](#5-endpoints)

### `api/users/`

### Exemplo de Request:

```
GET api/users/
Host: https://biblioteka-production-be6a.up.railway.appv
Authorization: Bearer token
Content-type: application/json
```

### Corpo da Requisição:

```json
Vazio
```

### Exemplo de Response:

```
200 OK
```

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "username": "Seu username",
      "password": "1234",
      "email": "seuemail@mail.com",
      "first_name": "seu nome",
      "last_name": "seu sobrenome",
      "is_employee": true,
      "is_blocked": false
    },
    {
      "username": "outro username",
      "password": "1234",
      "email": "email@mail.com",
      "first_name": "seu nome",
      "last_name": "seu sobrenome",
      "is_employee": true,
      "is_blocked": false
    }
  ]
}
```

### Possíveis Erros:

| Código do Erro   | Descrição          |
| ---------------- | ------------------ |
| 403 Forbidden    | User is not admin. |
| 401 Unauthorized | Invalid token.     |

---

### 2.3. **Listar Usuário por ID**

[ Voltar aos Endpoints ](#5-endpoints)

### `api/users/<user_id>/`

### Exemplo de Request:

```
PATCH api/users/<user_id>/
Host: https://biblioteka-production-be6a.up.railway.appv
Authorization: Bearer token
Content-type: application/json
```

### Parâmetros da Requisição:

| Parâmetro | Tipo   | Descrição                             |
| --------- | ------ | ------------------------------------- |
| user_id   | string | Identificador único do usuário (User) |

### Corpo da Requisição:

Necessita de apenas um campo para fazer a atualização parcial.

```json
{
  "username": "Seu username",
  "password": "1234",
  "email": "seuemail@mail.com",
  "first_name": "seu nome",
  "last_name": "seu sobrenome",
  "is_employee": true,
  "is_blocked": false
}
```

### Exemplo de Response:

```
200 OK
```

```json
{
  "id": "904e976a-c16f-40cc-9ac5-39f947455148",
  "username": "Seu username",
  "password": "1234",
  "email": "seuemail@mail.com",
  "first_name": "seu nome",
  "last_name": "seu sobrenome",
  "is_employee": true,
  "is_blocked": false
}
```

### Possíveis Erros:

| Código do Erro   | Descrição                                     |
| ---------------- | --------------------------------------------- |
| 401 Unauthorized | Authentication credentials were not provided. |

---

### 2.4. **Atualizar Usuário por ID**

[ Voltar aos Endpoints ](#5-endpoints)

### `api/users/<user_id>/`

### Exemplo de Request:

```
PATCH api/users/<user_id>/
Host: https://biblioteka-production-be6a.up.railway.appv
Authorization: Bearer token
Content-type: application/json
```

### Parâmetros da Requisição:

| Parâmetro | Tipo   | Descrição                             |
| --------- | ------ | ------------------------------------- |
| user_id   | string | Identificador único do usuário (User) |

### Corpo da Requisição:

Necessita de apenas um campo para fazer a atualização parcial.

```json
{
  "username": "username editado",
  "email": "bibliotekag27@gmail.com",
  "first_name": "Raphael",
  "last_name": "Damasceno",
  "is_employee": true,
  "is_blocked": false
}
```

### Exemplo de Response:

```
200 OK
```

```json
{
  "id": "904e976a-c16f-40cc-9ac5-39f947455148",
  "username": "username editado",
  "email": "bibliotekag27@gmail.com",
  "first_name": "Raphael",
  "last_name": "Damasceno",
  "is_employee": true,
  "is_blocked": false
}
```

### Possíveis Erros:

| Código do Erro   | Descrição                                     |
| ---------------- | --------------------------------------------- |
| 401 Unauthorized | Authentication credentials were not provided. |

---

### 2.5. **Deletar Usuário por ID**

[ Voltar aos Endpoints ](#5-endpoints)

### `api/users/<user_id>/`

### Exemplo de Request:

```
DELETE api/users/<user_id>/
Host: https://biblioteka-production-be6a.up.railway.appv
Authorization: Bearer token
Content-type: application/json
```

### Parâmetros da Requisição:

| Parâmetro | Tipo   | Descrição                             |
| --------- | ------ | ------------------------------------- |
| user_id   | string | Identificador único do usuário (User) |

### Corpo da Requisição:

Necessita de apenas um campo para fazer a atualização parcial.

```json
{
  "username": "username editado",
  "email": "bibliotekag27@gmail.com",
  "first_name": "Raphael",
  "last_name": "Damasceno",
  "is_employee": true,
  "is_blocked": false
}
```

### Exemplo de Response:

```
204 No Content
```

```json
{
  "id": "904e976a-c16f-40cc-9ac5-39f947455148",
  "username": "username editado",
  "email": "bibliotekag27@gmail.com",
  "first_name": "Raphael",
  "last_name": "Damasceno",
  "is_employee": true,
  "is_blocked": false
}
```

### Possíveis Erros:

| Código do Erro   | Descrição                                     |
| ---------------- | --------------------------------------------- |
| 401 Unauthorized | Authentication credentials were not provided. |

---

## 3. **Books**

[ Voltar para os Endpoints ](#5-endpoints)

O objeto Ong é definido como:

| Campo        | Tipo   | Descrição                    |
| ------------ | ------ | ---------------------------- |
| id           | string | Identificador único do livro |
| name         | string | O nome do livro.             |
| description  | string | Descrição do livro.          |
| author       | string | O nome do autor.             |
| category     | string | A categoria do livro.        |
| pages        | number | Números de páginas do livro. |
| release_date | string | data do lançamento do livro  |

---

### Endpoints

| Método | Rota                 | Descrição                                       |
| ------ | -------------------- | ----------------------------------------------- |
| POST   | api/books/           | Criação do livro                                |
| GET    | api/books/           | Lista todos os livros.                          |
| GET    | api/books/<book_id>/ | Lista um livro pelo identificador único.        |
| PATCH  | api/books/<book_id>/ | Atualiza uma livro usando seu ID como parâmetro |
| DELETE | api/books/<book_id>/ | Deleta uma ong usando seu ID como parâmetro.    |

---

### 3.1. **Criação de livro**

[ Voltar para os Endpoints ](#5-endpoints)

### `api/books/<book_id>/`

### Exemplo de Request:

```
POST api/books/
Host: https://biblioteka-production-be6a.up.railway.appv
Authorization: none
Content-type: application/json
```

### Corpo da Requisição:

```json
{
  "name": "O Poder Do Subconsciente",
  "description": "Um dos melhores e mais populares livros de auto-ajuda já escritos...",
  "author": "Joseph Murphy",
  "category": "Autoajuda",
  "pages": 308,
  "release_date": "2012-12-14"
}
```

### Exemplo de Response:

```
201 Created
```

```json
{
  "id": "a057b7cb-fb75-44da-8de2-0ca4d2154909",
  "name": "O Poder Do Subconsciente",
  "description": "Um dos melhores e mais populares livros de auto-ajuda já escritos...",
  "author": "Joseph Murphy",
  "category": "Autoajuda",
  "pages": 308,
  "release_date": "2012-12-14",
  "copies": 0
}
```

### Possíveis Erros:

| Código do Erro   | Descrição                                                    |
| ---------------- | ------------------------------------------------------------ |
| 401 Unauthorized | Authorization header must contain two space-delimited values |
| 401 Unauthorized | bad_authorization_header                                     |

---

### 3.2. **Listando Livros**

[ Voltar aos Endpoints ](#5-endpoints)

### `api/books/`

### Exemplo de Request:

```
GET api/books/
Host: https://biblioteka-production-be6a.up.railway.appv
Authorization: Bearer token
Content-type: application/json
```

### Corpo da Requisição:

```json
Vazio
```

### Exemplo de Response:

```
200 OK
```

```json
[
  {
    "id": "0485e599-12c4-4930-a74c-182aa14f5c02",
    "name": "O Poder Do Subconsciente",
    "description": "Um dos melhores e mais populares livros de auto-ajuda já escritos...",
    "author": "Joseph Murphy",
    "category": "Autoajuda",
    "pages": 308,
    "release_date": "2012-12-14",
    "copies": 0
  }
]
```

### Possíveis Erros:

| Código do Erro   | Descrição                                                     |
| ---------------- | ------------------------------------------------------------- |
| 401 Unauthorized | Authorization header must contain two space-delimited values. |

---

### 3.3. **Atualizar livro por ID**

[ Voltar aos Endpoints ](#5-endpoints)

### `api/books/<book_id>/`

### Exemplo de Request:

```
PATCH api/books/<book_id>/
Host: https://biblioteka-production-be6a.up.railway.appv
Authorization: Bearer token
Content-type: application/json
```

### Parâmetros da Requisição:

| Parâmetro | Tipo   | Descrição                           |
| --------- | ------ | ----------------------------------- |
| book_id   | string | Identificador único do livro (book) |

### Corpo da Requisição:

Necessita de apenas um campo para fazer a atualização parcial.

```json
{
  "name": "O Poder Do Subconsciente editado"
}
```

### Exemplo de Response:

```
200 OK
```

```json
{
  "id": "0485e599-12c4-4930-a74c-182aa14f5c02",
  "name": "O Poder Do Subconsciente editado",
  "description": "Um dos melhores e mais populares livros de auto-ajuda já escritos...",
  "author": "Joseph Murphy",
  "category": "Autoajuda",
  "pages": 308,
  "release_date": "2012-12-14",
  "copies": 0
}
```

### Possíveis Erros:

| Código do Erro   | Descrição                                                    |
| ---------------- | ------------------------------------------------------------ |
| 401 Unauthorized | Authorization header must contain two space-delimited values |

---

### 3.4. **Deletar livro por ID**

[ Voltar aos Endpoints ](#5-endpoints)

### `api/books/<book_id>/`

### Exemplo de Request:

```
PATCH api/books/<book_id>/
Host: https://biblioteka-production-be6a.up.railway.appv
Authorization: Bearer token
Content-type: application/json
```

### Parâmetros da Requisição:

| Parâmetro | Tipo   | Descrição                           |
| --------- | ------ | ----------------------------------- |
| book_id   | string | Identificador único do livro (book) |

### Corpo da Requisição:

vazio.

### Exemplo de Response:

```
204 No Content
```

### Possíveis Erros:

| Código do Erro   | Descrição                                                     |
| ---------------- | ------------------------------------------------------------- |
| 401 Unauthorized | "Authorization header must contain two space-delimited values |

---

## 4. **Copy**

[ Voltar para os Endpoints ](#5-endpoints)

O objeto news é definido como:

| Campo        | Tipo   | Descrição                    |
| ------------ | ------ | ---------------------------- |
| id           | string | Identificador único do livro |
| name         | string | O nome do livro.             |
| description  | string | Descrição do livro.          |
| author       | string | O nome do autor.             |
| category     | string | A categoria do livro.        |
| pages        | number | Números de páginas do livro. |
| release_date | string | data do lançamento do livro  |

---

### Endpoints

| Método | Rota                | Descrição                                       |
| ------ | ------------------- | ----------------------------------------------- |
| POST   | api/copy/           | Criação de cópias.                              |
| GET    | api/copy/           | Lista todas as cópias.                          |
| DELETE | api/copy/<copy_id>/ | Deleta uma notícia usando seu ID como parâmetro |

---

### 4.1. **Criação de cópias**

[ Voltar para os Endpoints ](#5-endpoints)

### `api/copy/`

### Exemplo de Request:

```
POST api/copy/
Host: https://biblioteka-production-be6a.up.railway.appv
Authorization: Bearer token
Content-type: application/json
```

### Corpo da Requisição:

```json
{

	"name": "O Poder Do Subconsciente",
	"description": "Um dos melhores e mais populares livros de auto-ajuda já escritos...",
	"author": "Joseph Murphy",
	"category": "Autoajuda",
	"pages": 308,
	"release_date": "2012-12-14",
	"copies": 3
}
}
```

### Exemplo de Response:

```
201 Created
```

```json
{
  "id": "a057b7cb-fb75-44da-8de2-0ca4d2154909",
  "name": "O Poder Do Subconsciente",
  "description": "Um dos melhores e mais populares livros de auto-ajuda já escritos...",
  "author": "Joseph Murphy",
  "category": "Autoajuda",
  "pages": 308,
  "release_date": "2012-12-14",
  "copies": 3
}
```

### Possíveis Erros:

| Código do Erro   | Descrição                                     |
| ---------------- | --------------------------------------------- |
| 401 Unauthorized | Authentication credentials were not provided. |

---

### 4.2. **Listando Cópias**

[ Voltar aos Endpoints ](#5-endpoints)

### `api/copy/`

### Exemplo de Request:

```
GET api/copy/
Host: https://biblioteka-production-be6a.up.railway.appv
Authorization: Bearer token
Content-type: application/json
```

### Corpo da Requisição:

```json
Vazio
```

### Exemplo de Response:

```
200 OK
```

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "ed88f775-a0c0-45e6-b36e-8ed29938f233",
      "is_avaliable": true,
      "book": {
        "id": "a057b7cb-fb75-44da-8de2-0ca4d2154909",
        "name": "O Poder Do Subconsciente",
        "description": "Um dos melhores e mais populares livros de auto-ajuda já escritos...",
        "author": "Joseph Murphy",
        "category": "Autoajuda",
        "pages": 308,
        "release_date": "2012-12-14",
        "copies": 3
      },
      "borrowers": [
        {
          "id": "5ca25e9c-246d-46df-9244-bebf8ec55bf9",
          "username": "Eduardo",
          "email": "raphael_damasceno07@hotmail.com",
          "first_name": "Eduardo",
          "last_name": "Damasceno",
          "is_employee": false,
          "is_blocked": false
        }
      ]
    },
    {
      "id": "ce6461aa-b8c5-4b1a-8245-dae73bf8cc4d",
      "is_avaliable": true,
      "book": {
        "id": "a057b7cb-fb75-44da-8de2-0ca4d2154909",
        "name": "O Poder Do Subconsciente",
        "description": "Um dos melhores e mais populares livros de auto-ajuda já escritos...",
        "author": "Joseph Murphy",
        "category": "Autoajuda",
        "pages": 308,
        "release_date": "2012-12-14",
        "copies": 3
      },
      "borrowers": []
    }
  ]
}
```

### Possíveis Erros:

| Código do Erro   | Descrição                                     |
| ---------------- | --------------------------------------------- |
| 401 Unauthorized | Authentication credentials were not provided. |

---

### 4.3. **Listando cópias por ID**

[ Voltar aos Endpoints ](#5-endpoints)

### `api/copy/copy_id`

### Exemplo de Request:

```
GET api/copy/d3ede8d8-e7d8-41e4-91fa-8e52e43e3d65
Host: https://biblioteka-production-be6a.up.railway.appv
Authorization: Bearer token
Content-type: application/json
```

### Parâmetros da Requisição:

### 4.3. **Deletar Cópia por ID**

[ Voltar aos Endpoints ](#5-endpoints)

### `api/copy/copy_id`

### Exemplo de Request:

```
DELETE api/copy/<copy_id>/
Host: https://biblioteka-production-be6a.up.railway.appv
Authorization: Bearer token
Content-type: application/json
```

### Parâmetros da Requisição:

| Parâmetro | Tipo   | Descrição                             |
| --------- | ------ | ------------------------------------- |
| user_id   | string | Identificador único da notícia (news) |

### Corpo da Requisição:

vazio.

### Exemplo de Response:

```
204 No Content
```

### Possíveis Erros:

| Código do Erro   | Descrição                                     |
| ---------------- | --------------------------------------------- |
| 401 Unauthorized | Authentication credentials were not provided. |

---

## 5. **Loans**

[ Voltar para os Endpoints ](#5-endpoints)

O objeto Project é definido como:

| Campo      | Tipo           | Descrição                           |
| ---------- | -------------- | ----------------------------------- |
| id         | string         | Identificador único do empréstimo   |
| lend_at    | string         | Data do empréstimo.                 |
| refund_at  | string or null | Data da devolução do empréstimo.    |
| expires_at | string or null | Data da expiração do empréstimo.    |
| book_copy  | boolean        | Identificador único do empréstimo.  |
| book_name  | string         | Nome do livro que a cópia pertence. |
| borrower   | string         | Identificador único do usuário.     |

---

### Endpoints

| Método | Rota                                     | Descrição                                        |
| ------ | ---------------------------------------- | ------------------------------------------------ |
| POST   | api/users/<user_id>/copy/<copy_id>/loan/ | Criação de um projeto.                           |
| GET    | api/loans                                | Lista todos os projetos.                         |
| PATCH  | api/loans/<loan_id>/                     | Atualiza um projeto usando seu ID como parâmetro |

---

### 5.1. **Criação de empréstimos**

[ Voltar para os Endpoints ](#5-endpoints)

### `api/users/<user_id>/copy/<copy_id>/loan/`

### Exemplo de Request:

```
POST api/users/<user_id>/copy/<copy_id>/loan/
Host: https://biblioteka-production-be6a.up.railway.appv
Authorization: Bearer token
Content-type: application/json
```

### Corpo da Requisição:

```json
  vazio
```

### Exemplo de Response:

```
201 Created
```

```json
{
  "id": "05d287e3-1195-478b-950b-cb130a2fca86",
  "lend_at": "2023-03-14",
  "refund_at": "2023-03-22",
  "expires_at": "2023-03-22",
  "book_copy": "ed88f775-a0c0-45e6-b36e-8ed29938f233",
  "book_name": "O Poder Do Subconsciente",
  "borrower": "seuemail@mail.com"
}
```

### Possíveis Erros:

| Código do Erro   | Descrição                                     |
| ---------------- | --------------------------------------------- |
| 401 Unauthorized | Authentication credentials were not provided. |

---

### 5.2. **Listando empréstimos**

[ Voltar aos Endpoints ](#5-endpoints)

### `api/loans/`

### Exemplo de Request:

```
GET api/loans/`
Host: https://biblioteka-production-be6a.up.railway.appv
Authorization: Bearer token
Content-type: application/json
```

### Corpo da Requisição:

```json
Vazio
```

### Exemplo de Response:

```
200 OK
```

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "05d287e3-1195-478b-950b-cb130a2fca86",
      "lend_at": "2023-03-14",
      "refund_at": null,
      "expires_at": "2023-03-22",
      "book_copy": "ed88f775-a0c0-45e6-b36e-8ed29938f233",
      "book_name": "O Poder Do Subconsciente",
      "borrower": "raphael_damasceno07@hotmail.com"
    }
  ]
}
```

### Possíveis Erros:

| Código do Erro   | Descrição                                 |
| ---------------- | ----------------------------------------- |
| 401 Unauthorized | Given token not valid for any token type. |

---

### 5.3. **Atualizar empréstimos por ID**

[ Voltar aos Endpoints ](#5-endpoints)

### `api/loans/loan_id/`

### Exemplo de Request:

```
PATCH api/loans/loan_id/`
Host: https://biblioteka-production-be6a.up.railway.appv
Authorization: Bearer token
Content-type: application/json
```

### Parâmetros da Requisição:

| Parâmetro | Tipo   | Descrição                             |
| --------- | ------ | ------------------------------------- |
| loan_id   | string | Identificador único do projeto (loan) |

### Corpo da Requisição:

Necessita de apenas um campo para fazer a atualização parcial.

```json
{
  "refund_at": "2023-03-22"
}
```

### Exemplo de Response:

```
200 OK
```

```json
{
  "id": "05d287e3-1195-478b-950b-cb130a2fca86",
  "lend_at": "2023-03-14",
  "refund_at": "2023-03-22",
  "expires_at": "2023-03-22",
  "book_copy": "ed88f775-a0c0-45e6-b36e-8ed29938f233",
  "book_name": "O Poder Do Subconsciente",
  "borrower": "seuemail@mail.com"
}
```

### Possíveis Erros:

| Código do Erro   | Descrição                                 |
| ---------------- | ----------------------------------------- |
| 401 Unauthorized | Given token not valid for any token type. |

---

## 6. **Seguir livros**

[ Voltar para os Endpoints ](#5-endpoints)

O objeto Task é definido como:

| Campo  | Tipo    | Descrição                            |
| ------ | ------- | ------------------------------------ |
| id     | string  | Identificador único da tarefa.       |
| title  | string  | Título da tarefa.                    |
| status | boolean | status da tarefa.                    |
| ong    | string  | Nome da ong que solicitou o projeto. |

---

### Endpoints

| Método | Rota                              | Descrição                                   |
| ------ | --------------------------------- | ------------------------------------------- |
| POST   | api/books/follow/<book_id>/       | curtir um livro.                            |
| GET    | /api/books/follow/<book_id>/      | Lista todos as curtidas.                    |
| GET    | /api/books/follow/<book_id>/user/ | Lista todos os livros que o usuário curtiu. |
| DELETE | /api/books/follow/<book_id>/user/ | rota para deixar de curtir                  |

---

### 6.1. **Seguir livro**

[ Voltar para os Endpoints ](#5-endpoints)

### `api/books/follow/<book_id>/`

### Exemplo de Request:

```
api/books/follow/<book_id>/
Host: https://biblioteka-production-be6a.up.railway.appv
Authorization: Bearer token
Content-type: application/json
```

### Corpo da Requisição:

```json
  vazio
```

### Parâmetros da Requisição:

| Parâmetro | Tipo   | Descrição                                  |
| --------- | ------ | ------------------------------------------ |
| book_id   | string | Identificador único da livro a ser seguido |

### Exemplo de Response:

```
201 Created
```

```json
{
  "id": 1,
  "date": "2023-03-14T14:33:11.320748Z",
  "book": {
    "id": "5cd2a7b5-194e-4d53-9656-c3405d2888a1",
    "name": "O Poder Do Subconsciente",
    "description": "Um dos melhores e mais populares livros de auto-ajuda já escritos...",
    "author": "Joseph Murphy",
    "category": "Autoajuda",
    "pages": 308,
    "release_date": "2012-12-14",
    "copies": 0
  },
  "user": {
    "id": "9b56ffb8-e761-43cb-97d6-3f2b389db269",
    "username": "Fernando",
    "email": "rdamasceno1852@gmail.com",
    "first_name": "Fernando",
    "last_name": "Damasceno",
    "is_employee": false,
    "is_blocked": false
  }
}
```

### Possíveis Erros:

| Código do Erro   | Descrição                                     |
| ---------------- | --------------------------------------------- |
| 401 Unauthorized | Authentication credentials were not provided. |

---

### 6.2. **Lista de livros seguidos**

[ Voltar aos Endpoints ](#5-endpoints)

### `/api/books/follow/<book_id>/      `

### Exemplo de Request:

```
GET /api/books/follow/<book_id>/
Host: https://biblioteka-production-be6a.up.railway.appv
Authorization: Bearer token
Content-type: application/json
```

### Parâmetros da Requisição:

| Parâmetro | Tipo   | Descrição                                                                     |
| --------- | ------ | ----------------------------------------------------------------------------- |
| book_id   | string | Identificador único do projeto em que todas os livros seguidos serão listados |

### Corpo da Requisição:

```json
Vazio
```

### Exemplo de Response:

```
200 OK
```

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "date": "2019-08-24T14:15:22Z",
  "book": {
    "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
    "name": "string",
    "description": "string",
    "author": "string",
    "category": "string",
    "pages": 2147483647,
    "release_date": "2019-08-24",
    "copies": 0,
    "follows": []
  },
  "user": {
    "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "is_employee": true,
    "is_blocked": true
  }
}
```

### Possíveis Erros:

| Código do Erro   | Descrição                                     |
| ---------------- | --------------------------------------------- |
| 401 Unauthorized | Authentication credentials were not provided. |

---

### 6.3. **Deixar de seguir por ID**

[ Voltar aos Endpoints ](#5-endpoints)

### `/api/books/follow/<follow_id`

### Exemplo de Request:

```
DELETE `/api/books/follow/<follow_id`
Host: https://biblioteka-production-be6a.up.railway.appv
Authorization: Bearer token
Content-type: application/json
```

### Parâmetros da Requisição:

| Parâmetro | Tipo   | Descrição                      |
| --------- | ------ | ------------------------------ |
| follow_id | string | Identificador único de seguir) |

### Corpo da Requisição:

vazio.

### Exemplo de Response:

```
204 No Content
```

### Possíveis Erros:

| Código do Erro   | Descrição                                     |
| ---------------- | --------------------------------------------- |
| 401 Unauthorized | Authentication credentials were not provided. |

---
