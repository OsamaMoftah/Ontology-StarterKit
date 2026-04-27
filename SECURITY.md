# Security Policy

## Reporting a Vulnerability

Please do not open public issues for suspected security vulnerabilities.

Instead, report the issue privately to the maintainers with:

- A description of the vulnerability
- Impact and affected files
- Reproduction steps or proof of concept
- Suggested remediation, if known

## Secure-by-Default Expectations

For this repository, secure defaults include:

- No committed secrets or `.env` files
- No hard-coded production credentials
- Read-only graph access for LLM-generated queries whenever possible
- Clear setup instructions for local development versus production

## Scope Notes

This repository contains examples and templates. Teams deploying this repository in production are responsible for enforcing their own authentication, authorization, secret management, and infrastructure controls.
