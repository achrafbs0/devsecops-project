FROM python:3.9-slim

# Vulnérabilités intentionnelles pour la démo
USER root
WORKDIR /app

# Copier les fichiers de l'application
COPY app/ .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port
EXPOSE 5000

# Démarrer l'application
CMD ["python", "app.py"]
