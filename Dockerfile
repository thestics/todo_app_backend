FROM python:3.10
WORKDIR /app
COPY . /app
RUN chmod +x /app/scripts/install.sh
RUN /app/scripts/install.sh
RUN chmod +x /app/scripts/run.sh

CMD ["/app/scripts/run.sh"]
