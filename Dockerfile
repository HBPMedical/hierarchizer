FROM hbpmip/python-base:a2b201e

MAINTAINER mirco.nasuti@chuv.ch

COPY hierarchizer/ /hierarchizer/
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

VOLUME /input_folder
VOLUME /output_folder

WORKDIR /
ENTRYPOINT ["python", "/hierarchizer/hierarchize.py", "/input_folder", "/output_folder"]
