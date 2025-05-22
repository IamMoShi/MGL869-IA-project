const path = require('path');
const fs = require('fs');
const s3 = require('../services/minioClient');

module.exports = async function uploadImage(req, res) {
  if (!req.file) return res.status(400).json({ error: "Aucune image reçue" });

  const localPath = req.file.path;
  const filename = `${Date.now()}_${req.file.originalname}`;
  const bucket = "images";

  try {
    const fileContent = fs.readFileSync(localPath);

    const params = {
      Bucket: bucket,
      Key: filename,
      Body: fileContent,
      ContentType: req.file.mimetype,
    };

    const data = await s3.upload(params).promise();

    fs.unlinkSync(localPath);

    res.status(200).json({
      message: "Upload réussi",
      location: data.Location,
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Échec de l'upload" });
  }
};
