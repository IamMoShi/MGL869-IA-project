const express = require("express");
const router = express.Router();
const AWS = require("aws-sdk");

// Configuration MinIO
const s3 = new AWS.S3({
  endpoint: "http://localhost:9000",
  accessKeyId: "minioadmin",
  secretAccessKey: "minioadmin",
  s3ForcePathStyle: true, // important for MinIO
  signatureVersion: "v4",
});

// GET /api/images : retourne la liste des images publiques
router.get("/", async (req, res) => {
  try {
    const data = await s3.listObjectsV2({ Bucket: "images" }).promise();

    const images = (data.Contents || []).map((item) => {
      return `http://localhost:9000/images/${item.Key}`;
    });

    res.json(images);
  } catch (error) {
    console.error("Erreur MinIO :", error);
    res.status(500).json({ error: "Erreur de récupération des images" });
  }
});

module.exports = router;
