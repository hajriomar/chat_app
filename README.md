# chat_app

1. Lancer les conteneurs :
   docker compose up --build

2. Vérifier les services :
   docker compose ps

3. Vérifier MongoDB ReplicaSet :
   docker exec -it mongo1 mongosh
   rs.status()

4. Si nécessaire, initialiser le ReplicaSet :
   rs.initiate({
     _id: "rs0",
     members: [
       { _id: 0, host: "mongo1:27017" },
       { _id: 1, host: "mongo2:27017" },
       { _id: 2, host: "mongo3:27017" }
     ]
   })

5. Ouvrir l’application :
   http://localhost:8000/
   http://localhost:8000/api/docs/
