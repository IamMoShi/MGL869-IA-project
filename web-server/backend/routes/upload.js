const router = require('express').Router();
const multer = require('multer');
const upload = multer({ dest: 'uploads/' });
const {uploadImage, uploadMultiImages} = require('../controllers/upload');

router.post('/', upload.single('file'), uploadImage);
router.post('/multi', upload.array('file', 1000), uploadMultiImages);

module.exports = router;
