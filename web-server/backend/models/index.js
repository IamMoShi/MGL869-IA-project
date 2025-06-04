const sqlite = require('../db/sqlite');
const postgres = require('../db/postgres');

const User = require('./user');
const Image = require('./image');

(async () => {
  await sqlite.sync({ force: false });
  await postgres.sync({ force: false });
  console.log("Les deux bases sont synchronisées !");
})();

module.exports = { User, Image };