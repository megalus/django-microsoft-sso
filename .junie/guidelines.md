Project runs on a virtualenv inside WSL. Python interpreter can be found using command `poetry env info`.

Test runner is `pytest`. To run can use command `make test`.

Always use the latest version of `django` and `msal`.

Always use type hints in the code. Always use TypeDicts for dictionaries.

Always use dataclasses for objects.

Always add docstrings in functions with more than seven lines of code. Use Google style.

Linter packages are managed by [pre-commit](https://github.com/pre-commit/pre-commit) library. Use `make lint` to check for linter and format errors.

Project python version is 3.11.10.

This is a public python library hosted in PyPI. All configuration is inside `pyproject.toml` file.

Use semantic versioning for commit messages. Use `fix:` if new code only changes or adds tests. Use `feat:` if the decorator is changed. Use `chore:` if the non-test code is changed but not the decorator. Use `docs:` if the documentation is changed. Use `refactor:` if the code is changed but not the decorator and not the tests.

Project versioning is done during GitHub actions `.github/publish.yml` workflow, using the [auto-changelog](https://github.com/KeNaCo/auto-changelog) library.

Always update the README at the root of the project.

README always contains [shields.io](https://shields.io/docs) badges for (when applicable): python versions, django versions, pypi version, license and build status.

Prefer use mermaid diagrams on docs.

Always use English on code and docs.

The README always contains the minimal configuration for the library to work.

Always write the README for developers with no or low experience with Django, Microsoft 365 and OAuth2, but be pragmatic and short. The README should be a quick start guide for developers to use the library.

The ./docs folder contains detailed instructions of how to use the library, including examples and diagrams. Reading order for the markdown files is located in mkdocs.yml at `nav` key. On these docs you can be very didactic.

The folder `example_microsoft_app` contains a minimal Django app using the library. It can be used as a reference for the documentation. Use their README.md as a reference for how to use.
