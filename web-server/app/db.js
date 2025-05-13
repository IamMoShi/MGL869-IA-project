const path = require('path');
const { Sequelize } = require('sequelize');

module.exports = new Sequelize({
  dialect: 'sqlite',
  storage: path.join(__dirname, 'databases/mvc_demo.sqlite')
});
