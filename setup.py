import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
#with open("requirements.txt", "r") as fh:
#    requirements = fh.read().splitlines()

setuptools.setup(
    name="FlyBIDS",
    version="0.0.2",
    author="Tinashe M. Tapera",
    author_email="tinashemtapera@gmail.com",
    description="Quickly collect and inspect BIDS data on Flywheel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PennLINC/FlyBIDS",
    packages=setuptools.find_packages(),
    install_requires=[
        "flywheel-sdk",
        "pandas",
        "tqdm"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
