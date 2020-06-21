import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rolltables",
    version="0.2.2",
    author="david.schenck@outlook.com",
    author_email="david.schenck@outlook.com",
    description="Commodity futures roll tables made easy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dschenck/rolltables",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pandas'],
    include_package_data=True
)
