import UploadFilesDragNDropRoute from "./UploadFilesForm/dragNDrop/UploadFilesDragNDropRoute";

const ImageUploaderDrawer = () => {

    return (
        <div className="lg:flex lg:w-full lg:flex-col mt-8">
            <nav className="flex flex-1 flex-col">
                <div className="flex items-center justify-center">
                    <div className="mx-auto w-full max-w-[550px]">
                        <UploadFilesDragNDropRoute/>
                    </div>
                </div>
            </nav>
        </div>
    );
};

export default ImageUploaderDrawer;
