import React, {useState} from "react";
import {
    Box,
    Button,
    Input,
    Typography,
    Dropdown,
    Menu,
    MenuItem,
    MenuButton,
} from '@mui/joy';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import {useNavigate} from "react-router-dom";

import ImageRightDrawer from "../common/ImageRightDrawer.jsx";
import {CATEGORY_MAP} from "../../utils/helpers.js";

const Header = ({category}) => {
    const navigate = useNavigate();

    const [rightDrawerOpen, setRightDrawerOpen] = useState(false);


    const goToCategory = (category) => {
        navigate(`/${category}`);
        window.location.reload();

    };

    const categories = Object.keys(CATEGORY_MAP);

    return (
        <>
            <ImageRightDrawer rightDrawerOpen={rightDrawerOpen} setRightDrawerOpen={setRightDrawerOpen}/>

            <Box component="header" sx={{ px: 10, py : 5, display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Typography level="h4">SmartVue Photos</Typography>

                    <Input placeholder="Rechercher..." sx={{ width: 500, ml: 15}} />

                    <Box sx={{display: 'flex', gap: 1}}>
                        <Button variant="outlined">Log in</Button>
                        <Button variant="outlined">Sign up</Button>
                        <button
                            onClick={() => setRightDrawerOpen(true)}
                            type="button"
                            className="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                        >
                            Upload
                        </button>
                    </Box>
                </Box>

                {/* Second Row: Category Buttons */}
                <Box sx={{display: 'flex', gap: 1, justifyContent: 'center'}}>
                    <Button variant={category === undefined ? "solid" : "outlined"} onClick={() => navigate('/')}>All</Button>
                    {categories.map(cat => (
                        <Button key={cat} variant={category === CATEGORY_MAP[cat] ? "solid" : "outlined"}
                                onClick={() => goToCategory(cat)}>
                            {cat}
                        </Button>
                    ))}
                </Box>

                {/* Third Row: Dropdowns & Export */}
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box sx={{ display: 'flex', gap: 1 }}>
                        {/* Dropdown 1 */}
                        <Dropdown>
                            <MenuButton endDecorator={<KeyboardArrowDownIcon />} variant="outlined">
                                Filter 1
                            </MenuButton>
                            <Menu>
                                <MenuItem>Elmt 1</MenuItem>
                                <MenuItem>Elmt 2</MenuItem>
                                <MenuItem>Elmt 3</MenuItem>
                                <MenuItem>Elmt 4</MenuItem>
                            </Menu>
                        </Dropdown>

                        {/* Dropdown 2 */}
                        <Dropdown>
                            <MenuButton endDecorator={<KeyboardArrowDownIcon />} variant="outlined">
                                Filter 2
                            </MenuButton>
                            <Menu>
                                <MenuItem>Elmt 1</MenuItem>
                                <MenuItem>Elmt 2</MenuItem>
                                <MenuItem>Elmt 3</MenuItem>
                                <MenuItem>Elmt 4</MenuItem>
                            </Menu>
                        </Dropdown>

                        <Button variant="solid">Export All</Button>
                    </Box>

                </Box>
            </Box>
        </>
    );
};

export default Header;