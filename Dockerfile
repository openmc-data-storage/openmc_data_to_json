
# build with
# docker build -t openmc_data_to_json .

FROM openmc/openmc:latest

COPY openmc_data_to_json openmc_data_to_json/
COPY tests tests/
COPY setup.py setup.py
COPY README.md README.md

# using setup.py instead of pip due to https://github.com/pypa/pip/issues/5816
RUN python setup.py install
