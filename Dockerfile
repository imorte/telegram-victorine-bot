FROM python
WORKDIR /app
ADD . /app
RUN pip3 install -r requirements.txt
EXPOSE 8443

COPY entrypoint.sh /
CMD ["/bin/bash", "entrypoint.sh"]