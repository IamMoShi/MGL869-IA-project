const path = require("path");
const fs = require("fs");
const s3 = require("../services/minioClient");

module.exports = {
    uploadSingleFile: async (req, res) => {
        console.log("Image reçue :", req.file.originalname);

        const localPath = req.file.path;
        console.log("Chemin local de l'image :", localPath);
        const now = new Date();
        const yyyy = now.getFullYear();
        const mm = String(now.getMonth() + 1).padStart(2, "0");
        const dd = String(now.getDate()).padStart(2, "0");
        const hh = String(now.getHours()).padStart(2, "0");
        const min = String(now.getMinutes()).padStart(2, "0");
        const ss = String(now.getSeconds()).padStart(2, "0");
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
    },

    imageslist: async (req, res) => {
        const bucketName = req.query.bucket || "images"; // Get bucket from query or use default

        // Helper function to list objects
        function listObjects(bucketName) {
            return new Promise((resolve, reject) => {
                const objectsList = [];
                const stream = minioClient.listObjectsV2(bucketName, "", true);

                stream.on("data", (obj) => {
                    objectsList.push({
                        name: obj.name,
                        size: obj.size,
                        lastModified: obj.lastModified,
                        etag: obj.etag,
                    });
                });

                stream.on("error", (err) => reject(err));
                stream.on("end", () => resolve(objectsList));
            });
        }

        try {
            // List all objects in the bucket
            const objectsList = await listObjects(bucketName);
            res.json({
                success: true,
                bucket: bucketName,
                files: objectsList,
            });
        } catch (err) {
            console.error("Error listing files:", err);
            res.status(500).json({
                success: false,
                message: "Failed to list files",
                error: err.message,
            });
        }
    },
};
