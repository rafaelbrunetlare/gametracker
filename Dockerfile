# Image de base python:3.11-slim
FROM python:3.11-slim

# Installation du client MySQL et des outils système 
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier et installer les dépendances Python
COPY requirements.txt .
# On met à jour pip et on installe les dépendances
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le code source et les scripts
COPY . .

# Rendre les scripts exécutables
RUN chmod +x scripts/*.sh

# Commande par défaut
CMD ["bash"]