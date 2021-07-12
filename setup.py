import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openmc_data_to_json",
    version="0.0.14",
    author="Jonathan Shimwell",
    description="A tool for selectively extracting cross sections from OpenMC h5 files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/openmc_data_storage/openmc_data_to_json",
    packages=setuptools.find_packages(),
    zip_safe=True,
    package_dir={"openmc_data_to_json": "openmc_data_to_json"},
    scripts=['openmc_data_to_json/openmc-data-to-json'],
    package_data={
        "openmc_data_to_json": [
            "requirements.txt",
            "README.md",
            "LICENSE",
        ],
        # "tests": [
        #     "Li.h5"
        # ]
    },
    install_requires=[
        "h5py"
    ],
    tests_require=["pytest-cov"],
)
