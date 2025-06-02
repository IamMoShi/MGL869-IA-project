"use client";

export default function ImageGridList({ files }) {
  return (
    <div className="mx-auto max-w-2xl px-4 py-8 sm:px-6 sm:py-12 lg:max-w-7xl lg:px-8">
      <h2 className="text-2xl font-bold tracking-tight text-gray-900 mb-1.5">
        Photos
      </h2>
      <ul
        role="list"
        className="grid grid-cols-2 gap-x-4 gap-y-8 sm:grid-cols-3 sm:gap-x-6 lg:grid-cols-4 xl:gap-x-8"
      >
        {files.map((file, index) => (
          <li key={index} className="relative">
            <div className="group overflow-hidden rounded-lg bg-gray-100 focus-within:ring-2 focus-within:ring-indigo-500 focus-within:ring-offset-2 focus-within:ring-offset-gray-100">
              <img
                alt=""
                src={file.source}
                className="pointer-events-none aspect-10/7 object-cover group-hover:opacity-75"
              />
              <button
                type="button"
                className="absolute inset-0 focus:outline-hidden"
              >
                <span className="sr-only">View details for {file.title}</span>
              </button>
            </div>
            <p className="pointer-events-none mt-2 block truncate text-sm font-medium text-gray-900">
              {file.title}
            </p>
            <p className="pointer-events-none block text-sm font-medium text-gray-500">
              {file.size}
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
}
