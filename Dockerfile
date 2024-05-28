FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install -r req.txt


EXPOSE 8000

# CMD or ENTRYPOINT
# Comment entrypoint, if you don't have migrations 

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]