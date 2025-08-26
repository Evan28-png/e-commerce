FROM python:latest
WORKDIR /app

COPY . .
RUN pip install -r requirements.txt
RUN apt update && apt install netcat-openbsd -y && apt clean && apt autoremove | tail -4
EXPOSE 3000

RUN chmod +x wait_for_mysql.sh
RUN useradd app
USER app

CMD ["./wait_for_mysql.sh"]
