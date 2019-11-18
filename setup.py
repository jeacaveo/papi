import setuptools

with open("README.rst", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="papi_jeacaveo",
    version="1.0.0",
    author="Jean Ventura",
    author_email="jv@venturasystems.net",
    description="REST API for Prismata related data.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst; charset=UTF-8",
    url="https://github.com/jeacaveo/papi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: "
        "GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        ],
    python_requires=">=3.6",
    install_requires=["django", "djangorestframework"],
    extras_require={
        "dev": ["pycodestyle", "pylint", "mypy"],
        "test": ["mock", "coverage"],
        },
    )
