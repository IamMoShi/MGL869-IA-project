
const uploadSF = require('../models/bucket');
const {wlogger, createMessage} = require('../winstonlogger.js');

const MODULE = 'upload.js';

module.exports = async function uploadImage(req, res) {
  if (!req.file) {
    erreur = "Aucune image reçue";
    wlogger.error(createMessage( Date.now(), 'PARAM_MISSING', MODULE, '/uploadImage', '', '', 'Aucune image reçue'));
    return res.status(400).json({ error: erreur });
  }

  try {
  
    // Save the image to a temporary location
    await uploadSF.uploadSingleFile(req, res);
        
    wlogger.info(createMessage( Date.now(), 'SUCCESS', MODULE, '/uploadImage', '', '', 'Image uploadé avec succès'));
    res.status(200).json({ error: "Succès de l'upload" });
  }
  catch (err) {
    wlogger.error(createMessage( Date.now(), 'CATCH_ERR', MODULE, '/uploadImage', '', '', 'Une exception a été attrappée durant le upload'));
    res.status(500).json({ error: "Échec de l'upload" });
  }

}