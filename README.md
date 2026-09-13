# SecureShop — Web Application Penetration Testing Lab

> An intentionally vulnerable e-commerce application built to demonstrate
> a complete web application security testing and remediation lifecycle.

## Overview

SecureShop is a Python/Flask e-commerce application created as an
authorized local penetration-testing laboratory.

The project demonstrates how an application can be:

1. Built from a secure baseline
2. Intentionally configured with controlled vulnerabilities
3. Assessed using common security tools
4. Remediated
5. Retested
6. Hardened

All testing is performed against the local application.

## Architecture

```text
Browser
   |
   v
Flask Web Application
   |
   +---- Authentication
   +---- Product Catalog
   +---- Search
   +---- Shopping Cart
   +---- Orders
   +---- REST API
   +---- Admin Panel
   |
   v
SQLite Database
## Project Screenshots

### Application Overview

![Application Overview](docs/screenshots/Screenshot_2026-09-13_12_23_38.png)

### Security Testing

![Security Testing](docs/screenshots/Screenshot_2026-09-13_12_25_31.png)

### SQL Injection Testing

![SQL Injection Testing](docs/screenshots/Screenshot_2026-09-13_12_26_24.png)

### Reflected XSS Testing

![Reflected XSS Testing](docs/screenshots/Screenshot_2026-09-13_12_26_36.png)

### Security Retesting

![Security Retesting](docs/screenshots/Screenshot_2026-09-13_12_26_47.png)
