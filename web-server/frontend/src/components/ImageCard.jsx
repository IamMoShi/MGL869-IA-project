import React from 'react';
import '../styles/ImageCard.css';
import { FiDownload } from 'react-icons/fi';
import {Dropdown, Menu, MenuButton, MenuItem} from "@mui/joy";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown"; // Icône de téléchargement
import { ID_TO_CATEGORY, CATEGORY_MAP } from '../utils/categoryMap.js';

const ImageCard = ({ imageUrl, category, onSelectCategory }) => {
    const handleDownload = () => {
        const link = document.createElement("a");
        link.href = imageUrl;
        link.download = imageUrl.split('/').pop(); // nom du fichier
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      };
  return (
    <div className="image-card" style={{ backgroundImage: `url(${imageUrl})` }}>
      <div className="image-overlay">
        {/* Dropdown 1 */}
          <Dropdown>
              <MenuButton endDecorator={<KeyboardArrowDownIcon />} variant="soft">
                {ID_TO_CATEGORY[category].charAt(0).toUpperCase() + ID_TO_CATEGORY[category].slice(1) || "Choisir une catégorie"}
              </MenuButton>
              <Menu>
                {Object.entries(CATEGORY_MAP).map(([name, id]) =>
                  id !== category ? (
                    <MenuItem key={id}>
                      {name.charAt(0).toUpperCase() + name.slice(1)}
                    </MenuItem>
                  ) : null
                )}
              </Menu>
            </Dropdown>
        <button className="download-button" onClick={handleDownload}>
          <FiDownload size={18} />
        </button>
      </div>
    </div>
  );
};

export default ImageCard;
