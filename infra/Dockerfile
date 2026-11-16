FROM python:3.12-slim

RUN pip install --no-cache-dir zizmor==1.32.0

# Do not run the tool as root inside the container.
USER nobody

ENTRYPOINT ["zizmor"]