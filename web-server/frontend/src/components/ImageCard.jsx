import React from 'react';
import '../styles/ImageCard.css';
import { FiDownload } from 'react-icons/fi';
import {Dropdown, Menu, MenuButton, MenuItem} from "@mui/joy";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown"; // Icône de téléchargement

const ImageCard = ({ imageUrl, category }) => {
  return (
    <div className="image-card" style={{ backgroundImage: `url(${imageUrl})` }}>
      <div className="image-overlay">
        {/* Dropdown 1 */}
          <Dropdown>
            <MenuButton endDecorator={<KeyboardArrowDownIcon />} variant="soft">
              {category}
            </MenuButton>
            <Menu>
              <MenuItem>Sea</MenuItem>
              <MenuItem>Mountain</MenuItem>
            </Menu>
          </Dropdown>
        <button className="download-button">
          <FiDownload size={18} />
        </button>
      </div>
    </div>
  );
};

export default ImageCard;
