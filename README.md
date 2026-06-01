# auth-gateway-platform

Auth Gateway Platform is a Docker-based authentication and routing demo that combines Keycloak, Traefik, a FastAPI auth middleware, and OpenTelemetry/observability tooling.

## Services

- `traefik`: edge proxy and router.
- `postgres`: Keycloak database.
- `keycloak`: identity provider for OAuth2/OpenID Connect.
- `pgadmin`: Postgres administration UI.
- `mailhog`: SMTP test mail service.
- `auth-middleware`: FastAPI app that verifies bearer tokens and provides Traefik forward-auth.
- `otel-collector`: OpenTelemetry collector for trace ingestion.
- `docker-proxy`: docker-socket-proxy used by Traefik to discover Docker services.

# 📂 Directory Structure

auth-gateway-platform/
├── docker/                 # Infrastructure configurations (Keycloak, Postgres, etc.)
├── deployments/            # K8s manifests and reusable GitHub Action templates
├── services/               # Microservices organized by domain (Clean Architecture)
│   ├── auth-middleware/
│   ├── api-gateway/
│   └── service-A/
└── docker-compose-dev.yml
└── .env


## Getting Started

### Prerequisites

- Docker Engine
- Docker Compose v2 (`docker compose`)



## Development Stack

For a richer development environment with Prometheus, Jaeger, and additional observability, use:

```bash
docker compose -f docker-compose-dev.yml up --build
```

## Environment Variables

The dev compose file uses environment variables from `.env`:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `KEYCLOAK_ADMIN_USERNAME`
- `KEYCLOAK_ADMIN_PASSWORD`

Create a `.env` file in the project root if needed. Example:

```env
POSTGRES_USER=keycloak
POSTGRES_PASSWORD=kc_password
KEYCLOAK_ADMIN_USERNAME=admin
KEYCLOAK_ADMIN_PASSWORD=admin
```

## Service Ports

- `8080`: Keycloak UI
- `5050`: pgAdmin
- `8025`: MailHog web UI
- `1025`: MailHog SMTP
- `8000`: auth-middleware service
- `4317`: OTLP gRPC receiver
- `4318`: OTLP HTTP receiver
- `8089`: Traefik web entrypoint (default compose)
- `8087`: Traefik metrics endpoint (default compose)

## Auth Middleware

The middleware in `services/api-gateway` verifies JWT bearer tokens using Keycloak's public key.
It exposes:

- `GET /`: health/info endpoint
- `GET /secure-endpoint`: example protected endpoint
- `GET /verify`: Traefik forward authentication endpoint

Traefik forwards authentication requests to `http://auth-middleware:8000/verify` using the `auth-mw` middleware defined in `services/api-gateway/dynamic.yml`.

## Traefik Configuration

Traefik is configured by `services/api-gateway/traefik.yml` and `services/api-gateway/dynamic.yml`.
The router labels in `docker-compose-dev.yml` route `keycloak` under `/keycloak` and `auth` under `/auth`.

## OpenTelemetry

The collector config file is mounted from `docker/otel/collector-config.yaml`.
Traefik is configured to send OTLP traces to the collector.

## Notes

- The project uses a docker socket proxy so Traefik can discover containers without direct access to the host Docker socket.
- If you need to update the collector configuration, edit `docker/otel/collector-config.yaml` and restart the collector.

## Troubleshooting

- If the collector fails to start, verify `docker/otel/collector-config.yaml` is a valid YAML file and that the compose mount points to a file, not a directory.
- If Traefik is not routing correctly, confirm the `PathPrefix` labels and the correct entrypoints in `services/api-gateway/traefik.yml`.
