const s3 = require("../services/minioClient");


module.exports = {
    renameImage:  (fileName) => {
        const now = new Date();
        const yyyy = now.getFullYear();
        const mm = String(now.getMonth() + 1).padStart(2, '0');
        const dd = String(now.getDate()).padStart(2, '0');
        const hh = String(now.getHours()).padStart(2, '0');
        const min = String(now.getMinutes()).padStart(2, '0');
        const ss = String(now.getSeconds()).padStart(2, '0');
        const dateStr = `${yyyy}-${mm}-${dd}_${hh}-${min}-${ss}`;

        return `${dateStr}_${fileName}`;
    },


       deleteFileFromBucket : async({ bucketName, fileName }) =>{
           try {
               const params = {
                   Bucket: bucketName,
                   Key: fileName,
               };
               await s3.deleteObject(params).promise();
               console.log(`✅ Fichier supprimé : ${fileName}`);
               return true;
           } catch (err) {
               console.error("❌ Erreur lors de la suppression :", err);
               return  false;
           }
    }
};
