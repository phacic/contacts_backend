FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# set working dir
RUN mkdir /code
WORKDIR /code

# copy requirement.txt first to hit the cache
ADD requirements.txt /code/

# upgrade pip wheel and setuptools then install requirements
RUN pip install --no-cache-dir --upgrade pip wheel setuptools &&  \
    pip install --no-cache-dir -r requirements.txt

ADD . /code/
