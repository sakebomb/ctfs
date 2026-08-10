FROM python:3.9-slim

WORKDIR /app

COPY main.py .
COPY flag.txt .

# Make flag readable but not writable
RUN chmod 444 flag.txt

EXPOSE 31337

CMD ["python", "main.py"] 