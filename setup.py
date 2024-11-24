from setuptools import setup, find_packages

setup(
    name='hidjango',
    version='1.0.0',
    description='A library to simplify Django project initialization',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author='Parsa Rezaei',
    author_email='rezaei.7parsa@gmail.com',
    url='https://github.com/parsarezaee/HiDjango',
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        'pytest>=7.0.0',
        'django>=3.2',
        'textwrap3>=0.9.2',
    ],
    entry_points={
        'console_scripts': [
            'hidjango=hidjango.main:main',
        ],
    },
    license="MIT",
    keywords="django library project automation devops",
    include_package_data=True,
    zip_safe=False,
)