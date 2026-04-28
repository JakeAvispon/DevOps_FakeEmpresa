FROM python:3.9-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Exponemos el puerto para la app Flask
EXPOSE 5000
CMD ["python", "app/pokeApp.py"]