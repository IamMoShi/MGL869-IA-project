import React, {useState, useRef, useEffect} from "react";

import {createFormData, MAX_FILE_SIZE_NEXTJS_ROUTE, validateFiles} from "../../../../../utils/fileUploadHelpers.js";
import {UploadFilesFormDragNDrop} from "./UploadFilesFormDragNDrop.jsx";



const  UploadFilesDragNDropRoute = () =>{

  const [imagesToUpload, setImagesToUpload] = useState([]);

  function uploadFiles(files) {
    setImagesToUpload([...imagesToUpload, ...files]);
    console.log("imagesToUpload", imagesToUpload);
  }

  function deleteFile(indexImg) {
    const updatedList = imagesToUpload.filter((ele, index) => index !== indexImg);
    setImagesToUpload(updatedList);
  }

  return (
    <UploadFilesFormDragNDrop
      maxFileSize={MAX_FILE_SIZE_NEXTJS_ROUTE}
      onUpload={uploadFiles}
      onDelete={deleteFile}
      count={30}
      formats={["jpg", "jpeg", "png"]}
      imagesToUpload={imagesToUpload}
    />
  );
}

export default  UploadFilesDragNDropRoute;