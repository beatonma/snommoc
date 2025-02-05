"use client";
import { useEffect, useId, useRef, useState } from "react";
import { Map as OlMap, View } from "ol";

import VectorSource from "ol/source/Vector";
import { type GeoJSON } from "geojson";
import { default as OlGeoJSON } from "ol/format/GeoJSON.js";
import TileLayer from "ol/layer/Tile";
import { OSM } from "ol/source";
import VectorLayer from "ol/layer/Vector";
import { Fill, Stroke, Style } from "ol/style";
import { useGeographic } from "ol/proj";
import { RemoteContent } from "@/components/remote-content";
import { Control } from "ol/control";
import { DivPropsNoChildren } from "@/types/react";
import Loading from "@/components/loading";

// A rect with the min/max boundaries of a feature: [minX, minY, maxX, maxY]
type Extents = [number, number, number, number];
const UkExtents: Extents = [-11.5, 49.5, 2.5, 61.5];

type LayerKey = string | number;
export interface GeoJsonLayer {
  key: LayerKey;
  geoJson: GeoJSON;
  color?: string;
  replace?: boolean;
}

class MapRenderer {
  map: OlMap;
  extents: Extents | null = null;
  layers: Record<LayerKey, VectorLayer> = {};

  constructor() {
    // eslint-disable-next-line react-hooks/rules-of-hooks
    useGeographic(); // Not a React hook
    this.map = new OlMap({
      layers: [new TileLayer({ source: new OSM() })],
      controls: [
        new Control({
          element: OpenStreetMapOverlay(),
        }),
      ],
      view: new View({
        extent: UkExtents,
      }),
    });
  }

  setContainer(containerId: string) {
    this.map.setTarget(containerId);
  }

  addOverlay({ key, geoJson, color, replace = false }: GeoJsonLayer) {
    if (key in this.layers) {
      if (!replace) return; // Layer already exists and should not be replaced.
      const existing = this.layers[key];
      if (existing) {
        this.map.removeLayer(existing);
      }
      delete this.layers[key];
    }

    const source = new VectorSource({
      features: new OlGeoJSON().readFeatures(geoJson),
    });
    const layer = new VectorLayer({
      source: source,
      style: getStyle(color),
    });

    this.layers[key] = layer;
    this.map.addLayer(layer);
    this.addExtents(source.getExtent() as Extents);
  }

  /**
   * Update the map view to show the full extents of all added layers.
   */
  addExtents(extents: Extents) {
    const before: Extents = [...(this.extents ?? extents)];
    const expanded: Extents = [
      Math.min(before[0], extents[0]),
      Math.min(before[1], extents[1]),
      Math.max(before[2], extents[2]),
      Math.max(before[3], extents[3]),
    ];
    this.extents = expanded;
    this.map.getView().fit(expanded, { duration: 500 });
  }
}
const getStyle = (color: string | undefined) =>
  new Style({
    stroke: new Stroke({
      color: `color-mix(in srgb, ${color ?? "var(--primary)"} 90%, transparent)`,
      width: 1,
    }),
    fill: new Fill({
      color: `color-mix(in srgb, ${color ?? "var(--primary)"} 25%, transparent)`,
    }),
  });

export const useMap = () => {
  const [map, setMap] = useState<MapRenderer>();
  const initialized = useRef(false);

  useEffect(() => {
    if (initialized.current) return;

    initialized.current = true;
    setMap(new MapRenderer());
  }, [map]);

  return map;
};

export const Map = (props: MapProps) => {
  return (
    <RemoteContent
      provider="openstreetmap.org"
      content={() => <MapView {...props} />}
    />
  );
};

export type MapProps = {
  map: MapRenderer | undefined;
} & Omit<DivPropsNoChildren, "id">;
const MapView = (props: MapProps) => {
  const { map, ...rest } = props;
  const id = useId();
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    map?.setContainer(id);
  }, [map, id]);

  if (!props.map) return <Loading />;

  return <div id={id} ref={ref} {...rest} />;
};

const OpenStreetMapOverlay = () => {
  const element = document.createElement("div");
  element.innerHTML = "© OpenStreetMap contributors";
  element.className =
    "text-sm m-1 px-2 py-1 text-black bg-white/75 w-fit rounded-md";
  return element;
};
