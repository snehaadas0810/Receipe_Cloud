from setuptools import setup, find_packages

setup(
    name="django-auth-register-imran",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.2",
    ],
    author="Sneha",
    description="Reusable Django registration system",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
    ],
)