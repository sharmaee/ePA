# pull official base image
FROM ubuntu:20.04 AS builder

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends python3.9 python3-pip python3.9-dev python3.9-distutils libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /home/backend

RUN pip install --upgrade pip
RUN pip install pipenv

# create venv
ADD ./backend/Pipfile ./backend/Pipfile.lock /home/backend/
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

ENV PATH="/home/backend/.venv/bin:$PATH" VIRTUAL_ENV="/home/backend/.venv/bin"

FROM ubuntu:20.04 AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends python3.9 python3.9-dev python3.9-distutils libpq-dev ca-certificates && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home backend

# Copy virtual env from python-deps stage
COPY --from=builder /home/backend/.venv /home/backend/.venv

RUN mkdir /home/backend/web
RUN mkdir /home/backend/web/static
RUN mkdir /home/backend/web/media

WORKDIR /home/backend/web

# copy project
COPY ./backend/ .

ENV PYTHONUNBUFFERED=1

# chown all the files to the backend user
RUN chown -R backend:backend /home/backend/web

USER backend

ENV PATH="/home/backend/.venv/bin:$PATH" VIRTUAL_ENV="/home/backend/.venv/bin"
