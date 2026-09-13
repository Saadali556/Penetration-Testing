# Security Policy

## Project Scope

SecureShop is an intentionally vulnerable web application created for
authorized security training and application-security research.

The application is designed to run locally.

Default development target:

    http://127.0.0.1:5000

## Responsible Testing

Only test this application when you have authorization to do so.

Do not use the techniques demonstrated in this repository against systems
you do not own or have explicit permission to assess.

## Vulnerabilities Demonstrated

The project intentionally demonstrates:

- Broken Object Level Authorization (BOLA/IDOR)
- SQL Injection
- Reflected Cross-Site Scripting (XSS)

The vulnerabilities are documented together with their remediation and
retest results.

## Reporting

For security issues in the project itself, please open a GitHub issue
with enough information to reproduce the problem without exposing
sensitive information.
