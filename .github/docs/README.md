# Auth Gateway CI/CD Configuration Documentation

This directory documents the reusable GitHub Actions workflows in
`Ahmadzadeh920/auth-gateway-platform` and the configuration required to reuse
them from another repository.

## Source

Repository:
`https://github.com/Ahmadzadeh920/auth-gateway-platform`

Workflow directory:
`.github/workflows`

The inventory is based on the public workflow definitions currently available
from the repository. Secret **values are intentionally not included**.

## Recommended documentation model

Keep three things separate:

1. **Workflow contract** — inputs, outputs, permissions and required secrets.
2. **Configuration inventory** — names and purpose of repository/environment
   variables and secrets.
3. **Secret storage** — actual secret values remain in GitHub Secrets or an
   external secret manager.

Never commit actual secret values, kubeconfigs, private keys, webhook URLs,
tokens or passwords to this documentation.

## Reusable workflow family

The repository currently contains these reusable workflows:

- `reusable-test.yml`
- `reusable-codeql.yml`
- `reusable-sonarqube.yml`
- `reusable-docker-build.yml`
- `reusable-docker-push.yml`
- `reusable-trivy.yml`
- `reusable-notification.yml`
- `reusable-deploy.yml`
- `reusable-deploy-docker-compose.yml`
- `reusable-deploy-kubernetes.yml`
- `reusable-deploy-helm.yml`
- `reusable-sync.yml`
- `reusable-docker.yml`

The primary CI/CD configuration inventory focuses on workflows normally
composed by `ci.yml`: test, CodeQL, SonarQube, Docker build/push, Trivy,
notification and deployment. The deployment-specific workflows are also
documented because they define additional contracts available to callers.

## Important portability rule

A future application repository should normally provide:

- application-specific `workflow_call` inputs
- only the secrets explicitly required by the selected reusable workflow
- repository/environment variables for non-sensitive configuration
- appropriate GitHub Actions permissions
- self-hosted runner labels when deployment requires the local k3s runner

Do not copy secret values from one repository to another. Recreate or migrate
the credentials securely.

## Versioning recommendation

Do not consume the reusable workflows from `main` forever. Create release
tags such as:

- `v1`
- `v1.1.0`
- `v1.2.0`

and have application repositories call a stable tag. This makes the workflow
library a reusable CI/CD platform instead of a moving target.
