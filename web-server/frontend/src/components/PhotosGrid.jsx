import React, { useEffect, useState } from "react";
import { Typography, Grid, Sheet } from "@mui/joy";
import ImageCard from "./ImageCard";
import { ID_TO_CATEGORY } from '../utils/categoryMap.js';

const PhotosGrid = ({ category }) => {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);


  useEffect(() => {
    setLoading(true);
    let path = `http://localhost:5001/api/images?category=${category}`;
    if (category === undefined) {
        path = "http://localhost:5001/api/images";
    }
    fetch(path)
      .then((res) => res.json())
      .then((data) => {
        console.log("Données reçues:", data); // Pour vérifier ce que tu reçois
        setImages(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Erreur lors du fetch des images :", err);
        setLoading(false);
      });
  }, [category]);  // Ce useEffect se déclenche à chaque changement de category

  return (
    <Sheet sx={{ px: 10, py: 5 }}>
        <Typography textAlign="right" level="body-sm">{images.length} image{images.length <= 1 ? "" : "s"} trouvée{images.length <= 1 ? "" : "s"}</Typography>

      <Typography level="h2" sx={{ mb: 2, pb: 2 }}>
        Photos {category !== undefined ? ` - ${ID_TO_CATEGORY[category]}` : ""}
      </Typography>

      {loading ? (
        <Typography>Loading...</Typography>
      ) : (
        <Grid container spacing={2}>
          {images.map((image, index) => (
            <Grid xs={12} sm={6} md={4} lg={3} key={index}>
              <ImageCard imageUrl={image.url} category={image.category} />
            </Grid>
          ))}
        </Grid>
      )}
    </Sheet>
  );
};

export default PhotosGrid;
