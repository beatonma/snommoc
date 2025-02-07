"use client";
import { useEffect, useId, useRef, useState } from "react";
import { Feature, Map as OlMap, MapBrowserEvent, View } from "ol";

import VectorSource from "ol/source/Vector";
import { type GeoJSON } from "geojson";
import { default as OlGeoJSON } from "ol/format/GeoJSON.js";
import TileLayer from "ol/layer/Tile";
import { ImageTile, OSM, TileImage } from "ol/source";
import VectorLayer from "ol/layer/Vector";
import { Fill, Stroke, Style } from "ol/style";
import { useGeographic } from "ol/proj";
import { RemoteContent } from "@/components/remote-content";
import { Control } from "ol/control";
import { DivProps } from "@/types/react";
import { ViewOptions } from "ol/View";
import { get as getProjection } from "ol/proj";
import { addClass } from "@/util/transforms";
import { FeatureLike } from "ol/Feature";
import { Nullish } from "@/types/common";

// A rect with the min/max boundaries of a feature: [minX, minY, maxX, maxY]
type Extents = [number, number, number, number];

// An approximation of a square (relative to the projection), so that a fully
// zoomed-out map is able to show the full UK when the map is rendered in a
// square element.
const UkExtents: Extents = [-19.5, 49.4, 8.8, 61.2];
const MapProjectionCode = "EPSG:27700"; // British National Grid

export type LayerKey = string | number;
interface GeoJsonLayer {
  layerKey: LayerKey;
  geoJson: GeoJSON;
  color?: string;
  replace?: boolean;
}
type LayerEventHandler = ((id: LayerKey | undefined) => void) | Nullish;
type OnFeatureHover = LayerEventHandler;
type OnFeatureClick = LayerEventHandler;
interface MapOptions {
  provider?: MapProvider | Nullish;
  viewOptions?: ViewOptions;
  events?: MapEventHandlers;
}

interface MapProvider {
  source: () => ImageTile | TileImage;
  attribution: () => HTMLElement;
}

interface MapEventHandlers {
  onHover?: OnFeatureHover;
  onClick?: OnFeatureClick;
}
class MapRenderer {
  #map: OlMap;
  #extents: Extents | null = null;
  #layers: Record<LayerKey, VectorLayer> = {};
  #eventHandlers: MapEventHandlers | Nullish;

  constructor(options?: MapOptions) {
    this.#eventHandlers = options?.events;
    this.#map = this.#initializeMap(options);
  }

  setEventHandlers(handlers: MapEventHandlers | Nullish) {
    this.#eventHandlers = handlers;
  }

  setContainer(containerId: string) {
    this.#map.setTarget(containerId);
  }

  addOverlay({ layerKey, geoJson, color, replace = false }: GeoJsonLayer) {
    if (layerKey in this.#layers) {
      if (!replace) return; // Layer already exists and should not be replaced.
      const existing = this.#layers[layerKey];
      if (existing) {
        this.#map.removeLayer(existing);
      }
      delete this.#layers[layerKey];
    }

    const source = new VectorSource({
      features: new OlGeoJSON().readFeatures(geoJson).map((feature, index) => {
        setId(feature, layerKey, index);
        return feature;
      }),
    });
    const layer = new VectorLayer({
      source: source,
      style: getStyle(color),
    });

    this.#layers[layerKey] = layer;
    this.#map.addLayer(layer);
    this.#addExtents(source.getExtent() as Extents);
  }

  /**
   * Update the map view to show the full extents of all added layers.
   */
  #addExtents(extents: Extents) {
    const before: Extents = [...(this.#extents ?? extents)];
    const expanded: Extents = [
      Math.min(before[0], extents[0]),
      Math.min(before[1], extents[1]),
      Math.max(before[2], extents[2]),
      Math.max(before[3], extents[3]),
    ];
    this.#extents = expanded;
    this.#map.getView().fit(expanded, { duration: 500 });
  }

  #initializeMap(options: MapOptions | undefined): OlMap {
    // eslint-disable-next-line react-hooks/rules-of-hooks
    useGeographic(); // Not a React hook

    const map = new OlMap({
      view: new View({
        extent: UkExtents,
        projection: getProjection(MapProjectionCode) ?? undefined,
        ...(options?.viewOptions ?? {}),
      }),
      controls: [],
    });

    const provider =
      options?.provider === null
        ? null
        : (options?.provider ?? MapProvider.OSM);
    if (provider) {
      map.addLayer(new TileLayer({ source: provider.source() }));
      map.addControl(new Control({ element: provider.attribution() }));
    }

    map.on("pointermove", (ev) => {
      if (ev.dragging) {
        this.#eventHandlers?.onHover?.(undefined);
        return;
      }

      withFeature(map, ev, this.#eventHandlers?.onHover);
    });

    map.on("singleclick", (ev) => {
      withFeature(map, ev, this.#eventHandlers?.onClick);
    });

    return map;
  }
}
const getStyle = (color: string | undefined) =>
  new Style({
    stroke: new Stroke({
      color: `color-mix(in srgb, black 90%, transparent)`,
      width: 1,
    }),
    fill: new Fill({
      color: `color-mix(in srgb, ${color ?? "var(--primary)"} 50%, transparent)`,
    }),
  });

export const useMap = (options?: MapOptions) => {
  const [map, setMap] = useState<MapRenderer>();
  const initialized = useRef(false);

  useEffect(() => {
    if (initialized.current) return;

    initialized.current = true;
    setMap(new MapRenderer(options));
  }, []);

  useEffect(() => {
    map?.setEventHandlers(options?.events);
  }, [map, options?.events]);

  return map;
};

export const Map = (props: MapProps) => (
  <RemoteContent
    provider="openstreetmap.org"
    content={() => <MapView {...props} />}
  />
);

export type MapProps = {
  map: MapRenderer | undefined;
} & Omit<DivProps, "id">;
const MapView = (props: MapProps) => {
  const { map, children, ...rest } = addClass(props, "relative");
  const id = useId();
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    map?.setContainer(id);
  }, [map, id]);

  return (
    <div id={id} ref={ref} {...rest}>
      {children}
    </div>
  );
};

const OpenStreetMapOverlay = () => {
  const element = document.createElement("div");
  element.innerHTML = "© OpenStreetMap contributors";
  element.className =
    "text-sm m-1 px-2 py-1 text-black bg-white/75 w-fit rounded-md absolute";
  return element;
};

const setId = (feature: Feature, layerKey: LayerKey, suffix: number) => {
  feature.setId(`${layerKey}_${suffix}`);
};
const getLayerId = (feature: FeatureLike | undefined): LayerKey | undefined => {
  const id = feature?.getId();
  if (!id) return undefined;
  const asString = (id as string).split("_")[0]!;
  const asInt = parseInt(asString);
  return isNaN(asInt) ? asString : asInt;
};

const withFeature = (
  map: OlMap,
  ev: MapBrowserEvent<any>,
  action: LayerEventHandler,
) => {
  const feature = ev.originalEvent.target?.closest(".ol-control")
    ? undefined
    : map.forEachFeatureAtPixel(ev.pixel, (f) => f);

  const layerId = getLayerId(feature);
  action?.(layerId);
};

export const MapProvider = {
  OSM: {
    source: () => new OSM(),
    attribution: OpenStreetMapOverlay,
  } as MapProvider,
};
