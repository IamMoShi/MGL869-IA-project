const path = require('path');
const fs = require('fs');
const s3 = require('../services/minioClient');


module.exports = {

    uploadSingleFile: async (req, res) => {

        console.log("Image reçue :", req.file.originalname);

        const localPath = req.file.path;
        console.log("Chemin local de l'image :", localPath);
        const now = new Date();
        const yyyy = now.getFullYear();
        const mm = String(now.getMonth() + 1).padStart(2, '0');
        const dd = String(now.getDate()).padStart(2, '0');
        const hh = String(now.getHours()).padStart(2, '0');
        const min = String(now.getMinutes()).padStart(2, '0');
        const ss = String(now.getSeconds()).padStart(2, '0');
        const dateStr = `${yyyy}-${mm}-${dd}_${hh}-${min}-${ss}`;
        const filename = `${dateStr}_${req.file.originalname}`;
        console.log("Nom de l'image :", filename);
        const bucket = "images";

        const fileContent = fs.readFileSync(localPath);

        const params = {
            Bucket: bucket,
            Key: filename,
            Body: fileContent,
            ContentType: req.file.mimetype,
        };

        const data = await s3.upload(params).promise();

        fs.unlinkSync(localPath);

    }
}
