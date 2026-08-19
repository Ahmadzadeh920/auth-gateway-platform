# GitHub Actions Secrets Inventory

This file records **secret names and their purpose only**. It intentionally
does not contain secret values.

## Required/known secrets

| Secret | Workflow | Required | Purpose | Recommended scope | OIDC replacement |
|---|---|---:|---|---|---|
| `sonar-token` | `reusable-sonarqube.yml` | Yes | SonarQube authentication token | Environment or repository | No |
| `sonar-host-url` | `reusable-sonarqube.yml` | Yes | SonarQube server URL | Repository/environment; preferably variable if non-sensitive | No |
| `DEPLOY_KEY` | `reusable-sonarqube.yml` | Yes in current workflow | SSH key supplied to checkout | Repository/environment | No |
| `registry-password` | `reusable-docker-build.yml` | Yes | Container registry password/token | Repository/environment | Sometimes |
| `registry-password` | `reusable-docker-push.yml` | Yes | Container registry password/token | Repository/environment | Sometimes |
| `ssh-host` | `reusable-deploy.yml` | Optional | Remote Docker Compose host | Variable preferred; secret only if policy requires | No |
| `ssh-user` | `reusable-deploy.yml` | Optional | Remote SSH username | Variable preferred | No |
| `ssh-private-key` | `reusable-deploy.yml` | Optional | SSH private key for remote Docker Compose deployment | Environment | No |
| `kubeconfig` | `reusable-deploy.yml` | Optional | Kubernetes authentication for deploy/Helm | Environment | Potentially |
| `slack-webhook` | `reusable-notification.yml` | Optional | Slack notification webhook | Environment/repository | No |
| `teams-webhook` | `reusable-notification.yml` | Optional | Microsoft Teams webhook | Environment/repository | No |
| `discord-webhook` | `reusable-notification.yml` | Optional | Discord notification webhook | Environment/repository | No |
| `target-token` | `reusable-sync.yml` | Yes | Token used to push to target repository | Environment/repository | Prefer GitHub App/OIDC-style short-lived auth where practical |
| `DEPLOY_KEY` | `reusable-deploy-kubernetes.yml` | Yes | SSH key passed to `actions/checkout` | Repository/environment | No |

## Important observations

### 1. `sonar-host-url` should normally be a variable

The current reusable workflow defines it as a secret. The URL itself is normally
not secret. A future revision should consider:

```text
vars.SONAR_HOST_URL
```

while keeping:

```text
secrets.SONAR_TOKEN
```

as the credential.

### 2. GHCR

For GitHub Container Registry, prefer the automatically provided
`GITHUB_TOKEN` where possible instead of creating a long-lived personal access
token. The current reusable Docker workflows require a generic
`registry-password`, so the reusable workflow can later be improved to support
`GITHUB_TOKEN` directly for GHCR.

### 3. Kubeconfig

The current k3s deployment architecture uses a kubeconfig/private credential.
For the current on-premises k3s setup, keep this as an environment secret unless
you redesign Kubernetes authentication.

For cloud Kubernetes, investigate short-lived OIDC-based authentication.

### 4. SSH

OIDC does not directly replace a normal SSH private key used to access a
self-hosted Ubuntu server. Keep the SSH key in an environment/repository secret
unless the deployment architecture changes.

## Secret naming recommendation

For a future version of the workflow library, prefer consistent uppercase
names when the secret is infrastructure-specific:

```text
SONAR_TOKEN
REGISTRY_PASSWORD
SSH_PRIVATE_KEY
KUBECONFIG
DISCORD_WEBHOOK
SLACK_WEBHOOK
TEAMS_WEBHOOK
TARGET_REPOSITORY_TOKEN
```

However, changing names in a reusable workflow is a breaking contract unless
backward compatibility is maintained.

## What must never be stored here

Do not put any of the following in this repository:

- actual token values
- private keys
- kubeconfig contents
- passwords
- webhook URLs containing credentials
- PATs
- cloud access keys
