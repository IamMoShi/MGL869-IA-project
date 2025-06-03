import {UploadFilesFormUIProps} from "~/utils/types";
import {LoadSpinner} from "./LoadSpinner";


export function UploadFilesFormUI({isLoading, fileInputRef, uploadToServer, maxFileSize,}: UploadFilesFormUIProps) {
    return (
        <form className="flex flex-col items-center justify-center gap-3" onSubmit={uploadToServer}>
            <div className="bg-white shadow rounded-lg w-full px-5 pt-3 pb-5">
                <h1 className="text-lg">Televerer vos imagees </h1>
                <p className="text-lg">{`Total file(s) size should not exceed ${maxFileSize} MB`}</p>


                {isLoading ? (
                    <LoadSpinner/>
                ) : (
                    <>
                        <div className="flex h-16 gap-5 my-4">
                            <div className="flex-1 flex flex-col">
                                <input
                                    id="file"
                                    type="file"
                                    multiple
                                    className="rounded-md border bg-gray-100 p-2 py-5"
                                    required
                                    ref={fileInputRef}
                                />
                            </div>

                        </div>
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
