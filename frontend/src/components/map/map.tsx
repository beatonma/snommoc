"use client";
import { useEffect, useId, useRef, useState } from "react";
import { Feature, Map as OlMap, MapBrowserEvent, View } from "ol";

import VectorSource from "ol/source/Vector";
import { type GeoJSON } from "geojson";
import { default as OlGeoJSON } from "ol/format/GeoJSON.js";
import TileLayer from "ol/layer/Tile";
import { ImageTile, OSM, TileImage } from "ol/source";
import VectorLayer from "ol/layer/Vector";
import { Fill, Icon, Stroke, Style } from "ol/style";
import { useGeographic } from "ol/proj";
import { RemoteContent } from "@/components/remote-content";
import { Control } from "ol/control";
import { DivProps } from "@/types/react";
import { ViewOptions } from "ol/View";
import { get as getProjection } from "ol/proj";
import { addClass } from "@/util/transforms";
import { FeatureLike } from "ol/Feature";
import { Nullish } from "@/types/common";
import {
  combineExtents,
  Extents,
  padExtents,
  UkSquareExtents,
} from "./geography";
import { Point } from "ol/geom";
import { useGeoLocationPrompt } from "./geolocation";
import { Select } from "ol/interaction";
import { click } from "ol/events/condition";

const MapProjectionCode = "EPSG:27700"; // British National Grid
const UserLocationMarkerId = "user_location";

export type LayerKey = string | number;
interface GeoJsonLayer {
  layerKey: LayerKey;
  geoJson: GeoJSON;
  style?: StyleOptions;
  properties?: FeatureProperties;
  replace?: boolean;
  zIndex?: number;
}
interface StyleOptions {
  stroke?: boolean;
  fill?: {
    color?: string;
    opacityPercent?: number;
  };
}

type LayerEventHandler = ((id: LayerKey | undefined) => void) | Nullish;
type OnFeatureHover = LayerEventHandler;
type OnFeatureClick = LayerEventHandler;
interface MapOptions {
  provider?: MapProvider | Nullish;
  viewOptions?: ViewOptions;
  events?: MapEventHandlers;
  fitToExtents?: boolean;
}
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

interface MapProvider {
  source: () => ImageTile | TileImage;
  attribution: () => HTMLElement;
}
export const MapProvider = {
  OSM: {
    source: () => new OSM(),
    attribution: () => {
      const element = document.createElement("div");
      element.innerHTML = "© OpenStreetMap contributors";
      element.className =
        "text-sm m-1 px-2 py-1 text-black bg-white/75 w-fit rounded-md absolute";
      return element;
    },
  } as MapProvider,
};

interface MapEventHandlers {
  onHover?: OnFeatureHover;
  onClick?: OnFeatureClick;
}
class MapRenderer {
  #map: OlMap;
  #extents: Extents | null = null;
  #layers: Record<LayerKey, VectorLayer> = {};
  #eventHandlers: MapEventHandlers | Nullish;
  #fitToExtents: boolean;

  constructor(options?: MapOptions) {
    this.#eventHandlers = options?.events;
    this.#map = this.#initializeMap(options);
    this.#fitToExtents = options?.fitToExtents || false;

    if (!this.#fitToExtents) {
      // Show fully zoomed-out map.
      this.#map.getView().fit(options?.viewOptions?.extent ?? UkSquareExtents);
    }
  }

  setEventHandlers(handlers: MapEventHandlers | Nullish) {
    this.#eventHandlers = handlers;
  }

  setContainer(containerId: string) {
    this.#map.setTarget(containerId);
  }

  addOverlay({
    layerKey,
    geoJson,
    style,
    properties,
    zIndex,
    replace = false,
  }: GeoJsonLayer) {
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
        if (properties) {
          let key: FeatureProperty;
          for (key in properties) {
            setProperty(feature, key, properties[key]);
          }
        }
        return feature;
      }),
    });
    const layer = new VectorLayer({
      source: source,
      style: getStyle(style),
      zIndex: zIndex,
    });

    this.#layers[layerKey] = layer;
    this.#map.addLayer(layer);
    if (this.#fitToExtents) {
      this.#addExtents(source.getExtent() as Extents);
    }
  }

  addUserLocation({
    longitude,
    latitude,
  }: {
    longitude: number;
    latitude: number;
  }) {
    const marker = new Feature({
      geometry: new Point([longitude, latitude]),
    });
    marker.setId(UserLocationMarkerId);

    const layer = new VectorLayer({
      source: new VectorSource({
        features: [marker],
      }),
      style: new Style({
        image: new Icon({
          src: "/user-location.svg",
          anchor: [0.5, 1],
          color: "white",
        }),
      }),
      zIndex: 1000,
    });
    this.#map.addLayer(layer);
  }

  /**
   * Update the map view to show the full extents of all added layers.
   */
  #addExtents(extents: Extents) {
    const before: Extents = [...(this.#extents ?? extents)];
    const expanded: Extents = combineExtents(before, extents);
    this.#extents = expanded;
    this.#map.getView().fit(padExtents(expanded, 0.1), { duration: 500 });
  }

  #initializeMap(options: MapOptions | undefined): OlMap {
    // eslint-disable-next-line react-hooks/rules-of-hooks
    useGeographic(); // Not a React hook

    const map = new OlMap({
      view: new View({
        extent: UkSquareExtents,
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
      console.debug(
        `Clicked coordinate lat=${ev.coordinate[1]?.toFixed(3)}, long=${ev.coordinate[0]?.toFixed(3)}`,
      );
      withFeature(map, ev, this.#eventHandlers?.onClick);
    });

    const selectClick = new Select({
      style: (feature) => {
        const color = getProperty(feature, "color");
        return new Style({
          fill: new Fill({
            color: `color-mix(in srgb, ${color} 90%, transparent)`,
          }),
          stroke: new Stroke({
            color: `color-mix(in srgb, black 90%, transparent)`,
            width: 1.5,
          }),
        });
      },
      condition: click,
      filter: (feature) => getProperty(feature, "selectable") === true,
    });
    map.addInteraction(selectClick);

    return map;
  }
}

type MapProps = {
  map: MapRenderer | undefined;
} & Omit<DivProps, "id">;
const MapView = (props: MapProps) => {
  const { map, children, ...rest } = addClass(props, "relative");
  const id = useId();
  const ref = useRef<HTMLDivElement>(null);
  const { geoLocation, GeoLocationPromptButton: GeoLocationPromptButton } =
    useGeoLocationPrompt();

  useEffect(() => {
    map?.setContainer(id);
  }, [map, id]);

  useEffect(() => {
    if (geoLocation) {
      map?.addUserLocation(geoLocation);
    }
  }, [map, geoLocation]);

  return (
    <div id={id} ref={ref} {...rest}>
      <GeoLocationPromptButton className="absolute top-0 right-0 m-2" />
      {children}
    </div>
  );
};

const getStyle = (options?: StyleOptions) => {
  const opts = options ?? ({ stroke: true } as StyleOptions);
  return new Style({
    stroke: opts.stroke
      ? new Stroke({
          color: `color-mix(in srgb, black 90%, transparent)`,
          width: 0.25,
        })
      : undefined,
    fill: opts?.fill?.color
      ? new Fill({
          color: `color-mix(in srgb, ${opts.fill.color} ${opts.fill.opacityPercent ?? 50}%, transparent)`,
        })
      : undefined,
  });
};

/** Feature functions */
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

interface FeatureProperties {
  color?: string | undefined;
  selectable?: boolean;
}
type FeatureProperty = keyof FeatureProperties;
const setProperty = <K extends keyof FeatureProperties>(
  feature: Feature,
  key: K,
  value: FeatureProperties[K],
) => feature.set(key, value);

const getProperty = <K extends keyof FeatureProperties>(
  feature: FeatureLike,
  key: K,
): FeatureProperties[K] => feature.get(key);

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
