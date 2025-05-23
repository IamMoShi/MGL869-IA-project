const path = require('path');
const fs = require('fs');
const s3 = require('../services/minioClient');
const uploadSF = require('../models/bucket');
const http = require('http');
const axios = require('axios');
const FormData = require('form-data');

const DESTINATION_URL = 'http:/ia-api:8000/api/v1/analyze/predict';

module.exports = async function uploadImage(req, res) {

  if (!req.file)
    return res.status(400).json({ error: "Aucune image reçue" });

  try {
  
    const fileBuffer = req.file.buffer; // Buffer of the uploaded file

    const imagePath = req.file.path; // e.g. './uploads/abcdef.jpg'
    const filename = req.file.originalname;
    const tempFilePath = path.join(imagePath, filename);
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

    res.status(response.status).json(response.data);
    
    fs.unlinkSync(imagePath);

    // Save the image to a temporary location
    // await uploadSF.uploadSingleFile(req, res);
   
  
  }
  catch (err) {
    console.error(err);
    res.status(500).json({ error: "Échec de l'upload" });
  }

}