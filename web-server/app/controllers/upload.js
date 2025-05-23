const path = require('path');
const fs = require('fs');
const s3 = require('../services/minioClient');
const uploadSF = require('../models/bucket');

module.exports = async function uploadImage(req, res) {
  if (!req.file) return res.status(400).json({ error: "Aucune image reçue" });

  try {
  
    await uploadSF.uploadSingleFile(req, res);

  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Échec de l'upload" });
  }
};
