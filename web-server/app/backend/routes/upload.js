const router = require('express').Router();
const multer = require('multer');
const upload = multer({ dest: 'uploads/' });
const uploadHandler = require('../controllers/upload');

router.post('/upload', upload.single('file'), uploadHandler);

module.exports = router;
