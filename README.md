## Prepare environment

```bash
python3 -m venv env
source env/bin/activate
```

## Install dependencies of microservice

Move to one of the microservices and run the following command

```bash
pip install -r ./requirements.txt
```

## Run microservice

After installing dependencies run the microservice server with the following command

```bash
sh ./bootstrap
```

## Run microservice tests

```bash
pytest --cov=src -v -s --cov-fail-under=80
```

## Run docker compose

```bash
docker-compose -f "docker-compose.yml" up -d
```