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
import {CATEGORY_MAP} from "../utils/categoryMap.js";
import {

  XMarkIcon,
} from "@heroicons/react/24/outline";

import {
  Dialog,
  DialogPanel, DialogTitle,
} from "@headlessui/react";
import ImageUploaderDrawer from "./images/uploader/ImageUploaderDrawer.js";

const Header = ({category}) => {
  const navigate = useNavigate();

  const [rightDrawerOpen, setRightDrawerOpen] = useState(false);


  const goToCategory = (category) => {
    navigate(`/${category}`);
  };

  const categories = Object.keys(CATEGORY_MAP);

  return (
      <>

        <Dialog open={rightDrawerOpen} onClose={setRightDrawerOpen} className="relative z-10">
          <div className="fixed inset-0"/>

          <div className="fixed inset-0 overflow-hidden">
            <div className="absolute inset-0 overflow-hidden">
              <div className="pointer-events-none fixed inset-y-0 right-0 flex max-w-full pl-10">
                <DialogPanel
                    transition
                    className="pointer-events-auto w-screen max-w-md transform transition duration-500 ease-in-out data-closed:translate-x-full sm:duration-700"
                >
                  <div className="flex h-full flex-col overflow-y-scroll bg-white py-6 shadow-xl">
                    <div className="px-4 sm:px-6">
                      <div className="flex items-start justify-between">
                        <DialogTitle className="text-base font-semibold text-gray-900">Televerser
                          Photos</DialogTitle>
                        <div className="ml-3 flex h-7 items-center">
                          <button
                              type="button"
                              onClick={() => setRightDrawerOpen(false)}
                              className="relative rounded-md bg-white text-gray-400 hover:text-gray-500 focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:outline-hidden"
                          >
                            <span className="absolute -inset-2.5"/>
                            <span className="sr-only">Close panel</span>
                            <XMarkIcon aria-hidden="true" className="size-6"/>
                          </button>
                        </div>
                      </div>
                    </div>
                    <div className="relative mt-6 flex-1 px-4 sm:px-6 bg-gray-100">
                      <ImageUploaderDrawer/>
                    </div>
                  </div>
                </DialogPanel>
              </div>
            </div>
          </div>
        </Dialog>
    <Box component="header" sx={{ px: 10, py : 5, display: 'flex', flexDirection: 'column', gap: 2 }}>
      {/* First Row */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Typography level="h4">SmartVue Photos</Typography>

        <Input placeholder="Rechercher..." sx={{ width: 500, ml: 15}} />

        <Box sx={{display: 'flex', gap: 1}}>
          <Button variant="outlined">Log in</Button>
          <Button variant="outlined">Sign up</Button>
          {/*<Button variant="solid" onClick={goToUpload}>Upload images</Button>*/}

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
