// db/postgres.js
const { Sequelize } = require('sequelize');

const pgSequelize = new Sequelize('web-database', 'postgres', 'changeme', {
  host: 'localhost',
  port: 3630,
  dialect: 'postgres',
  logging: console.log,
});

pgSequelize.authenticate()
  .then(() => console.log("Connecté à PostgreSQL ✅"))
  .catch(err => console.error("Erreur PostgreSQL ❌", err));

module.exports = pgSequelize;
