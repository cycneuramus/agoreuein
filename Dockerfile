FROM python:alpine

ARG SCRIPT_DIR=/home/agoreuein/script
ARG USER=agoreuein
ARG UID=1000

RUN adduser \
	--disabled-password \
	--uid $UID \
	$USER

USER $USER

RUN mkdir -p $SCRIPT_DIR
ENV PYTHONPATH=$SCRIPT_DIR
ENV PATH=/home/agoreuein/.local/bin:${PATH}

RUN pip install requests telethon names
WORKDIR $SCRIPT_DIR
ENTRYPOINT ["python", "agoreuein.py"]
