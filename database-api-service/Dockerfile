FROM python:3.9-slim

WORKDIR /app

COPY . /app/

RUN python3 -m pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=/app/src/server.py

EXPOSE 5010

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5010"]
