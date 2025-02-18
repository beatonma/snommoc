// A rect with the min/max boundaries of a feature: [minX, minY, maxX, maxY]
import { Feature } from "ol";
import { LinearRing, Polygon } from "ol/geom";

export type Extents = [number, number, number, number];

export interface GeoLocation {
  latitude: number;
  longitude: number;
}

export const combineExtents = (a: Extents, b: Extents): Extents => [
  Math.min(a[0], b[0]),
  Math.min(a[1], b[1]),
  Math.max(a[2], b[2]),
  Math.max(a[3], b[3]),
];

export const mutateCombineExtents = (
  receiver: Extents,
  other: Extents,
): void => {
  if (isNaN(receiver[0])) {
    receiver[0] = other[0];
    receiver[1] = other[1];
    receiver[2] = other[2];
    receiver[3] = other[3];
    return;
  }

  receiver[0] = Math.min(receiver[0], other[0]);
  receiver[1] = Math.min(receiver[1], other[1]);
  receiver[2] = Math.max(receiver[2], other[2]);
  receiver[3] = Math.max(receiver[3], other[3]);
};

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

export const UkParliamentLocation: GeoLocation = {
  latitude: 51.5,
  longitude: -0.13,
};

export const asFeature = (extents: Extents): Feature =>
  new Feature({
    geometry: new Polygon([
      new LinearRing([
        [extents[0], extents[1]],
        [extents[0], extents[3]],
        [extents[2], extents[3]],
        [extents[2], extents[1]],
        [extents[0], extents[1]],
      ]).getCoordinates(),
    ]),
  });
