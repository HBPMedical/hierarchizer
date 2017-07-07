FROM hbpmip/python-base:a2b201e

MAINTAINER mirco.nasuti@chuv.ch

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY hierarchizer/ /opt/hierarchizer/

VOLUME /input_folder
VOLUME /output_folder
VOLUME /meta_output_folder

WORKDIR /opt
ENV PYTHONPATH /opt/
ENTRYPOINT ["python", "/opt/hierarchizer/hierarchize.py", "/input_folder", "/output_folder", "/meta_output_folder"]
