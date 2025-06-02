"use client";

import { useRef, useEffect, useState } from "react";
import { FaUpload, FaRegFileImage, FaRegFile } from "react-icons/fa";
import { BsX } from "react-icons/bs";
import Swal from "sweetalert2";
import axios from "axios";

export function CustomDragDrop({
  ownerLicense,
  onUpload,
  onDelete,
  count,
  formats,
}) {
  const dropContainer = useRef(null);
  const [dragging, setDragging] = useState(false);
  const fileRef = useRef(null);

  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadedFileURL, setUploadedFileURL] = useState("");
  const [file, setFile] = useState([])

  function handleDrop(e, type) {
    let files;
    if (type === "inputFile") {
      files = [...e.target.files];
      setFile([...e.target.files]);
    } else {
      e.preventDefault();
      e.stopPropagation();
      setDragging(false);
      files = [...e.dataTransfer.files];
    }

    const allFilesValid = files.every((file) => {
      return formats.some((format) => file.type.endsWith(`/${format}`));
    });

    if (ownerLicense.length >= count) {
      showAlert(
        "warning",
        "Maximum Files",
        `Only ${count} files can be uploaded`
      );
      return;
    }
    if (!allFilesValid) {
      showAlert(
        "warning",
        "Invalid Media",
        `Invalid file format. Please only upload ${formats
          .join(", ")
          .toUpperCase()}`
      );
      return;
    }
    if (count && count < files.length) {
      showAlert(
        "error",
        "Error",
        `Only ${count} file${count !== 1 ? "s" : ""} can be uploaded at a time`
      );
      return;
    }

    if (files && files.length) {
      const nFiles = files.map(async (file) => {
        const base64String = await convertFileBase64(file);
        return {
          name: file.name,
          photo: base64String,
          type: file.type,
          size: file.size,
        };
      });

      Promise.all(nFiles).then((newFiles) => {
        onUpload(newFiles);
        TopNotification.fire({
          icon: "success",
          title: "Image(s) uploaded",
        });
      });
    }
  }

  async function convertFileBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        resolve(reader.result);
      };
      reader.onerror = (error) => {
        reject(error);
      };
    });
  }

  useEffect(() => {
    function handleDragOver(e) {
      e.preventDefault();
      e.stopPropagation();
      setDragging(true);
    }
    function handleDragLeave(e) {
      e.preventDefault();
      e.stopPropagation();
      setDragging(false);
    }
    dropContainer.current.addEventListener("dragover", handleDragOver);
    dropContainer.current.addEventListener("drop", handleDrop);
    dropContainer.current.addEventListener("dragleave", handleDragLeave);

    return () => {
      if (dropContainer.current) {
        dropContainer.current.removeEventListener("dragover", handleDragOver);
        dropContainer.current.removeEventListener("drop", handleDrop);
        dropContainer.current.removeEventListener("dragleave", handleDragLeave);
      }
    };
  }, [ownerLicense]);

  const TopNotification = Swal.mixin({
    toast: true,
    position: "bottom-end",
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.addEventListener("mouseenter", Swal.stopTimer);
      toast.addEventListener("mouseleave", Swal.resumeTimer);
    },
  });

  function showAlert(icon, title, text) {
    Swal.fire({
      icon: icon,
      title: title,
      text: text,
      showConfirmButton: false,
      width: 500,
      timer: 1500,
    });
  }

  function showImage(image) {
    Swal.fire({
      imageUrl: image,
      showCloseButton: true,
      showConfirmButton: false,
      width: 450,
    });
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    // if (!ownerLicense[0]) return;
    if (!file[0]) return;

    const formData = new FormData();
    // formData.append("file", ownerLicense[0]);
    formData.append("file", file[0]);

    console.log('file', file);

    try {
      const response = await axios.post(
        "http://localhost:5000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          onUploadProgress: (progressEvent) => {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / (progressEvent.total || 1)
            );
            setUploadProgress(percentCompleted);
          },
        }
      );
      console.log("Upload Successful:", response.data);
      setUploadedFileURL(response.data.fileUrl); // Assuming the response contains the uploaded file URL
    } catch (error) {
      console.error("Error uploading file:", error.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="bg-white shadow rounded-lg w-full px-5 pt-3 pb-5">
        <div className="pb-[8px] border-b border-[#e0e0e0] bg-white">
          <h2 className="text-black text-[12px] font-[700]">
            Drag and Drop Container
          </h2>
        </div>
        <div
          className={`${
            dragging
              ? "border border-[#2B92EC] bg-[#EDF2FF]"
              : "border-dashed border-[#e0e0e0]"
          } flex items-center justify-center mx-auto text-center border-2 rounded-md mt-4 py-5`}
          ref={dropContainer}
        >
          <div className="flex-1 flex flex-col">
            <div className="mx-auto text-gray-400 mb-2">
              <FaUpload size={18} />
            </div>
            <div className="text-[12px] font-normal text-gray-500">
              <input
                className="opacity-0 hidden"
                type="file"
                multiple
                accept="image/*"
                ref={fileRef}
                onChange={(e) => handleDrop(e, "inputFile")}
              />
              <span
                className="text-[#4070f4] cursor-pointer"
                onClick={() => {
                  fileRef.current.click();
                }}
              >
                Click to upload
              </span>{" "}
              or drag and drop
            </div>
            <div className="text-[10px] font-normal text-gray-500">
              Only two files PNG, JPG or JPEG
            </div>
          </div>
        </div>
        <div className="pt-2.5">
          <ul role="list" className="divide-y divide-gray-200">
            {ownerLicense.map((img, index) => (
              <li key={index} className="px-1 py-1 sm:px-0">
                <div className="w-full px-3 py-1.5 rounded-md bg-slate-200 space-y-3">
                  <div className="flex justify-between">
                    <div className="w-[70%] flex justify-start items-center space-x-2">
                      <div
                        className="text-[#5E62FF] text-[24px] cursor-pointer"
                        onClick={() => showImage(img.photo)}
                      >
                        {
                          // img.type.match(/image.*/i) ? (
                          //   <FaRegFileImage />
                          // ) : (
                          //   <FaRegFile />
                          // )
                        }
                        <img
                          alt={img.name}
                          src={img.photo}
                          className="size-12 flex-none rounded-md bg-gray-100 object-cover"
                        />
                      </div>
                      <div className=" space-y-1">
                        <div className="text-xs font-medium text-gray-500">
                          {img.name}
                        </div>
                        <div className="text-[10px] font-medium text-gray-400">{`${Math.floor(
                          img.size / 1024
                        )} KB`}</div>
                      </div>
                    </div>
                    <div className="flex-1 flex justify-end">
                      <div className="space-y-1">
                        <div
                          className="text-gray-500 text-[17px] cursor-pointer"
                          onClick={() => onDelete(index)}
                        >
                          <BsX className="ml-auto" />
                        </div>
                        <div className="text-[10px] font-medium text-gray-400">
                          Done
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {ownerLicense.length === 0 ? (
        <></>
      ) : (
        <div className="mt-10">
          <button
            type="submit"
            className="w-full rounded-md border border-transparent bg-indigo-600 px-4 py-3 text-base font-medium text-white shadow-xs hover:bg-indigo-700 focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-50 focus:outline-hidden"
          >
            Upload
          </button>

          {/*<progress value={uploadProgress} max="100"></progress>*/}
          {/*{uploadProgress > 0 && <p>Upload Progress: {uploadProgress}%</p>}*/}
        </div>
      )}
    </form>
  );
}
