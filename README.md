# chat_app
Dans le cmd : docker compose up --build
Dans un autre cmd en parallele: docker exec -it mongo1 mongosh
Entrer ca dans le > ou test affiché sur le cmd :
 rs.initiate({
  _id: "rs0", // Utilise bien le nom du replSet de ton docker-compose
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" },
    { _id: 2, host: "mongo3:27017" }
  ]
})
Pour verifier on trouve sur le cmd : ok:1 .
On saisie exit pour sortir.