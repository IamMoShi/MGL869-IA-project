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
  
    // Save the image to a temporary location
    await uploadSF.uploadSingleFile(req, res);
    
    res.status(200).json({ error: "Succès de l'upload" });
    
  }
  catch (err) {
    console.error(err);
    res.status(500).json({ error: "Échec de l'upload" });
  }

}