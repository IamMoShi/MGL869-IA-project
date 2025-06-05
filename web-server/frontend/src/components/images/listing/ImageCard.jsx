import React, {useState} from 'react';
import '../../../styles/ImageCard.css';
import {Dropdown, Menu, MenuButton, MenuItem} from "@mui/joy";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown"; // Icône de téléchargement
import {ID_TO_CATEGORY, CATEGORY_MAP, getCategoryStatus} from '../../../utils/helpers';
import ImageDialog from "../../common/ImageDialog.jsx";
import {TopNotification} from "../../../utils/helpers.js";

const ImageCard = ({imageUrl, category, fetchData}) => {


    const [currentCategory, setCurrentCategory] = useState(category);
    const [open, setOpen] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    const handleDownload = () => {
        const link = document.createElement("a");
        link.href = imageUrl;
        link.download = imageUrl.split('/').pop(); // nom du fichier
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };


    const handleDelete = async (filename) => {
        setIsLoading(true);
        try {
            const filename = imageUrl.split('/').pop();
            await fetch(`http://localhost:5001/api/images/${filename}/delete`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                },
            });
            setIsLoading(false);
            setOpen(false)
            fetchData()
            await TopNotification.fire({
                icon: "success",
                title: "Image deleted",
            });
        } catch (error) {
            setIsLoading(false);
            setOpen(false)
            fetchData()
            console.error("Erreur DELETE :", error);
        }
    }


    const handleCategoryChange = async (newCategory) => {
        setIsLoading(true);
        try {
            const filename = imageUrl.split('/').pop();
            const response = await fetch(`http://localhost:5001/api/images/${filename}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({category: newCategory}),
            });

            if (!response.ok) {
                throw new Error("Erreur lors de la mise à jour de la catégorie");
            }
            setIsLoading(false);
            setCurrentCategory(newCategory);
            await TopNotification.fire({
                icon: "success",
                title: "Category changed",
            });
        } catch (error) {
            setIsLoading(false);
            console.error("Erreur PUT :", error);
        }
    };


    return (
        <>
            <ImageDialog isLoading={isLoading} open={open} setOpen={setOpen} image={imageUrl}
                         category={getCategoryStatus(currentCategory)} handleDownload={handleDownload}
                         handleCategoryChange={handleCategoryChange}
                         handleDelete={handleDelete}/>
            <div className="image-card" style={{backgroundImage: `url(${imageUrl})`}} onClick={() => setOpen(true)}>
                <div className="image-overlay">
                    {/* Dropdown 1 */}
                    <Dropdown>
                        <MenuButton endDecorator={<KeyboardArrowDownIcon/>} variant="soft">
                            {ID_TO_CATEGORY[currentCategory].charAt(0).toUpperCase() + ID_TO_CATEGORY[currentCategory].slice(1) || "Choisir une catégorie"}
                        </MenuButton>
                        <Menu>
                            {Object.entries(CATEGORY_MAP).map(([name, id]) =>
                                id !== category ? (
                                    <MenuItem key={id} onClick={() => handleCategoryChange(id)}>
                                        {name.charAt(0).toUpperCase() + name.slice(1)}
                                    </MenuItem>
                                ) : null
                            )}
                        </Menu>
                    </Dropdown>
                </div>
            </div>
        </>
    );
};

export default ImageCard;
