const {Image} = require("../models"); // importe ton modèle Sequelize Image
const uploadSF = require('../models/bucket');
const {wlogger, createMessage} = require('../winstonlogger.js');
const {get} = require("axios");
const axios = require("axios");
const {DataTypes} = require("sequelize");

const baseUrl = process.env.ML_API_URL;

const MODULE = 'upload.js';
module.exports = {
    uploadImage: async (req, res) => {
        if (!req.file) {
            erreur = "Aucune image reçue";
            wlogger.error(createMessage(Date.now(), 'PARAM_MISSING', MODULE, '/uploadImage', '', '', 'Aucune image reçue'));
            return res.status(400).json({error: erreur});
        }

        try {

            // Save the image to a temporary location
            const imageBucket = await uploadSF.uploadSingleFile(req.file);
            const imageName = imageBucket.Location.split('/').pop();

            let resML = await axios.get(`${baseUrl}/api/v1/analyze/image/${imageName}`)
                .then(({data}) => data)
                .catch(err => err.data);


            const CATEGORY_MAP = {
                buildings: 0,
                forest: 1,
                glacier: 2,
                mountain: 3,
                sea: 4,
                street: 5,
            };

            resML.category = CATEGORY_MAP[resML.prediction];

            await Image.create({filename: resML.filename, category: resML.category, created_at: Date.now()});

            wlogger.info(createMessage(Date.now(), 'SUCCESS', MODULE, '/uploadImage', '', '', 'Image uploadé avec succès'));
            res.status(200).json({error: "Succès de l'upload"});
        } catch (err) {
            console.log(err)
            wlogger.error(createMessage(Date.now(), 'CATCH_ERR', MODULE, '/uploadImage', '', '', 'Une exception a été attrappée durant le upload'));
            res.status(500).json({error: "Échec de l'upload"});
        }

    }
    ,

    uploadMultiImages: async (req, res) => {

        let resultBody = {
            status: "fail",
            message: "Upload error - DB or Minio Error",
        };

        const images = req.files;

        console.log('images :', images);

        if (!Array.isArray(images)) {
            wlogger.error(createMessage(Date.now(), 'PARAM_MISSING', MODULE, '/uploadImage', '', '', 'Aucunes images reçues'));
            return res.status(400).json({ error: 'No files uploaded or incorrect format.' });
        }

        if (images?.length) {

            try {
                await Promise.all(
                    images.map(async (fileObject) => {

                        // Save the image to a temporary location
                        const imageBucket = await uploadSF.uploadSingleFile(fileObject);
                        const imageName = imageBucket.Location.split('/').pop();

                        let resML = await axios.get(`http://fastapi-production-model:8000/api/v1/analyze/image/${imageName}`)
                            .then(({data}) => data)
                            .catch(err => err.data);
                        // save file info to database
                        const CATEGORY_MAP = {
                            buildings: 0,
                            forest: 1,
                            glacier: 2,
                            mountain: 3,
                            sea: 4,
                            street: 5,
                        };

                        resML.category = CATEGORY_MAP[resML.prediction];

                        await Image.create({filename: resML.filename, category: resML.category, created_at: Date.now()});


                    }),
                );

                resultBody = {
                    status: "success",
                    message: "Succès de l'upload",
                };
                res.status(200).json(resultBody);

            } catch (e) {
                console.error('error', e);
                 resultBody = {
                    status: "fail",
                    message: "Upload error - DB or Minio Error",
                };

                res.status(400).json(resultBody);
            }
        }

    }
}
