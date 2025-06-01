import React, {useState} from "react";
import '../styles/Home.css';

import Header from "../components/Header";
import PhotosGrid from "../components/PhotosGrid";
import {Typography} from "@mui/joy";

function Home() {
  const [message, setMessage] = useState('');
  const [prediction, setPrediction] = useState('');

  const handleUpload = async () => {
    const res = await fetch('http://localhost:5000/upload', { method: 'POST' });
    const data = await res.json();
    setMessage(data.message);
  };

  // const handlePredict = async () => {
  //   const res = await fetch('http://localhost:5000/api/images/predict', { method: 'POST' });
  //   const data = await res.json();
  //   setPrediction(data.prediction);
  // };

    return (
        <div className="App">
            <Header/>
            <PhotosGrid/>
        </div>
    );
}

export default Home;