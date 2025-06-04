const express = require("express");
const router = express.Router();
const AWS = require("aws-sdk");
const { Image } = require("../models"); // importe ton modèle Sequelize Image

// Configuration MinIO
const s3 = new AWS.S3({
  endpoint: "http://minio:9000",
  accessKeyId: "minioadmin",
  secretAccessKey: "minioadmin",
  s3ForcePathStyle: true,
  signatureVersion: "v4",
});

// GET /api/images?category=4
router.get("/", async (req, res) => {
  try {
    const categoryFilter = req.query.category;

    // Construction du filtre Sequelize selon query param
    const whereClause = {};
    if (categoryFilter !== undefined) {
      whereClause.category = categoryFilter;
    }

    // Récupère en base la liste des images filtrées
    const imagesData = await Image.findAll({
      where: whereClause,
      attributes: ["filename", "category"],
    });

    console.log("Images récupérées de la base :", imagesData);

    // Map pour retourner URLs complètes MinIO + catégorie (optionnel)
    const images = imagesData.map((img) => ({
      url: `http://localhost:9000/images/${img.filename}`,
      category: img.category,
      filename: img.filename,
    }));

    console.log("Images envoyées :", images);
    res.json(images);
  } catch (error) {
    console.error("Erreur dans /api/images :", error);
    res.status(500).json({ error: "Erreur de récupération des images" });
  }
});

// POST /api/images
router.put("/:filename", async (req, res) => {
  const { filename } = req.params;
  const { category } = req.body || {};

  if (category === undefined) {
    return res.status(400).json({ error: "Champ 'category' requis" });
  }

  try {
    const image = await Image.findOne({ where: { filename } });
    if (!image) {
      return res.status(404).json({ error: "Image non trouvée" });
    }

    image.category = category;
    await image.save();

    res.json({ success: true, image });
  } catch (err) {
    console.error("Erreur PUT /api/images/:filename", err);
    res.status(500).json({ error: "Erreur serveur" });
  }
});


module.exports = router;
