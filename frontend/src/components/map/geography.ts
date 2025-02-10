// A rect with the min/max boundaries of a feature: [minX, minY, maxX, maxY]
export type Extents = [number, number, number, number];

export const combineExtents = (a: Extents, b: Extents): Extents => [
  Math.min(a[0], b[0]),
  Math.min(a[1], b[1]),
  Math.max(a[2], b[2]),
  Math.max(a[3], b[3]),
];
export const padExtents = (
  extents: Extents,
  paddingFactor: number = 0.1,
): Extents => {
  const widthPadding = (extents[2] - extents[0]) * paddingFactor;
  const heightPadding = (extents[3] - extents[1]) * paddingFactor;
  return [
    extents[0] - widthPadding,
    extents[1] - heightPadding,
    extents[2] + widthPadding,
    extents[3] + heightPadding,
  ];
};

const degreesToDecimal = (degrees: number, minutes: number): number =>
  degrees + minutes / 60;

const UkNorth = degreesToDecimal(60, 51);
const UkSouth = degreesToDecimal(49, 51);
const UkWest = degreesToDecimal(-13, 41);
const UkEast = degreesToDecimal(1, 46);

export const UkLimitExtents: Extents = [UkWest, UkSouth, UkEast, UkNorth];
export const UkSquareExtents: Extents = padExtents([
  -16.51,
  UkSouth,
  5.94,
  UkNorth,
]);
