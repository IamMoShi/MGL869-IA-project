const express = require("express");
const router = express.Router();
const AWS = require("aws-sdk");
const { Image } = require("../models");
const {deleteFileFromBucket} = require("../utils/helpers"); // importe ton modèle Sequelize Image

// Configuration MinIO
// const s3Client = new AWS.S3({
//   endpoint: "http://localhost:9000",
//   accessKeyId: "minioadmin",
//   secretAccessKey: "minioadmin",
//   s3ForcePathStyle: true,
//   signatureVersion: "v4",
// });

// GET /api/images?category=4
router.get("/", async (req, res) => {
  try {
    const categoryFilter = req.query.category;
    const limit = parseInt(req.query.limit, 10) || 10;
    const skip = parseInt(req.query.skip, 10) || 0;

    // Construction du filtre Sequelize selon query param
    const whereClause = {};
    if (categoryFilter !== undefined) {
      whereClause.category = categoryFilter;
    }

    // Récupère en base la liste des images filtrées
    // const imagesTotal = await Image.findAll({
    //   where: whereClause,
    //   attributes: ["filename", "category"],
    // });

    const { rows: imagesData, count: total } = await Image.findAndCountAll({
      where: whereClause,
      attributes: ["filename", "category"],
      limit,
      offset: skip,
      order: [['created_at', 'DESC']], // tri optionnel
    });


    // Map pour retourner URLs complètes MinIO + catégorie (optionnel)
    const images = imagesData.map((img) => ({
      url: `http://localhost:9000/images/${img.filename}`,
      category: img.category,
      filename: img.filename,
    }));

    console.log("Images envoyées :", images);
    res.json({
      images,
      total,       // total matching items (non paginé)
      limit,
      skip,
      page: Math.floor(skip / limit) + 1
    });
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

    console.log('category', category);

    image.category = category;
    await image.save();


    console.log('image', image);

    res.json({ success: true, image });
  } catch (err) {
    console.error("Erreur PUT /api/images/:filename", err);
    res.status(500).json({ error: "Erreur serveur" });
  }
});


router.delete("/:filename/delete", async  (req, res)=>{
  console.log("DELETE")
  if (req.method !== 'DELETE') {
    res.status(405).json({ message: 'Only DELETE requests are allowed' })
  }

  const { filename } = req.params
  console.log("DELETE filename", filename)
  if (!filename || typeof filename !== 'string') {
    return res.status(400).json({ message: 'Missing or invalid filename' })
  }

  // Get the file name in bucket from the database
  const image = await Image.findOne({ where: { filename } });


  if (!image) {
    return res.status(404).json({ message: 'Image not found' })
  }
  // Delete the file from the bucket
  const bucket = await deleteFileFromBucket({
    bucketName: process.env.S3_BUCKET_NAME,
    fileName: filename,
  })

  console.log("deleteFileFromBucket", bucket)
  // Delete the file from the database
  const deletedItem = await Image.destroy({
    where: {
      filename,
    },
  })

  console.log("deletedItem", deletedItem)

  if (deletedItem && bucket) {
    res.status(200).json({ message: 'Image deleted successfully' })
  } else {
    res.status(404).json({ message: 'Image not found - Error' })
  }
});


module.exports = router;
