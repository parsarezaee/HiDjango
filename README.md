# HiDjango

HiDjango is a Python library designed to simplify the initialization and setup of Django projects, enabling developers to create or configure Django projects with DevOps setups and database settings using simple commands.

## Features

- Initialize new Django projects with a single command.
- Configure existing Django projects with DevOps and database settings.
- Automatically add Docker and Docker Compose files for development.
- Generate an `.env` file with the `SECRET_KEY` extracted from Django settings.
- Configure databases (PostgreSQL or MySQL) with minimal effort.
- Easy-to-use CLI for managing Django projects.

## What's New in Version 1.1.0

- **Existing Project Configuration**: Added the ability to configure existing Django projects with DevOps and database settings.
- **`.env` File Generation**: Automatically generates an `.env` file for managing sensitive data like `SECRET_KEY`.

## Installation

To install HiDjango, use pip:

```bash
pip install hidjango
```

## Usage

### Creating a Django Project

To create a new Django project:

```bash
hidjango --init --name="project_name"
```

This command creates a new Django project with the specified name.

### Configuring an Existing Django Project

To configure an existing Django project (e.g., adding DevOps files or setting up a database):

```bash
hidjango --config /path/to/project
```

#### Add DevOps Configuration

```bash
hidjango --config /path/to/project --devops
```

This adds the following files to your existing project:
- `Dockerfile`
- `docker-compose.yml`

If the database configuration already exists in the `settings.py` file, it will be included in the `docker-compose.yml` automatically.

#### Add Database Configuration

```bash
hidjango --config /path/to/project --db=postgresql
```

This command:
1. Configures the database settings in the `settings.py` file.
2. If `--devops` is also included, adds the database configuration to the `docker-compose.yml`.

#### Full Configuration Example:

```bash
hidjango --config /path/to/project --devops --db=mysql
```

This performs:
1. Adding Docker and Docker Compose files.
2. Configuring MySQL as the database in both `settings.py` and `docker-compose.yml`.

### Adding DevOps Files to a New Project

To include Docker and Docker Compose files in a new project:

```bash
hidjango --init --name="project_name" --devops
```

This adds:
- `Dockerfile`
- `docker-compose.yml`

### Generating `.env` File

HiDjango automatically generates an `.env` file in the project directory with the `SECRET_KEY` from `settings.py`. This ensures secure management of sensitive data.

## Requirements

- Python 3.7 or higher
- Django 3.2 or higher

## Example Commands

### Full Setup for a New Project

```bash
hidjango --init --name="my_project" --devops --db=postgresql
```

### Full Configuration for an Existing Project

```bash
hidjango --config /path/to/project --devops --db=mysql
```

## Contributing

We welcome contributions! To contribute:

1. Fork the repository on GitHub.
2. Make your changes.
3. Open a pull request.

For issues or feature requests, please open an issue on [GitHub](https://github.com/YourUsername/hidjango/issues).

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Links

- [GitHub Repository](https://github.com/YourUsername/hidjango)
- [PyPI Package](https://pypi.org/project/hidjango/)

---

