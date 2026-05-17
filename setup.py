from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="ichis_atlas_app",
    version="1.0.0",
    description="GF Atlas App — GREENFARMS Corporate Foundation App",
    author="GREENFARMS",
    author_email="flexfernandes@gmail.com",
    packages=find_packages(include=["ichis_atlas_app", "ichis_atlas_app.*"]),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
