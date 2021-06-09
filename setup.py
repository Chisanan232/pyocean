import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyocean",
    version="0.1.0",
    author="Liu, Bryant",
    author_email="chi10211201@cycu.org.tw",
    description="A Python framework integrate multi-work simultaneously with different strategy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: APACHE License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "gevent==1.4.0",
        "colorama==0.4.1",
        "kafka-python==2.0.2",
        "deprecated==1.2.11"
    ]
)
