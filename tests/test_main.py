import pytest
from unittest.mock import patch
from hidjango.main import create_django_project, configure_database, create_devops_files

@patch("subprocess.run")
def test_create_django_project(mock_subprocess_run):
    project_name = "testproject"
    
    create_django_project(project_name, devops=False)

    mock_subprocess_run.assert_called_once_with(
        ['django-admin', 'startproject', project_name], 
        check=True
    )

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

@patch("builtins.open")
def test_create_devops_files(mock_open):
    project_name = "testproject"
    db = "postgresql"

    create_devops_files(project_name, db=db)

    assert mock_open.call_count == 2
    mock_open.assert_any_call(f"{project_name}/Dockerfile", "w")
    mock_open.assert_any_call(f"{project_name}/docker-compose.yml", "w")
