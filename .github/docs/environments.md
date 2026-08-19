# GitHub Actions Environments

Use GitHub Environments to separate deployment configuration from normal CI.

## Recommended environments

```text
development
staging
production
```

If only one deployment environment exists today, start with:

```text
production
```

## Recommended production environment secrets

```text
KUBECONFIG
SSH_PRIVATE_KEY
SONAR_TOKEN
DISCORD_WEBHOOK
SLACK_WEBHOOK
TEAMS_WEBHOOK
REGISTRY_PASSWORD
```

Only create the secrets actually required by the selected workflow.

## Recommended production variables

```text
SONAR_HOST_URL
REGISTRY
REGISTRY_USERNAME
K8S_NAMESPACE
REMOTE_DIRECTORY
HELM_RELEASE
HELM_CHART
```

## Environment protection

For production, consider:

- required reviewers
- deployment branch/tag restrictions
- environment-specific secrets
- environment-specific variables

This gives a reusable workflow a stable interface while keeping production
credentials isolated from development.

## Self-hosted runner

The current Kubernetes workflows default to a `k3s` runner label. This is an
infrastructure requirement, not a secret.

A future repository using Kubernetes deployment must either:

1. provide a runner with the expected label, or
2. override the runner input with the correct self-hosted runner label.

Do not place runner labels in secrets.
