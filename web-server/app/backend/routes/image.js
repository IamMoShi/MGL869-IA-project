const router = require("express").Router();
const imagesList = require("../controllers/images");

router.get("/images", imagesList.list);

module.exports = router;
