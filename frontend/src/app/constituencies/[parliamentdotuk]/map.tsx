"use client";
import { useEffect, useId, useRef } from "react";
import { Map, View } from "ol";
import { DivPropsNoChildren } from "@/types/react";

import VectorSource from "ol/source/Vector";
import { type GeoJSON } from "geojson";
import { default as OlGeoJSON } from "ol/format/GeoJSON.js";
import TileLayer from "ol/layer/Tile";
import { OSM } from "ol/source";
import VectorLayer from "ol/layer/Vector";
import { Fill, Stroke, Style } from "ol/style";
import { useGeographic } from "ol/proj";
import { ViewOptions } from "ol/View";
import { RemoteContent } from "@/components/remote-content";
import { Control } from "ol/control";

export const ConstituencyMap = (
  props: ConstituencyMapProps & Omit<DivPropsNoChildren, "id">,
) => (
  <RemoteContent
    provider="openstreetmap.org"
    content={() => <RemoteConstituencyMap {...props} />}
  />
);

interface ConstituencyMapProps {
  geojson: GeoJSON | undefined;
}
const RemoteConstituencyMap = (
  props: ConstituencyMapProps & Omit<DivPropsNoChildren, "id">,
) => {
  const { geojson, ...rest } = props;
  const id = useId();
  const isInitialized = useRef(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!geojson) return;
    if (isInitialized.current) return;

    const container = ref.current;
    if (!container) return;

    // eslint-disable-next-line react-hooks/rules-of-hooks
    useGeographic(); // Not a React hook

    const overlaySource = new VectorSource({
      features: new OlGeoJSON().readFeatures(geojson),
    });
    const overlayLayer = new VectorLayer({
      source: overlaySource,
      style: themedStyle(container),
    });

    const map = new Map({
      target: id,
      view: new View(getViewOptions(overlaySource)),
      layers: [new TileLayer({ source: new OSM() }), overlayLayer],
      controls: [
        new Control({
          element: OpenStreetMapOverlay(),
        }),
      ],
    });

    map.getView().fit(overlaySource.getExtent());
    isInitialized.current = true;
  }, [geojson, id]);

  if (!geojson) return null;
  return <div id={id} ref={ref} {...rest} />;
};

type Point = [number, number];
type Extents = [number, number, number, number];
const UkCenter: Point = [-2.89479, 54.093409];
const UkExtents: Extents = [-11.5, 49.5, 2.5, 61.5];

const getViewOptions = (source: VectorSource): ViewOptions => {
  try {
    const extents = source.getExtent() as Extents;
    const [minX, minY, maxX, maxY] = extents;

    const center = [(minX + maxX) / 2, (minY + maxY) / 2];

    return {
      extent: UkExtents,
      center: center,
      zoom: 1,
    };
  } catch {
    return {
      extent: UkExtents,
      center: UkCenter,
      zoom: 1,
    };
  }
};

/**
 * Use current value of --primary CSS variable to style the overlay.
 */
const themedStyle = (element: HTMLElement) => {
  const themePrimary = element.computedStyleMap().get("--primary")?.toString();

  if (!themePrimary) {
    return buildStyle();
  }

  const match = /#([a-fA-F\d]{6})([a-fA-F\d]{2})?/.exec(themePrimary);
  if (match) {
    const opaque = match[1];
    return buildStyle(opaque);
  }
  console.warn(
    `Unable to construct map style from unsupported color format: '${themePrimary}'`,
  );
  return buildStyle();
};

const buildStyle = (opaqueColor?: string | undefined) => {
  const color = opaqueColor ?? "000000";
  return new Style({
    stroke: new Stroke({
      color: `#${color}fa`,
      width: 1,
    }),
    fill: new Fill({
      color: `#${color}28`,
    }),
  });
};

const OpenStreetMapOverlay = () => {
  const element = document.createElement("div");
  element.innerHTML = "© OpenStreetMap contributors";
  element.className =
    "text-sm m-1 px-2 py-1 text-black bg-white/75 w-fit rounded-md right-0 bottom-0";
  return element;
};
