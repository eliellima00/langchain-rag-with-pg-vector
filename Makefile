APP_CONTAINER = rag-app
DOCKER_COMPOSE = docker compose

# Sobe os containers e inicializa o banco
.PHONY: up
up:
	$(DOCKER_COMPOSE) up -d

# Para os containers
.PHONY: down
down:
	$(DOCKER_COMPOSE) down

# Mostra os logs do container principal
.PHONY: logs
logs:
	$(DOCKER_COMPOSE) logs -f $(APP_CONTAINER)

# Roda o script de ingestão dentro do container
.PHONY: ingest
ingest:
	$(DOCKER_COMPOSE) exec $(APP_CONTAINER) python3 src/ingest.py

# Roda o chat (que usa o search.py internamente)
.PHONY: chat
chat:
	$(DOCKER_COMPOSE) exec $(APP_CONTAINER) python3 src/chat.py

# Limpa tudo (containers, volumes, cache)
.PHONY: clean
clean:
	$(DOCKER_COMPOSE) down -v
	docker system prune -f
