# Reusable Workflow Contracts

## `reusable-test.yml`

Purpose: Python installation, linting, testing, coverage and artifact upload.

### Inputs

```text
runner
python-versions
working-directory
requirements-file
dependency-manager
install-command
lint
lint-command
run-tests
test-command
upload-artifacts
artifact-name
test-report-path
coverage-report-path
fail-fast
timeout-minutes
```

### Secrets

None.

### Permissions

```text
contents: read
```

### Outputs

```text
artifact-name
coverage-report
```

---

## `reusable-codeql.yml`

Purpose: CodeQL analysis.

### Inputs

```text
runner
languages
build-mode
build-command
queries
category
timeout-minutes
```

### Secrets

None.

### Permissions

```text
actions: read
contents: read
security-events: write
```

---

## `reusable-sonarqube.yml`

Purpose: SonarQube analysis and quality gate.

### Inputs

```text
runner
project-base-dir
artifact-name
download-artifact
scanner-args
quality-gate
quality-gate-timeout
fetch-depth
timeout-minutes
```

### Secrets

```text
sonar-token
sonar-host-url
DEPLOY_KEY
```

### Permissions

```text
contents: read
actions: read
```

---

## `reusable-docker-build.yml`

Purpose: Build a Docker image and optionally push/save it as an artifact.

### Inputs

```text
runner
registry
registry-username
image-name
image-tag
context
dockerfile
platforms
push
load
save-artifact
artifact-name
cache
```

### Secret

```text
registry-password
```

### Permissions

```text
contents: read
packages: write
```

### Outputs

```text
image
digest
tags
```

---

## `reusable-docker-push.yml`

Purpose: Download a Docker image artifact, load it, authenticate to a registry,
tag it and push it.

### Inputs

```text
runner
registry
registry-username
image-name
image-tag
artifact-name
timeout-minutes
```

### Secret

```text
registry-password
```

### Permissions

```text
contents: read
packages: write
```

### Outputs

```text
image
digest
```

---

## `reusable-trivy.yml`

Purpose: filesystem, image, configuration or SBOM security scanning.

### Inputs

```text
runner
scan-type
scan-target
download-artifact
artifact-name
severity
scanners
ignore-unfixed
exit-code
format
upload-sarif
upload-artifact
report-artifact-name
timeout-minutes
```

### Secrets

None.

### Permissions

```text
contents: read
security-events: write
```

### Outputs

```text
report
format
```

---

## `reusable-notification.yml`

Purpose: Slack, Microsoft Teams or Discord notifications.

### Inputs

```text
runner
channel
status
title
message
environment
application
color
include-github-context
```

### Secrets

```text
slack-webhook
teams-webhook
discord-webhook
```

### Permissions

```text
contents: read
```

---

## `reusable-deploy.yml`

Purpose: generic deployment dispatcher supporting Docker Compose, Kubernetes
and Helm.

### Inputs

```text
runner
deployment-type
environment
image
image-tag
compose-file
compose-service
kubernetes-manifest
namespace
helm-release
helm-chart
timeout-minutes
```

### Secrets

```text
ssh-host
ssh-user
ssh-private-key
kubeconfig
```

### Permissions

```text
contents: read
```

---

## Deployment-specific workflows

The repository also contains:

```text
reusable-deploy-docker-compose.yml
reusable-deploy-kubernetes.yml
reusable-deploy-helm.yml
```

These provide more specialized deployment contracts and should be treated as
separate reusable APIs if future repositories call them directly.

`reusable-deploy-kubernetes.yml` requires:

```text
DEPLOY_KEY
```

and uses a default runner label of:

```text
k3s
```

`reusable-deploy-helm.yml` also uses a default `k3s` runner and requires its
Helm/application inputs.

---

## `reusable-sync.yml`

Purpose: synchronize a source branch into a target repository.

### Inputs

```text
runner
source-branch
target-branch
target-repository
sync-tags
force-push
fetch-depth
commit-message
timeout-minutes
```

### Secret

```text
target-token
```

### Permissions

```text
contents: read
```

The current implementation creates a target HTTPS remote using the token.
For a future design, consider GitHub App authentication or another
short-lived credential mechanism instead of a long-lived PAT.
