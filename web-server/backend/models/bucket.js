const path = require('path');
const fs = require('fs');
const s3 = require('../services/minioClient');
const {renameImage} = require("../utils/helpers");


module.exports = {
    uploadSingleFile: async (file) => {
        const localPath = file.path;
        const filename = renameImage(file.originalname);
        const bucket = "images";
        const fileContent = fs.readFileSync(localPath);
        const params = {
            Bucket: bucket,
            Key: filename,
            Body: fileContent,
            ContentType: file.mimetype,
        };

        const data = await s3.upload(params).promise();
        fs.unlinkSync(localPath);

        return data;
    },





}
