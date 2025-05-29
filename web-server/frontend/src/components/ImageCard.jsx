import React from 'react';
import '../styles/ImageCard.css';
import { FiDownload } from 'react-icons/fi'; // Icône de téléchargement

const ImageCard = ({ imageUrl, category }) => {
  return (
    <div className="image-card" style={{ backgroundImage: `url(${imageUrl})` }}>
      <div className="image-overlay">
        <button className="category-button">{category}</button>
        <button className="download-button">
          <FiDownload size={18} />
        </button>
      </div>
    </div>
  );
};

export default ImageCard;
