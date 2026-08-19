# OIDC Strategy

## Conclusion

OIDC is useful for this workflow library, but it should be introduced
selectively.

OIDC is primarily useful for replacing long-lived cloud credentials with
short-lived identity tokens.

## Current credentials that OIDC does not directly replace

### SSH

The current Docker Compose deployment uses:

```text
ssh-private-key
ssh-user
ssh-host
```

OIDC does not directly authenticate a normal SSH connection to the existing
Ubuntu deployment host.

### SonarQube

The current workflow requires:

```text
sonar-token
```

SonarQube authentication is normally handled with its own token rather than
GitHub OIDC.

### Notification webhooks

Slack, Teams and Discord webhooks are application/service credentials.
GitHub OIDC is not a direct replacement.

## Credentials where OIDC can be valuable

### Cloud container registries

If a future deployment uses AWS, Azure or GCP, prefer GitHub OIDC and
short-lived credentials over storing cloud access keys.

### Cloud Kubernetes

For managed Kubernetes services, investigate provider-supported GitHub OIDC
authentication instead of storing long-lived cloud credentials.

## GitHub Actions permission

An OIDC-enabled job normally needs:

```yaml
permissions:
  id-token: write
  contents: read
```

Only grant `id-token: write` to jobs that actually need OIDC.

## Recommended future architecture

```text
GitHub Actions
      |
      | OIDC identity token
      v
Cloud identity provider
      |
      | short-lived credentials
      v
Cloud registry / cloud Kubernetes
```

For the current local/on-premises k3s + SSH architecture, keep the existing
credentials until the infrastructure is redesigned.

## Important reusable-workflow rule

If OIDC is added to a reusable workflow, explicitly document the required
permissions in that workflow and in the caller. Do not silently broaden
permissions for every consumer repository.
