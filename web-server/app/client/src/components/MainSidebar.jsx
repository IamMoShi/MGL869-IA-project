"use client";

import { CustomDragDrop } from "./CustomDragDrop";

import { useState } from "react";

const MainSidebar = () => {
  const [ownerLicense, setOwnerLicense] = useState([]);

  function uploadFiles(files) {
    setOwnerLicense([...ownerLicense, ...files]);

    console.log("ownerLicense", ownerLicense);
  }

  function deleteFile(indexImg) {
    const updatedList = ownerLicense.filter((ele, index) => index !== indexImg);
    setOwnerLicense(updatedList);
  }

  return (
    /* Static sidebar for desktop */
    <div className="hidden lg:fixed lg:inset-y-0 lg:z-50 lg:flex lg:w-92 lg:flex-col">
      <div className="flex grow flex-col gap-y-5 overflow-y-auto border-r border-gray-200 bg-gray-100 px-6">
        <div className="flex h-16 shrink-0 items-center">
          <span className="h-8 w-auto font-bold">SmartVue Photos</span>
        </div>

        <nav className="flex flex-1 flex-col">
          <div className="flex items-center justify-center">
            <div className="mx-auto w-full max-w-[550px]">
              <CustomDragDrop
                ownerLicense={ownerLicense}
                onUpload={uploadFiles}
                onDelete={deleteFile}
                count={30}
                formats={["jpg", "jpeg", "png"]}
              />
            </div>
          </div>
        </nav>
      </div>
    </div>
  );
};

export default MainSidebar;
