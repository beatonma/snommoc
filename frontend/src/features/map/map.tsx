"use client";

import { type GeoJSON } from "geojson";
import { Feature, MapBrowserEvent, Map as OlMap, View } from "ol";
import { FeatureLike } from "ol/Feature";
import { ViewOptions } from "ol/View";
import { Control } from "ol/control";
import { click } from "ol/events/condition";
import { default as OlGeoJSON } from "ol/format/GeoJSON.js";
import { Point } from "ol/geom";
import { Select } from "ol/interaction";
import TileLayer from "ol/layer/Tile";
import VectorLayer from "ol/layer/Vector";
import { useGeographic } from "ol/proj";
import { get as getProjection } from "ol/proj";
import { ImageTile, OSM, TileImage } from "ol/source";
import VectorSource from "ol/source/Vector";
import { Fill, Icon, Stroke, Style } from "ol/style";
import { useEffect, useId, useRef, useState } from "react";
import { onlyIf } from "@/components/optional";
import {
  RemoteContent,
  RemoteContentProvider,
} from "@/components/remote-content";
import { Nullish } from "@/types/common";
import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";
import {
  Extents,
  UkSquareExtents,
  asFeature,
  combineExtents,
  mutateCombineExtents,
  padExtents,
} from "./geography";
import { useGeoLocationPrompt } from "./geolocation";

const MapProjectionCode = "EPSG:27700"; // British National Grid
const UserLocationMarkerId = "user_location";
const OpenStreetMapsProvider: RemoteContentProvider = {
  domain: "openstreetmap.org",
  description: "Non-profit map provider",
};

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
  cssColor?: string;
}

type LayerEventHandler = ((id: LayerKey | undefined) => void) | Nullish;
type OnFeatureHover = LayerEventHandler;
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
    provider={OpenStreetMapsProvider}
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
  onSelect?: (layers: LayerKey[]) => void;
}
export class MapRenderer {
  #map: OlMap;
  #extents: Extents | null = null;
  #layers: Record<LayerKey, VectorLayer> = {};
  #eventHandlers: MapEventHandlers | Nullish;
  #fitToExtents: boolean;

  #select: Select;

  constructor(options?: MapOptions) {
    this.#eventHandlers = options?.events;
    this.#map = this.#initializeMap(options);
    this.#select = this.#initializeSelect(this.#map);

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

  selectFeatures<K extends keyof FeatureProperties>(
    property: K,
    value: FeatureProperties[K],
    options?: { fit: boolean },
  ) {
    const fitView = options?.fit === true;
    const extent: Extents = [NaN, NaN, NaN, NaN];

    const selected: Feature[] = this.#map
      .getLayers()
      .getArray()
      .map((layer) => {
        const source = (layer as VectorLayer).getSource();

        return source?.getFeatures()?.filter((feature: Feature) => {
          const result = getProperty(feature, property) === value;
          if (result && fitView) {
            mutateCombineExtents(extent, source.getExtent() as Extents);
          }

          return result;
        });
      })
      .flat();

    if (fitView && selected.length) {
      this.#zoomToExtent(padExtents([...extent], 0.1));
    }

    const features = this.#select.getFeatures();
    features.clear();
    selected.forEach((it) => features.push(it));
  }

  #zoomToExtent(extents: Extents) {
    this.#map.getView().fit(extents, { duration: 500 });
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
    this.#zoomToExtent(padExtents(expanded, 0.1));
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

    return map;
  }

  #initializeSelect(map: OlMap): Select {
    const selectClick = new Select({
      condition: click,
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
      filter: (feature) => getProperty(feature, "selectable") === true,
    });
    selectClick.on("select", (ev) => {
      const selectedLayers = selectClick
        .getFeatures()
        .getArray()
        .map((it) => getLayerId(it))
        .filter((it) => it !== undefined);
      this.#eventHandlers?.onSelect?.(selectedLayers);
    });

    map.addInteraction(selectClick);
    return selectClick;
  }

  #debugShowExtent(extent: Extents) {
    this.#map.addLayer(
      new VectorLayer({
        source: new VectorSource({
          features: [asFeature(extent)],
        }),
        style: new Style({
          stroke: new Stroke({ color: "black", width: 2 }),
          fill: new Fill({ color: "red" }),
        }),
      }),
    );
  }
}

type MapProps = DivProps<
  {
    map: MapRenderer | undefined;
  },
  "id"
>;
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
      <GeoLocationPromptButton className="absolute top-0 right-0 m-2 z-10" />
      {children}
    </div>
  );
};

const getStyle = (options?: StyleOptions) => {
  const opts = options ?? ({ stroke: true } as StyleOptions);
  return new Style({
    stroke: onlyIf(
      opts.stroke,
      new Stroke({
        color: `color-mix(in srgb, black 90%, transparent)`,
        width: 0.25,
      }),
    ),
    fill: onlyIf(opts.cssColor, (css) => new Fill({ color: css })),
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
  selectable?: boolean | undefined;
  partyId?: number | undefined;
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
    : map.forEachFeatureAtPixel(ev.pixel, (f) => {
        if (getProperty(f, "selectable")) {
          return f;
        }
      });

  const layerId = getLayerId(feature);
  action?.(layerId);
};
