

## Running

```bash

docker-compose up -d

pip3 install redis

python3 ./project.py

```


## Query example

```js
// Ajout d'un opérateur Mr Orange Free
hmset operator:1 identifiant 1 nom "Orange"  prenom "Free"

// Ajout d'un appel a traiter
hmset appel:1 identifiant 1 heure_appel 10:00:00 numero_origine 0123456789 status "NOT_TAKEN" duree 0 operateur 0  text_descriptif "je suis un exemple"

// Attribuer un appel a un opérateur
hmset appel:1 identifiant 1 heure_appel 10:00:00 numero_origine 0123456789 status "RUNNING" duree 0 operateur 1  text_descriptif "je suis un exemple"

// finir un appel 
hmset appel:1 identifiant 1 heure_appel 10:00:00 numero_origine 0123456789 status "END" duree 120 operateur 1  text_descriptif "je suis un exemple"


```