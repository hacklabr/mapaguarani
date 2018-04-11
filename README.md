# Mapa Guarany Yvyrupá

# Projeto Django Base

Projeto Django baseado no padrão [cookiecutter-django](http://cookiecutter-django.readthedocs.io/en/latest) e com diversas adaptações para uso na infraestrutura Docker-Rancher do hacklab/.

## Ambiente de desenvolvimento

Para clonar este repositório, execute:

`git clone git@gitlab.com:hacklab/base-django-project.git`

Levante o ambiente de desenvolvimento com `docker-compose up` e acesse [localhost:8000](http://localhost:8000).

## Importanto Bando de dados de testes (ou da produção)

Neste exemplo, apagamos e recriamos o banco para garantir que estamos importando sobre uma base limpa.
Este exemplo cobre a importação feita a partir de um binário (psqlc), adapte o os comandos para usar com outros formatos.

```
# Sobe somente container do postgres, importantes senão o django vai bloquer alterações no banco
docker-compose up postgres
# copia backup para dentro do container (isso pode ser melhorado)
docker cp mapaguarani.psqlc mapaguarani_postgres_1:/mapaguarani.psqlc
docker-compose exec -u postgres postgres dropdb django
docker-compose exec -u postgres postgres createdb django
docker-compose exec -u postgres postgres psql -d django -c "CREATE EXTENSION postgis;"
docker-compose exec -u postgres postgres pg_restore -O -x -n public -d django mapaguarani.psqlc
```

## Testes

Existem duas maneiras de se executar os testes automatizados localmente:

- Você já executou o comando `docker-compose up` e o servidor está funcionando.

```
docker-compose -f local.yml exec django pytest
```

- Você deseja apenas executar os testes sem necessariamente levantar o servidor. Antes é necessário construir a imagem do backend e disponibilizar o banco de dados para então executar o pytest via `docker run`

```
docker build -f compose/test/django/Dockerfile -t django_test .
docker run -d --env-file=./compose/test/test_env --name=postgres_test postgres:9.6
docker run --env-file=./compose/test/test_env --link=postgres_test:postgres \
  django_test /test.sh
```

## Variáveis de ambiente
### Banco de dados
- POSTGRES_HOST - opcional; padrão 'postgres'
- POSTGRES_DB - obrigatório
- POSTGRES_USER - obrigatório
- POSTGRES_PASSWORD - obrigatório

### Email
- MAILGUN_SENDER_DOMAIN - obrigatório em produção
- DJANGO_DEFAULT_FROM_EMAIL - obrigatório em produção
- DJANGO_MAILGUN_API_KEY - obrigatório em produção

### Django
- DJANGO_ALLOWED_HOSTS - obrigatório em produção
- DJANGO_ADMIN_URL - opcional
- DJANGO_SETTINGS_MODULE - opcional; use `config.settings.production` em produção
- DJANGO_ACCOUNT_ALLOW_REGISTRATION - opcional; padrão True
- DJANGO_SECRET_KEY - obrigatório em produção
- USE_CACHE - opcional; padrão True
- USE_DOCKER - opcional; desnecessário em produção; em ambientes locais, escreva 'yes' se estiver usando Docker

### Redis
- REDIS_URL - obrigatório em produção; exemplo: `redis://127.0.0.1:6379`

### Sentry
- DJANGO_SENTRY_DSN - opcional; só válido em produção

## Integrações de deploy
**Commits no branch `master`** fazem releases da versão em **desenvolvimento**.

**Tags** fazem releases em [**produção**](http://guarani.map.as/).


# Camadas Extras de Mapa

As camadas extras de dados de Paraguai, Bolivia e Argentina vieram do Who's On First Gazeteer.

