#!/bin/bash

# Fonction pour activer le venv et lancer des commandes
activate_and_run() {
    echo "Activation de l'environnement virtuel..."
    source .venv/bin/activate
    vscodium .
    cd src/
    python manage.py runserver
}

# Vérification de l'état de l'environnement virtuel
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Aucun environnement virtuel n'est actif."
    activate_and_run
else
    echo "Un environnement virtuel est actif : $VIRTUAL_ENV"
    deactivate
    activate_and_run
fi
