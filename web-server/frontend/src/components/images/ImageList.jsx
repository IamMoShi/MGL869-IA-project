"use client";

const ImageList = ({ ownerLicense }) => {
  return (
    <>
      <div className="pt-2.5">
        <ul role="list" className="divide-y divide-gray-200">
          {ownerLicense.map((img, index) => (
            <li key={img.id} className="px-1 py-1 sm:px-0">
              <div className="w-full px-3 py-1.5 rounded-md bg-slate-200 space-y-3">
                <div className="flex justify-between">
                  <div className="w-[70%] flex justify-start items-center space-x-2">
                    <div
                      className="text-[#5E62FF] text-[24px] cursor-pointer"
                      onClick={() => showImage(img.photo)}
                    >
                      {img.type.match(/image.*/i) ? (
                        <FaRegFileImage />
                      ) : (
                        <FaRegFile />
                      )}
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
    </>
  );
};

export default ImageList;
