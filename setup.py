from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

def main():
    "Executes setup when this script is the top-level"
    import openmc_data_to_json as app

    setup(
        name="openmc_data_to_json",
        version=app.__version__,,
        author="Jonathan Shimwell",
        description="A tool for selectively extracting cross sections from OpenMC h5 files.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/openmc_data_storage/openmc_data_to_json",
        packages=find_packages(),
        zip_safe=True,
        package_dir=find_packages(),
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
