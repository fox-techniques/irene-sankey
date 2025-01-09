from setuptools import setup, find_packages

setup(
    name="irene-sankey",
    version="1.0.2",
    author="FOX Techniques",
    author_email="ali.nabbi@fox-techniques.com",
    description="A package for generating source-target pair and node map from pandas DataFrames for Sankey flow diagrams",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/fox-techniques/irene-sankey",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24,<2.0",
        "pandas>=2.0,<2.1",
        "requests>=2.32.3",
        "plotly>=5.24.1",
    ],
    extras_require={"dev": ["pytest>=8.3.3"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
