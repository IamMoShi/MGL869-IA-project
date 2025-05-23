const router = require('express').Router();
const multer = require('multer');
const upload = multer({ dest: 'uploads/' });
const predictHandler = require('../controllers/predict_image');

router.post('/predictimage', upload.single('file'), predictHandler);

module.exports = router;
