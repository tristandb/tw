PROJECT_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
COMPOSE := docker compose --project-directory $(PROJECT_DIR)
COMPOSE_BASE := -f $(PROJECT_DIR)/compose.yml
COMPOSE_DEV := $(COMPOSE_BASE) -f $(PROJECT_DIR)/compose.dev.yml

ARGS ?=

.PHONY: prod dev watch prod-down dev-down watch-down ps logs

prod:
	$(COMPOSE) $(COMPOSE_BASE) up --build $(ARGS)

prod-down:
	$(COMPOSE) $(COMPOSE_BASE) down $(ARGS)

dev:
	$(COMPOSE) $(COMPOSE_DEV) up --build $(ARGS)

watch:
	$(COMPOSE) $(COMPOSE_DEV) watch $(ARGS)

dev-down:
	$(COMPOSE) $(COMPOSE_DEV) down $(ARGS)

watch-down:
	$(COMPOSE) $(COMPOSE_DEV) down $(ARGS)

ps:
	$(COMPOSE) $(COMPOSE_BASE) ps

logs:
	$(COMPOSE) $(COMPOSE_BASE) logs -f $(ARGS)

