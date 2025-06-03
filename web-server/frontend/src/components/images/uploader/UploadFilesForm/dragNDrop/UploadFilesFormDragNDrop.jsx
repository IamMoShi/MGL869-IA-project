import {LoadSpinner} from "../LoadSpinner.js";
import {useEffect, useRef, useState} from "react";
import {FaUpload} from "react-icons/fa";
import {BsX} from "react-icons/bs";
import Swal from "sweetalert2";
import {createFormData, MAX_FILE_SIZE_NEXTJS_ROUTE, validateFiles} from "../../../../../utils/fileUploadHelpers.js";
import TopNotification from "sweetalert2";


export function UploadFilesFormDragNDrop({
                                             maxFileSize, imagesToUpload,
                                             onUpload, onDelete, count, formats,
                                         }) {

    const dropContainer = useRef(null);
    const [dragging, setDragging] = useState(false);
    const [file, setFile] = useState([]);
    const [isLoading, setIsLoading] = useState(false);


    const fileInputRef = useRef(null);

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

        if (imagesToUpload.length >= count) {
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
    }, [imagesToUpload]);

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
        if (!fileInputRef.current?.files?.length) {
            alert("Please, select file you want to upload");
            return;
        }
        const files = Object.values(fileInputRef.current?.files);
        const filesInfo = files.map((file) => ({
            originalFileName: file.name,
            fileSize: file.size,
        }));

        const filesValidationResult = validateFiles(
            filesInfo,
            MAX_FILE_SIZE_NEXTJS_ROUTE,
        );
        if (filesValidationResult) {
            alert(filesValidationResult);
            return;
        }

        setIsLoading(true);

        const formData = createFormData(files);

        try {
            const response = await fetch("http://localhost:5001/api/upload/multi", {
                method: "POST",
                body: formData,
            });
            setIsLoading(false);
            await TopNotification.fire({
                icon: "success",
                title: "Image(s) uploaded",
            });


        }catch (e){
            setIsLoading(false);
            await TopNotification.fire({
                icon: "error",
                title: `Image(s) not uploaded - ${e}`,
            });

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
                            <FaUpload size={18}/>
                        </div>
                        <div className="text-[12px] font-normal text-gray-500">
                            <input
                                className="opacity-0 hidden"
                                type="file"
                                multiple
                                accept="image/*"
                                ref={fileInputRef}
                                onChange={(e) => handleDrop(e, "inputFile")}
                            />
                            <span
                                className="text-[#4070f4] cursor-pointer"
                                onClick={() => {
                                    fileInputRef.current.click();
                                }}
                            >
                Click to upload
              </span>{" "}
                            or drag and drop
                        </div>
                        <div className="text-[10px] font-normal text-gray-500">
                            Only two files PNG, JPG or JPEG
                        </div>
                        <div className="text-[10px] font-normal text-red-500">
                            {`Total file(s) size should not exceed ${maxFileSize} MB`}
                        </div>
                    </div>
                </div>
                <div className="pt-2.5">
                    <ul role="list" className="divide-y divide-gray-200">
                        {imagesToUpload.map((img, index) => (
                            <li key={index} className="px-1 py-1 sm:px-0">
                                <div className="w-full px-3 py-1.5 rounded-md bg-slate-200 space-y-3">
                                    <div className="flex justify-between">
                                        <div className="w-[70%] flex justify-start items-center space-x-2">
                                            <div
                                                className="text-[#5E62FF] text-[24px] cursor-pointer"
                                                onClick={() => showImage(img.photo)}
                                            >

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
                                                <div
                                                    className="text-[10px] font-medium text-gray-400">{`${Math.floor(
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
                                                    <BsX className="ml-auto"/>
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


                {isLoading ? (
                    <LoadSpinner/>
                ) : (
                    <>

                        <div className="mt-8">
                            <button
                                disabled={isLoading}
                                className="w-full rounded-md border border-transparent bg-indigo-600 px-4 py-3 text-base font-medium text-white shadow-xs hover:bg-indigo-700 focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-50 focus:outline-hidden"
                            >
                                Upload
                            </button>
                        </div>
                    </>
                )}
            </div>
        </form>
    );
}
