
# build with
# docker build -t openmc_data_to_json .

FROM openmc/openmc:latest

COPY openmc_data_to_json openmc_data_to_json/
COPY tests tests/
COPY pyproject.toml pyproject.toml
COPY README.md README.md

RUN pip install .
