FROM continuumio/miniconda3

WORKDIR /app

# Create the environment
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN comands use the new environment
SHELL ["conda", "run", "-n", "dct", "/bin/bash", "-c"]

# The code to run when container is started
COPY dash_app/app.py ./dash_app/
COPY dash_app/app_lib.py ./dash_app/
EXPOSE 8050
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "dct", "python", "./dash_app/app.py"]