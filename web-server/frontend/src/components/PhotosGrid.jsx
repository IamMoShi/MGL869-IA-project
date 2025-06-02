import React, { useEffect, useState } from "react";
import { Typography, Grid, Sheet } from "@mui/joy";
import ImageCard from "./ImageCard";

const PhotosGrid = () => {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:5001/api/images")
      .then((res) => res.json())
      .then((data) => {
          console.log("Réponse API :", data); // 👈 Ajoute ceci
        setImages(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Erreur lors du fetch des images :", err);
        setLoading(false);
      });
  }, []);

  return (
    <Sheet sx={{ px: 10, py: 5 }}>
      <Typography level="h2" sx={{ mb: 2, pb: 2 }}>
        Photos
      </Typography>

      {loading ? (
        <Typography>Chargement...</Typography>
      ) : (
        <Grid container spacing={2}>
          {images.map((src, index) => (
            <Grid xs={12} sm={6} md={4} lg={3} key={index}>
              <ImageCard imageUrl={src} category="Inconnue" />
            </Grid>
          ))}
        </Grid>
      )}
    </Sheet>
  );
};

export default PhotosGrid;
