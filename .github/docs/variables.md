# GitHub Actions Variables Inventory

This document records non-sensitive configuration needed by the reusable
workflows.

## Recommended variables

| Variable | Current source/usage | Purpose | Recommended scope |
|---|---|---|---|
| `SONAR_HOST_URL` | Currently passed as `secrets.sonar-host-url` | SonarQube URL | Repository or environment |
| `REGISTRY` | Workflow input defaults to `ghcr.io` | Container registry | Repository/org variable if shared |
| `REGISTRY_USERNAME` | Workflow input | Registry owner/user | Repository/org variable |
| `K8S_NAMESPACE` | Deployment input | Kubernetes namespace | Environment |
| `K8S_RUNNER` | Deployment input/default `k3s` | Self-hosted runner label | Repository/environment |
| `DEPLOYMENT_ENVIRONMENT` | Deployment input | GitHub environment name | Environment |
| `REMOTE_DIRECTORY` | Docker Compose deployment input | Remote deployment directory | Environment |
| `COMPOSE_FILE` | Docker Compose deployment input | Compose file | Repository/environment |
| `HELM_RELEASE` | Deployment input | Helm release name | Environment |
| `HELM_CHART` | Deployment input | Helm chart path | Repository |
| `IMAGE_NAME` | Docker workflow input | Container image name | Repository |
| `IMAGE_TAG` | Docker workflow input | Image tag | Workflow input |
| `SONAR_PROJECT_BASE_DIR` | Sonar workflow input | Sonar analysis directory | Repository |
| `NOTIFICATION_CHANNEL` | Notification workflow input | slack/teams/discord | Environment |

## Current workflow inputs are preferred over global variables

Most of the reusable workflows already expose explicit `workflow_call.inputs`.
That is preferable to putting everything into `vars`.

Use variables for stable infrastructure configuration and inputs for values that
are specific to a particular workflow invocation.

## Example configuration separation

Sensitive:

```text
secrets.SONAR_TOKEN
secrets.SSH_PRIVATE_KEY
secrets.KUBECONFIG
```

Non-sensitive:

```text
vars.SONAR_HOST_URL
vars.REGISTRY
vars.REGISTRY_USERNAME
vars.K8S_NAMESPACE
vars.REMOTE_DIRECTORY
```

Workflow-specific:

```text
with:
  image-name: api-gateway
  image-tag: ${{ github.sha }}
  working-directory: services/api
```
