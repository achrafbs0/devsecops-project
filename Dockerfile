# Utilise une image Python officielle
FROM python:3.9-slim

# Crée un dossier pour l’app
WORKDIR /app

# Copie les fichiers requirements
COPY app/requirements.txt .

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le code de l’app dans le conteneur
COPY ./app /app

# Définit la variable d’environnement Flask
ENV FLASK_APP=app.py

# Expose le port 5000
EXPOSE 5000

# Commande pour démarrer Flask
CMD ["flask", "run", "--host=0.0.0.0"]
