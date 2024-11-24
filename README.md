# HiDjango

HiDjango is a Python library designed to simplify the initialization and setup of Django projects, enabling developers to create Django projects with DevOps configurations using a single command.

## Features
- Initialize Django projects with a single command.
- Automatically add Docker and Docker Compose files for development.
- Configure databases (PostgreSQL or MySQL) with minimal effort.
- Easy-to-use CLI for managing Django projects.

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

### Adding DevOps Files
To include Docker and Docker Compose files:

```bash
hidjango --init --name="project_name" --devops
```

This adds the following files to your project:
- `Dockerfile`
- `docker-compose.yml`

### Configuring a Database
If a database is set, its configuration will be added to the `settings.py` file of the Django project automatically.

#### PostgreSQL Example:
```bash
hidjango --init --name="project_name" --db=postgresql
```

#### MySQL Example:
```bash
hidjango --init --name="project_name" --db=mysql
```

If the `--devops` flag is included, the database configuration will also be added to the `docker-compose.yml` file.

## Requirements
- Python 3.7 or higher
- Django 3.2 or higher

## Example Commands

### Full Setup with DevOps and Database
```bash
hidjango --init --name="my_project" --devops --db=postgresql
```

This command:
1. Creates a new Django project named `my_project`.
2. Adds `Dockerfile` and `docker-compose.yml`.
3. Configures the project to use PostgreSQL as its database.

## Contributing
We welcome contributions! To contribute:
1. Fork the repository on GitHub.
2. Make your changes.
3. Open a pull request.

For issues or feature requests, please open an issue on [GitHub](https://github.com/parsarezaee/HiDjango/issues).

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Links
- [GitHub Repository](https://github.com/parsarezaee/HiDjango)
- [PyPI Package](https://pypi.org/project/hidjango/)

---

