import React from "react";
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
import MenuIcon from '@mui/icons-material/Menu';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';

const Header = () => {
  return (
    <Box component="header" sx={{ px: 10, py : 5, display: 'flex', flexDirection: 'column', gap: 2 }}>
      {/* First Row */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Typography level="h4">SmartVue Photos</Typography>

        <Input placeholder="Rechercher..." sx={{ width: 500, ml: 15}} />

        <Box sx={{ display: 'flex', gap: 1}}>
          <Button variant="outlined">Log in</Button>
          <Button variant="outlined">Sign up</Button>
          <Button variant="solid">Upload images</Button>
        </Box>
      </Box>

      {/* Second Row: Category Buttons */}
      <Box sx={{ display: 'flex', gap: 1, justifyContent: 'center'}}>
        <Button variant="solid">All</Button>
        <Button variant="solid">Sea</Button>
        <Button variant="solid">Mountain</Button>
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

        <Typography level="body-sm">1-100 à 1 000 000</Typography>
      </Box>
    </Box>
  );
};

export default Header;
