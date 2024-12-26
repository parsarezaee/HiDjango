import os
import subprocess
import sys
import textwrap
import re



def create_django_project(project_name, devops=False, db=None):
    try:
        # Create Django Project
        subprocess.run(['django-admin', 'startproject', project_name], check=True)
        print(f"Project '{project_name}' has been successfully created!")
        # Create .env file
        create_env_from_settings(project_name)

        # Create database
        if db:
            configure_database(project_name, db)
        
        # Create docker files
        if devops:
            create_devops_files(project_name, db)
    
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while creating the project: {e}")


def create_env_from_settings(project_name):
    """
    Extract SECRET_KEY from settings.py and save it to .env file.
    """
    settings_path = os.path.join(project_name, project_name, "settings.py")
    env_path = os.path.join(project_name, ".env")

    try:
        # Read settings.py to find SECRET_KEY
        with open(settings_path, "r") as settings_file:
            settings_content = settings_file.read()
            secret_key_match = re.search(r"SECRET_KEY\s*=\s*['\"](.*?)['\"]", settings_content)
            if not secret_key_match:
                print("SECRET_KEY not found in settings.py")
                return
            secret_key = secret_key_match.group(1)

        # Write SECRET_KEY into the .env file
        env_content = f"SECRET_KEY='{secret_key}'\n"
        with open(env_path, "w") as env_file:
            env_file.write(env_content)
        print(".env file has been successfully created with SECRET_KEY!")

        # Replace SECRET_KEY in settings.py to use the .env file
        updated_settings_content = re.sub(
            r"SECRET_KEY\s*=\s*['\"].*?['\"]",
            "from dotenv import load_dotenv\n"
            "import os\n"
            "load_dotenv()\n"
            "SECRET_KEY = os.getenv('SECRET_KEY')",
            settings_content,
        )
        with open(settings_path, "w") as settings_file:
            settings_file.write(updated_settings_content)
        print("settings.py has been updated to use SECRET_KEY from .env!")

    except Exception as e:
        print(f"An error occurred: {e}")


def detect_existing_database(path):
    """
    Detect the database engine used in the settings.py file of the Django project.
    """
    settings_path = os.path.join(path, os.path.basename(path), "settings.py")
    try:
        with open(settings_path, "r") as settings_file:
            settings_content = settings_file.read()

        # Search for database engine
        if 'django.db.backends.postgresql' in settings_content:
            return "postgresql"
        elif 'django.db.backends.mysql' in settings_content:
            return "mysql"
        else:
            return None
    except Exception as e:
        print(f"An error occurred while reading settings.py: {e}")
        return None


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
    
    if not db:
        db = detect_existing_database(project_name)

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


def is_valid_django_project(path):
    """
    Check if the provided path is a valid Django project.
    """
    if not os.path.isdir(path):
        return False
    
    # Check for manage.py in the root 
    manage_py = os.path.join(path, "manage.py")
    if not os.path.isfile(manage_py):
        return False
    
    # Check for settings.py in the project folder
    project_name = os.path.basename(path)
    settings_py = os.path.join(path, project_name, "settings.py")
    if not os.path.isfile(settings_py):
        return False
    
    return True


def configure_existing_project(path, db=None, devops=False):
    """
    configure an existing Django project with the specified options.
    """
    if not is_valid_django_project(path):
        print(f"The provided path '{path}' is not a valid Django project. ")
        return
    
    print(f"Configuring Django project at: {path}")

    if db:
        configure_database(path, db)
    
    if devops:
        create_devops_files(path)
    
    print("Configuration complete!")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="hidjango CLI")
    parser.add_argument('--init', action='store_true', help='Create Django project')
    parser.add_argument('--name', type=str, required='--init' in sys.argv, help='Project name')
    parser.add_argument('--config', type=str, help='Path to an existing Django project to configure')
    parser.add_argument('--db', type=str, choices=['mysql', 'postgresql'], help='Database to configure')
    parser.add_argument('--devops', action='store_true', help='Generate Docker and docker-compose files')
    args = parser.parse_args()

    if args.init:
        if not args.name:
            print("Please set the project's name with using --name")
        else:
            create_django_project(args.name, devops=args.devops, db=args.db)
    
    elif args.config:
        if not is_valid_django_project(args.config):
            print("The provided path is not a valid Django project. ")
        else:
            configure_existing_project(args.config, db=args.db, devops=args.devops)

    else:
        print("Please provide a valid command. Use --help for options. ")


if __name__ == "__main__":
    main()