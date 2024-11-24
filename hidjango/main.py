import os
import subprocess
import sys
import textwrap



def create_django_project(project_name, devops=False, db=None):
    try:
        subprocess.run(['django-admin', 'startproject', project_name], check=True)
        print(f"Project '{project_name}' has been successfully created!")
    
        if db:
            configure_database(project_name, db)
        
        if devops:
            create_devops_files(project_name, db)
    
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while creating the project: {e}")


def configure_database(project_name, db):
    """Set up database configuration in settings.py"""
    settings_path = os.path.join(project_name, project_name, "settings.py")

    db_configs = {
        "postgresql": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "db",
            "USER": "user",
            "PASSWORD": "password",
            "HOST": "localhost",
            "PORT": "5432",
        },
        "mysql": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "db",
            "USER": "user",
            "PASSWORD": "password",
            "HOST": "localhost",
            "PORT": "3306",
        },
    }

    if db not in db_configs:
        print(f"Invalid database option: {db}. Supported databases: postgresql, mysql ")
        return
    
    try:
        with open(settings_path, "r") as settings_file:
            settings_content = settings_file.readlines()

        with open(settings_path, "w") as settings_file:
            in_databases_section = False
            for line in settings_content:
                if line.strip().startswith("DATABASES"):
                    in_databases_section = True
                    settings_file.write("DATABASES = {\n")
                    settings_file.write("    'default': {\n")
                    for key, value in db_configs[db].items():
                        settings_file.write(f"        '{key}': '{value}',\n")
                    settings_file.write("    }\n")
                elif in_databases_section:
                    if line.strip().startswith("}"):
                        in_databases_section = False
                else:
                    settings_file.write(line)

        print(f"Database configuration for {db} has been updated in settings.py.")

    except Exception as e:
        print(f"An error occurred while configuring the database: {e}")


def create_devops_files(project_name, db=None):
    dockerfile_content =textwrap.dedent( f"""
    # Dockerfile
    FROM python:3.10-slim
    ENV PYTHONDONTWRITEBYTECODE 1
    ENV PYTHONUNBUFFERED 1
    WORKDIR /app
    COPY requirements.txt requirements.txt 
    RUN pip install --upgrade pip && pip install -r requirements.txt
    COPY . . 
    CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
    """)

    docker_compose_content = textwrap.dedent(f"""
    version: '3'
    services:
      web:
        build: .
        ports:
          - "8000:8000"
        volumes:
          - .:/app
        command: python manage.py runserver 0.0.0.0:8000
    """)

    if db == "postgresql":
        docker_compose_content += textwrap.dedent("""
          db:
            image: postgres
            environment:
              POSTGRES_USER: user
              POSTGRES_PASSWORD: password
              POSTGRES_DB: db
            ports:
              - "5432:5432"
        """)
    elif db == "mysql":
        docker_compose_content += textwrap.dedent("""
          db:
            image: mysql
            environment:
              MYSQL_USER: user
              MYSQL_PASSWORD: password
              MYSQL_DATABASE: db
              MYSQL_ROOT_PASSWORD: root
            ports:
              - "3306:3306"
        """)

    try:
        with open(f"{project_name}/Dockerfile", "w") as dockerfile:
            dockerfile.write(dockerfile_content)
        print("Dockerfile has been created successfully!")

        with open(f"{project_name}/docker-compose.yml", "w") as docker_compose:
            docker_compose.write(docker_compose_content)
            print("docker-compose.yml has been created successfully!")
    
    except Exception as e:
        print(f"An error occurred while creating DevOps files: {e} ")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="hidjango CLI")
    parser.add_argument('--init', action='store_true', help='Create Django project')
    parser.add_argument('--name', type=str, required='--init' in sys.argv, help='Project name')
    parser.add_argument('--devops', action='store_true', help='Generate Docker and docker-compose files')
    parser.add_argument('--db', type=str, choices=['mysql', 'postgresql'], help='Database to configure')
    args = parser.parse_args()

    if args.init:
        if not args.name:
            print("Please set the project's name with using --name")
        else:
            create_django_project(args.name, devops=args.devops, db=args.db)

if __name__ == "__main__":
    main()