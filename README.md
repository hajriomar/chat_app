<<<<<<< HEAD
# chat_app
Dans le cmd : docker compose up --build
Dans un autre cmd en parallele: docker exec -it mongo1 mongosh
Entrer ca dans le > ou test affiché sur le cmd :
 rs.initiate({
  _id: "rs0", // Utilise bien le nom du replSet de ton docker-compose
=======
# Chat App

## Lancer les conteneurs

```bash
docker compose up --build
```

---

## Vérifier les services

```bash
docker compose ps
```

---

## Vérifier MongoDB ReplicaSet

Se connecter au conteneur MongoDB :

```bash
docker exec -it mongo1 mongosh
```

Vérifier l’état du ReplicaSet :

```javascript
rs.status()
```

---

## Initialiser le ReplicaSet (si nécessaire)

```javascript
rs.initiate({
  _id: "rs0",
>>>>>>> 4ebb6baac4b83f504d58e7558792853a028495e0
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" },
    { _id: 2, host: "mongo3:27017" }
  ]
})
<<<<<<< HEAD
Pour verifier on trouve sur le cmd : ok:1 .
On saisie exit pour sortir.
=======
```

---

## Accéder à l’application

* Application : http://localhost:8000/
* Documentation API : http://localhost:8000/api/docs/

---

## Commandes utiles

Voir les logs :

```bash
docker compose logs
```

Arrêter les conteneurs :

```bash
docker compose down
```


>>>>>>> 4ebb6baac4b83f504d58e7558792853a028495e0
