import Swal from "sweetalert2";


export const CATEGORY_MAP = {
    buildings: 0,
    forest: 1,
    glacier: 2,
    mountain: 3,
    sea: 4,
    street: 5,
};

export const ID_TO_CATEGORY = Object.fromEntries(
    Object.entries(CATEGORY_MAP).map(([key, value]) => [value, key])
);


/**
 * @param {any} ID_ACTIVE
 */
export function getCategoryStatus(ID_ACTIVE: unknown) {
    return Object.entries(CATEGORY_MAP).map(([name, id]) => ({
        id,
        name,
        isActive: id === ID_ACTIVE
    }));
}


export const TopNotification = Swal.mixin({
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