# Installation des dépendances système
FROM python:3.11-slim

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Définition du dossier de travail
WORKDIR /app

# Installation des bibliothèques Python
# On copie d'abord requirements.txt pour optimiser le cache Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie de tout le projet
COPY . .

# Donner les droits d'exécution aux scripts
RUN chmod +x scripts/*.sh || true

# Commande par défaut
CMD ["bash"]

RUN apt-get update && apt-get install -y dos2unix
RUN dos2unix /app/scripts/run_pipeline.sh
RUN chmod +x /app/scripts/run_pipeline.sh