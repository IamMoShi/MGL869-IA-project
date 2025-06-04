export const CATEGORY_MAP = {
    buildings: 0,
    forest: 1,
    glacier: 2,
    mountain: 3,
    sea: 4,
    street: 5,
};


// Set error status and result body if error occurs
export function setErrorStatus(
    status: number,
    resultBody: { status: string; message: string },
) {
    status = 500;
    resultBody = {
        status: "fail",
        message: "Upload error",
    };
    return { status, resultBody };
}