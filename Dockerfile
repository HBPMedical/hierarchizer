FROM hbpmip/python-base:0.2.0

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

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="hbpmip/hierarchizer" \
      org.label-schema.description="Reorganize DICOM files to MIP specs" \
      org.label-schema.url="https://github.com/LREN-CHUV/hierarchizer" \
      org.label-schema.vcs-type="git" \
      org.label-schema.vcs-url="https://github.com/LREN-CHUV/hierarchizer" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version="$VERSION" \
      org.label-schema.vendor="LREN CHUV" \
      org.label-schema.license="Apache2.0" \
      org.label-schema.docker.dockerfile="Dockerfile" \
      org.label-schema.schema-version="1.0"
