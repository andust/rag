RAG_SERVICE_NAME=rag_user_srv

PLAYWRIGHT_NAME=rag_playwright

migration_dir = migrate/migrations/

playwright-test:
	docker compose run --rm ${PLAYWRIGHT_NAME}

# USER SERVICE
user-build-api:
	docker compose exec ${RAG_SERVICE_NAME} env GOOS=linux CGO_ENABLED=0 go build -o api cmd/api/main.go 

user-build-scripts:
	docker compose exec ${RAG_SERVICE_NAME} env GOOS=linux CGO_ENABLED=0 go build -o scripts cmd/scripts/main.go 

user-build: user-build-api user-build-scripts
	@echo "build all user services"

# ALL
build-api: user-build-api
	@echo "build all services api"

# ALL
build-script: user-build-scripts
	@echo "build all services scripts"
