import React, {useState} from "react";

import {FILE_NUMBER_LIMIT, MAX_FILE_SIZE} from "../../../../../utils/fileUploadHelpers.js";
import {UploadFilesFormDragNDrop} from "./UploadFilesFormDragNDrop.jsx";



const  UploadFilesDragNDropRoute = () =>{

  const [imagesToUpload, setImagesToUpload] = useState([]);

  function uploadFiles(files) {
    setImagesToUpload([...imagesToUpload, ...files]);
  }

  function deleteFile(indexImg) {
    const updatedList = imagesToUpload.filter((ele, index) => index !== indexImg);
    setImagesToUpload(updatedList);
  }

  return (
    <UploadFilesFormDragNDrop
      maxFileSize={MAX_FILE_SIZE}
      onUpload={uploadFiles}
      onDelete={deleteFile}
      count={FILE_NUMBER_LIMIT}
      formats={["jpg", "jpeg", "png"]}
      imagesToUpload={imagesToUpload}
    />
  );
}

export default  UploadFilesDragNDropRoute;