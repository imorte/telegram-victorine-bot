FROM python
WORKDIR /app
ADD . /app
RUN pip3 install -r requirements.txt
EXPOSE 8443
CMD ["python", "main.py"]
CMD ["python", "scheduler.py"]