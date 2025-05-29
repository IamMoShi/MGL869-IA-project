import React from "react";
import { Typography, Grid, Sheet } from "@mui/joy";
import ImageCard from "./ImageCard";

const PhotosGrid = () => {
  const images = [
    'https://my.alfred.edu/zoom/_images/foster-lake.jpg',
    'https://my.alfred.edu/zoom/_images/foster-lake.jpg',
    'https://my.alfred.edu/zoom/_images/foster-lake.jpg',
    'https://my.alfred.edu/zoom/_images/foster-lake.jpg',
    'https://my.alfred.edu/zoom/_images/foster-lake.jpg',
    'https://my.alfred.edu/zoom/_images/foster-lake.jpg',
  ];

  return (
    <Sheet sx={{ p: 3 }}>
      <Typography level="h2" sx={{ mb: 2 }}>
        Photos
      </Typography>

      <Grid container spacing={2}>
        {images.map((src, index) => (
          <Grid xs={12} sm={6} md={4} lg={3} key={index}>
            <ImageCard imageUrl={src} category="Sea" />
          </Grid>
        ))}
      </Grid>
    </Sheet>
  );
};

export default PhotosGrid;
