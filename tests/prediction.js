const http = require('http');
const fs = require('fs');
const path = require('path');
// const AWS = require('aws-sdk');
const axios = require('axios');
const FormData = require('form-data');
const { log } = require('console');

SESSION_SECRET='secret'
MINIO_ENDPOINT='http://localhost:9000'
MINIO_ACCESS_KEY='minioadmin'
MINIO_SECRET_KEY='minioadmin'


// const s3 = new AWS.S3({
//   endpoint: MINIO_ENDPOINT,
//   accessKeyId: MINIO_ACCESS_KEY,
//   secretAccessKey: MINIO_SECRET_KEY,
//   s3ForcePathStyle: true,
//   signatureVersion: "v4",
// });

// async function uploadImageToS3(filePath, originalName, bucket = "images") {
//     console.log("Image reçue :", originalName);
//     console.log("Chemin local de l'image :", filePath);
    
//     const fileContent = fs.readFileSync(filePath);

//     const params = {
//         Bucket: bucket,
//         Key: originalName,
//         Body: fileContent,
//         ContentType: getMimeType(filePath),
//     };

//     try {
//         const data = await s3.upload(params).promise();
//         console.log("Upload réussi :", data.Location);
//     } catch (error) {
//         console.error("Erreur d'upload :", error);
//         throw error;
//     }

//     fs.unlinkSync(filePath);
// }

// Fonction utilitaire pour déterminer le type MIME basique selon l'extension
function getMimeType(filename) {
    const ext = path.extname(filename).toLowerCase();
    if (ext === '.jpg' || ext === '.jpeg') return 'image/jpeg';
    if (ext === '.png') return 'image/png';
    if (ext === '.gif') return 'image/gif';
    if (ext === '.webp') return 'image/webp';
    return 'application/octet-stream';
}

function predict(image, prediction_class) {

  request = 'http://127.0.0.1:5000/api/v1/analyze/image/' + image;
  // console.log('Requesting:', request);

  http.get(request, (res) => {
    let data = '';

    // A chunk of data has been received.
    res.on('data', (chunk) => {
      data += chunk;
    });

    // The whole response has been received.
    res.on('end', () => {
      // console.log('Response:', data);
      try {
        const jsonData = JSON.parse(data);
        console.log('Parsed JSON:', jsonData);
        if (jsonData.prediction) {
          console.log(`Prediction for ${image}:`, jsonData.prediction);
          if (jsonData.prediction === prediction_class) {
            console.log('\x1b[32m%s\x1b[0m', `Prediction matches expected class: ${prediction_class}`);
          } else {
            console.log('\x1b[31m%s\x1b[0m', `Prediction does not match expected class: ${prediction_class}`);
          }
        } else {
            console.log('\x1b[33m%s\x1b[0m', 'No prediction found in response.');
        }
      } catch (e) {
        console.error('Failed to parse JSON:', e.message);
      }
    });
  }).on('error', (err) => {
    console.error('Error:', err.message);
  }); 

}



const DESTINATION_URL = 'http://127.0.0.1:5000/api/v1/analyze/predict';

async function predictImage(filePath, originalName) {

  // console.log("Image reçue :", originalName);
  // console.log("Chemin local de l'image :", filePath);
  
  try {
  
    const fileContent = fs.readFileSync(filePath);

    const form = new FormData();
    form.append('file', fileContent, {
      filename: originalName,
      contentType: getMimeType(filePath)
    });

    const response = await axios.post(DESTINATION_URL, form, {
      headers: {
      ...form.getHeaders()
      }
    });

    console.log("Réponse du serveur :", response.data);

    if (response.data && response.data.prediction) {
      console.log('Prediction:', response.data.prediction);
    } else {
      console.log('No prediction field in response.');
    }

    return response.data.prediction;

  }
  catch (err) {
    console.error(err);
    res.status(500).json({ error: "Échec de l'upload" });
  }

}


const imagesDir = path.join(__dirname, 'images', 'seg_test', 'seg_test');
const imagesBuildingsDir = path.join(__dirname, 'images', 'seg_test', 'seg_test', 'buildings');
const imagesForestDir = path.join(__dirname, 'images', 'seg_test', 'seg_test', 'forest');
const imagesGlacierDir = path.join(__dirname, 'images', 'seg_test', 'seg_test', 'glacier'); 
const imagesMountainDir = path.join(__dirname, 'images', 'seg_test', 'seg_test', 'mountain');
const imagesSeaDir = path.join(__dirname, 'images', 'seg_test', 'seg_test', 'sea');
const imagesStreetDir = path.join(__dirname, 'images', 'seg_test', 'seg_test', 'street');

CLASSES = ["buildings", "forest", "glacier", "mountain", "sea", "street"]

// const imagesDir = path.join(__dirname, 'images', 'seg_pred', 'seg_pred_tiny');

async function run_tests() {

  try {

    nbFiles = 0;
    nbErrors = 0;

    const logStream = fs.createWriteStream('./tests/images-processing.log', { flags: 'w' });
    
    for (const className of CLASSES) {
      const classDir = path.join(imagesDir, className);
      logStream.write(`**************************************************\n`);
      logStream.write(`Processing class: ${className}\n`);
      if (fs.existsSync(classDir) && fs.lstatSync(classDir).isDirectory()) {
        const files = fs.readdirSync(classDir);
        for (const file of files) {
          if (/\.(jpg|jpeg|png)$/i.test(file)) {
          const fullPath = path.join(classDir, file);
          prediction = await predictImage(fullPath, file);
          if( prediction === className) {
            console.log(`Prediction for ${file} matches expected class: ${className}\n`);
          }
          else {
            logStream.write(`Prediction for ${file} does not match expected class: ${className}\n`);
            nbErrors++;
          }
          await new Promise(resolve => setTimeout(resolve, 250));
          nbFiles++;
          }
        }
      }
      logStream.write(`Processed files: ${nbFiles}\n`);
      logStream.write(`Errors found: ${nbErrors}\n`);
      if (nbFiles > 0) {
        const errorPercentage = ((nbErrors / nbFiles) * 100).toFixed(2);
        logStream.write(`Error percentage: ${errorPercentage}%\n`);
      } 
      nbFiles = 0; // Reset for next class
      nbErrors= 0; // Reset error count for next class
      logStream.write(`**************************************************\n`);
    }
    logStream.end();
  } catch (err) {
    console.error(err);
  }
}

run_tests();


console.log('All images processed.');
  



