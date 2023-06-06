import redis
import time

operateurs = [
    {'identifiant': 1, 'nom': 'Doe', 'prenom': 'John'},
    {'identifiant': 2, 'nom': 'Smith', 'prenom': 'Jane'}
]


status = [
    'NOT_TAKEN',
    'RUNNING',
    'END'
]

r = redis.Redis()


def ajouter_operateurs():
    for operateur in operateurs:
        r.hset('operateur:' + str(operateur['identifiant']),  mapping=operateur)

def ajouter_appel(identifiant, heure_appel, numero_origine, statut, duree, operateur, texte_descriptif):
    appel = {
        'identifiant': identifiant,
        'heure_appel': heure_appel,
        'numero_origine': numero_origine,
        'statut': statut,
        'duree': duree,
        'operateur': operateur,
        'texte_descriptif': texte_descriptif
    }
    r.lpush('to_take_call_id', identifiant)
    r.hset('appel:' + str(identifiant),  mapping=appel)


def affecter_appel(identifiant_appel, identifiant_operateur):
    appel = r.hgetall('appel:' + str(identifiant_appel))
    appel['statut'] = status[1]
    appel['operateur'] = identifiant_operateur
    r.hset('appel:' + str(identifiant_appel),  mapping=appel)
    r.lrem('to_take_call_id',0, identifiant_appel)

def finir_appel(identifiant_appel,temps_appel):
    appel = r.hgetall('appel:' + str(identifiant_appel))
    appel['statut'] = status[2]
    appel['duree'] = temps_appel
    r.hset('appel:' + str(identifiant_appel), mapping=appel)

def chercher_appel_a_prendre():
    identifiant_appel = r.lpop('to_take_call_id')
    appel = r.hgetall('appel:' + str(identifiant_appel))
    appel['statut'] = status[1]
    r.hset('appel:' + str(identifiant_appel), mapping=appel)
    return appel
#Ajout des opérateurs
ajouter_operateurs()


# Ajout d'un nouvel appel
ajouter_appel(1, time.time(), '0123456789',status[0], 0, '', 'Appel de test')

# Récupération des appels non pris en compte
appels_non_pris_en_compte = r.keys('appel:*')
for appel_key in appels_non_pris_en_compte:
    appel = r.hgetall(appel_key)
    appel =  {key.decode(): value.decode() for key, value in appel.items()}
    if 'statut' in appel and appel['statut'] == status[0]:
        print(appel)

# Affectation d'un appel à un opérateur
affecter_appel(1, operateurs[0]['identifiant'])


# Récupération d'un appel et finir le traitement
finir_appel(1,120)



