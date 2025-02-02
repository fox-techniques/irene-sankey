# 📥 Installation 

## 📦 pip 

IRENE-Sankey is published as a python package and can be installed with
`pip`, ideally by using a [virtual environment]. Open up a terminal and install with:

=== "Latest"

    ``` sh
    pip install irene-sankey
    ```

=== "1.x"

    ``` sh
    pip install irene-sankey=="1.*" # (1)!
    ```

    1.  IRENE-Sankey uses [semantic versioning].

        This will make sure that you don't accidentally [upgrade to the next
        major version], which may include breaking changes that silently corrupt
        your site. Additionally, you can use `pip freeze` to create a lockfile,
        so builds are reproducible at all times:

        ```
        pip freeze > requirements.txt
        ```

        Now, the lockfile can be used for installation:

        ```
        pip install -r requirements.txt
        ```

This will automatically install compatible versions of all dependencies:
[numpy], [pandas], [plotly], and [requests]. IRENE-Sankey always strives to support the latest versions, so there's no need to
install those packages separately.

---

!!! tip

    If you don't have prior experience with Python, we recommend reading
    [Using Python's pip to Manage Your Projects' Dependencies], which is a
    really good introduction on the mechanics of Python package management and
    helps you troubleshoot if you run into errors.

  [Python package]: https://pypi.org/project/irene-sankey/
  [virtual environment]: https://realpython.com/what-is-pip/#using-pip-in-a-python-virtual-environment
  [semantic versioning]: https://semver.org/
  [Using Python's pip to Manage Your Projects' Dependencies]: https://realpython.com/what-is-pip/


## 🐙 Git

**IRENE-Sankey** can be directly used from [GitHub] by cloning the
repository into a subfolder of your project root which might be useful if you
want to use the very latest version:

```
git clone https://github.com/fox-techniques/irene-sankey.git
```

Next, install the theme and its dependencies with:

```
pip install -e irene-sankey
```

## 🎭 Poetry

Prerequisites:

- Python 3.8 or higher
- [Poetry]

Installing IRENE-Sankey:

```bash
poetry add irene-sankey
```

This command downloads and installs the package and its dependencies and adds the package as a dependency in your `pyproject.toml`.

Using the Package:

After installation, you can start using the package in your project. If you need to enter the virtual environment managed by Poetry, run:

```bash
poetry shell
```

Verify the Installation:

```bash
poetry show irene-sankey
```

Updating the Package:

```bash
poetry update irene-sankey
```

  [IRENE-Sankey]: https://pypi.org/project/irene-sankey/
  [GitHub]: https://github.com/fox-techniques/irene-sankey
  [numpy]: https://pypi.org/project/numpy/
  [pandas]: https://pypi.org/project/pandas/
  [plotly]: https://pypi.org/project/plotly/
  [requests]: https://pypi.org/project/requests/
  [Poetry]: https://python-poetry.org/docs/#installation