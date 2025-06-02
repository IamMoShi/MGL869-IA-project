// src/constants/categoryMap.js
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
