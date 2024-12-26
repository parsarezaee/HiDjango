import pytest
from unittest.mock import patch, mock_open
from hidjango.main import create_django_project, configure_database, create_devops_files, create_env_from_settings, detect_existing_database, configure_existing_project

@patch("subprocess.run")
def test_create_django_project(mock_subprocess_run):
    project_name = "testproject"
    
    create_django_project(project_name, devops=False)

    mock_subprocess_run.assert_called_once_with(
        ['django-admin', 'startproject', project_name], 
        check=True
    )


@patch("builtins.open", new_callable=mock_open, read_data="SECRET_KEY = 'test-secret-key'")
@patch("os.path.join", side_effect=lambda *args: "/".join(args))
def test_create_env_from_settings(mock_path_join, mock_file):
    project_name = "testproject"
    expected_env_content = "SECRET_KEY='test-secret-key'\n"

    # Act
    create_env_from_settings(project_name)

    # Assert
    # Check that .env file was opened in write mode
    mock_file.assert_any_call("testproject/.env", "w")
    
    # Verify content written to .env
    written_content = [call[0][0] for call in mock_file().write.call_args_list]
    assert expected_env_content in written_content



@patch("builtins.open")
@patch("os.path.isfile")
@patch("os.path.isdir")
def test_configure_database(mock_isdir, mock_isfile, mock_open):
    project_name = "testproject"
    db = "mysql"

    mock_isdir.return_value = True
    mock_isfile.return_value = True

    configure_database(project_name, db)

    mock_open.assert_called()


@patch("builtins.open", new_callable=mock_open)
def test_create_devops_files(mock_open):
    project_name = "testproject"
    db = "postgresql"

    create_devops_files(project_name, db=db)

    assert mock_open.call_count == 2
    mock_open.assert_any_call(f"{project_name}/Dockerfile", "w")
    mock_open.assert_any_call(f"{project_name}/docker-compose.yml", "w")

    # Retrieve the content written to docker-compose.yml
    written_content = [call[0][0] for call in mock_open().write.call_args_list]
    docker_compose_content = "".join(written_content)

    # Verify the database configuration for PostgreSQL in docker-compose.yml
    assert "image: postgres" in docker_compose_content, "PostgreSQL image not found in docker-compose.yml"
    assert "POSTGRES_USER" in docker_compose_content, "PostgreSQL user variable not found"
    assert "POSTGRES_PASSWORD" in docker_compose_content, "PostgreSQL password variable not found"
    assert "POSTGRES_DB" in docker_compose_content, "PostgreSQL database variable not found"