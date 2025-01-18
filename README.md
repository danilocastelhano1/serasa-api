# Cadastro de Produtor Rural em Django Rest Framework

Baseado no [teste scenario](https://github.com/brain-ag/trabalhe-conosco)

## Instalação
#### Em Windows:
Baixar, instalar e executar o [Docker Desktop](https://www.docker.com/products/docker-desktop/)

#### Passos:
- Clonar o projeto, entrar na pasta dele e via terminal/dos:
- Renomear o .env-sample para .env
- Rodar o comando: ```docker-compose up --build```
- Depois de finalizado o comando acima, rodar o comando: ```docker-compose up``` esperar completar todo processo de instalação
- Se tudo der certo verá um prompt igual este:
````
backend-app-1  | INFO 2024-06-20 18:17:30,603 autoreload Watching for file changes with StatReloader
backend-app-1  | Performing system checks...
backend-app-1  |
backend-app-1  | System check identified no issues (0 silenced).
backend-app-1  | June 20, 2024 - 18:17:31
backend-app-1  | Django version 4.2.9, using settings 'app.settings'
backend-app-1  | Starting development server at http://0.0.0.0:8000/
backend-app-1  | Quit the server with CONTROL-C.
````

### Dentro da pasta do projeto está a collection via postman
```Serasa.postman_collection.json```
Só importar dentro do postman.

### Acessando o Django Admin
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

usuário: admin

senha: 123456

### Acessando o Swagger
[http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

### Acessando o redoc
[http://127.0.0.1:8000/redoc/#tag/api](http://127.0.0.1:8000/redoc/#tag/api)

## Para desenvolvedores
- Instalar o pré commit para formatação e qualidade do código
- Testes feitos com o unittest, para rodar os testes:
- listar os containers ``docker ps``
- entre dentro do container, ``docker exec -it 8a389fd6b2c2 /bin/bash`` e rode: ``python manage.py test``
- Utilizado pré commit para melhor qualidade do sistema
- Utilizado Black, Flake8, Isort
Qualquer dúvida estou à disposição no e-mail: danilocastelhano@hotmail.com