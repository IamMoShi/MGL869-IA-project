// models/image.js
const { DataTypes, Model } = require('sequelize');
const sequelize = require('../db/postgres');

class Image extends Model {}

Image.init({
  id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
  filename: { type: DataTypes.STRING, allowNull: false },
  category: { type: DataTypes.INTEGER },
  attribution_method: { type: DataTypes.INTEGER },
  created_at: { type: DataTypes.DATE },
}, {
  sequelize,
  modelName: 'Image',
  tableName: 'images',         // assure-toi que ce nom est correct (pas "Images")
  timestamps: false,           // sinon Sequelize attend createdAt/updatedAt
});

module.exports = Image;
