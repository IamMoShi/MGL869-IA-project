import {Dialog, DialogBackdrop, DialogPanel, RadioGroup} from '@headlessui/react'

import {XMarkIcon} from '@heroicons/react/24/outline'
import {useState} from "react";
import {LoadSpinner} from "./LoadSpinner.js";


export default function ImageDialog({open, setOpen, category, image, handleDownload, handleCategoryChange, isLoading, handleDelete}) {
    const [categories, setCategories] = useState(category);
    const selected = categories.find((c) => c.isActive);


    const handleChange = (selectedCategory) => {
        const updated = categories.map((c) => ({
            ...c,
            isActive: c.name === selectedCategory.name,
        }));
        setCategories(updated);

        handleCategoryChange(updated.find((c) => c.isActive).id);
    };


    function classNames(...classes) {
        return classes.filter(Boolean).join(' ')
    }

    return (
        <Dialog open={open} onClose={setOpen} className="relative z-10">
            <DialogBackdrop
                transition
                className="fixed inset-0 bg-gray-500/75 transition-opacity data-closed:opacity-0 data-enter:duration-300 data-enter:ease-out data-leave:duration-200 data-leave:ease-in"
            />

            <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
                <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
                    <DialogPanel
                        transition
                        className="relative transform overflow-hidden rounded-lg bg-white px-4 pt-5 pb-4 text-left shadow-xl transition-all data-closed:translate-y-4 data-closed:opacity-0 data-enter:duration-300 data-enter:ease-out data-leave:duration-200 data-leave:ease-in sm:my-8 sm:w-full sm:max-w-lg sm:p-6 data-closed:sm:translate-y-0 data-closed:sm:scale-95"
                    >
                        <div className="absolute top-0 right-0 hidden pt-4 pr-4 sm:block">
                            <button
                                type="button"
                                onClick={() => setOpen(false)}
                                className="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:outline-hidden"
                            >
                                <span className="sr-only">Close</span>
                                <XMarkIcon aria-hidden="true" className="size-6"/>
                            </button>
                        </div>
                        <div className="sm:flex sm:items-start">
                            <div className="text-center">
                                <div className="h-full w-116 overflow-y-auto">
                                    <div className="space-y-6">
                                        <div>
                                            <img
                                                alt=""
                                                src={image}
                                                className="block aspect-10/7 w-full rounded-lg object-cover"
                                            />
                                        </div>
                                        <div>
                                            <h3 className="font-medium text-gray-900">Categories</h3>
                                            {
                                                isLoading ? <LoadSpinner/>: <RadioGroup
                                                    value={selected}
                                                    onChange={handleChange}
                                                    // className="mt-2 grid grid-cols-6 gap-2"
                                                    className="mt-4 grid grid-cols-3 gap-3"
                                                >
                                                    {categories.map((category) => (
                                                        <RadioGroup.Option
                                                            key={category.name}
                                                            value={category}
                                                            className={() =>
                                                                classNames(
                                                                    category.isActive ? 'cursor-pointer focus:outline-hidden' : 'opacity-25',
                                                                    'flex items-center justify-center rounded-md border border-gray-600 bg-white px-5 py-6 text-sm font-medium text-gray-900 uppercase hover:bg-gray-50 data-checked:border-transparent data-checked:bg-indigo-600 data-checked:text-white data-checked:hover:bg-indigo-700 data-focus:ring-2 data-focus:ring-indigo-500 data-focus:ring-offset-2 sm:flex-1',
                                                                )

                                                            }
                                                        >
                                                            {category.name}
                                                        </RadioGroup.Option>
                                                    ))}
                                                </RadioGroup>
                                            }

                                        </div>
                                        <div className="flex pt-8">
                                            <button
                                                onClick={handleDownload}
                                                type="button"
                                                className="flex-1 rounded-md bg-indigo-600 px-4 py-3 text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                                            >
                                                Download
                                            </button>
                                            <button
                                                onClick={()=>handleDelete(image)}
                                                type="button"
                                                className="ml-3 flex-1 rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-xs ring-1 ring-gray-300 ring-inset hover:bg-gray-50"
                                            >
                                                Delete
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </DialogPanel>
                </div>
            </div>
        </Dialog>
    )
}
