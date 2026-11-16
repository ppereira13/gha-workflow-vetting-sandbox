# The pull_request_target trigger and "pwn requests"

Related zizmor rule: dangerous-triggers

The `pull_request` trigger runs workflows from forks in a restricted context: the token
is read-only and repository secrets are not available. That makes it safe to build and
test code from strangers.

The `pull_request_target` trigger is different. It runs in the context of the base
repository, so the job receives repository secrets and a token that may have write
access, even when the pull request comes from a fork. It exists for tasks that need
those privileges but do not run the contributor's code, such as labelling or commenting.

The dangerous combination, often called a "pwn request", has three parts:

1. the workflow is triggered by `pull_request_target`;
2. it checks out the pull request's code, for example with
   `ref: ${{ github.event.pull_request.head.sha }}`;
3. it then executes something from that checkout, such as a build script, a test suite
   or `./deploy.sh`.

In that case code written by an untrusted contributor runs with the repository's secrets
and token. The attacker can read the secrets, push commits or tamper with releases.

## Fix

- Use `pull_request` instead of `pull_request_target` whenever the job has to build or
  run the contributor's code.
- If `pull_request_target` is really needed, do not check out or execute code from the
  pull request in that job.
- Keep steps that use secrets, such as deployment, in a separate workflow that only runs
  on trusted events like a push to the main branch.

Sources: GitHub Docs, "Events that trigger workflows" (pull_request_target); GitHub
Security Lab, "Keeping your GitHub Actions and workflows secure: Preventing pwn
requests".
