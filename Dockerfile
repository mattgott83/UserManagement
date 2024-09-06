FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt ./

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application dans le conteneur
COPY . .

# Exposer le port que l'application va utiliser (par exemple, 5000 pour Flask)
EXPOSE 5000

# Commande pour démarrer l'application
# Adapter cette commande selon la façon dont votre application démarre
CMD ["python", "main.py"]
