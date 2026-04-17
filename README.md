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
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" },
    { _id: 2, host: "mongo3:27017" }
  ]
})
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

