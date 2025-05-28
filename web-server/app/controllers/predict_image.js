const path = require('path');
const fs = require('fs');
const s3 = require('../services/minioClient');
const uploadSF = require('../models/bucket');
const http = require('http');
const axios = require('axios');
const FormData = require('form-data');

const DESTINATION_URL = 'http:/production-model:8000/api/v1/analyze/predict';

module.exports = async function predictImage(req, res) {

  if (!req.file)
    return res.status(400).json({ error: "Aucune image reçue" });

  try {

    const imagePath = req.file.path; // e.g. './uploads/abcdef.jpg'
    const filename = req.file.originalname;
    const mimeType = req.file.mimetype;
    const fileContent = fs.readFileSync(imagePath);

    const form = new FormData();
    form.append('file', fileContent, {
      filename: filename,
      contentType: mimeType
    });

    const response = await axios.post(DESTINATION_URL, form, {
      headers: {
        ...form.getHeaders()
      }
    });

    fs.unlinkSync(imagePath);

    res.status(response.status).json(response.data);

  }
  catch (err) {
    console.error(err);
    res.status(500).json({ error: "Échec de l'upload" });
  }

}
