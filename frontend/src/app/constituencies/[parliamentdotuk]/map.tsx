"use client";

import { DivPropsNoChildren } from "@/types/react";

import { GeoJsonLayer, Map, useMap } from "@/components/map";
import { useEffect } from "react";
import { GeoJSON } from "geojson";

interface OptionalGeoJsonLayer extends Pick<GeoJsonLayer, "key" | "color"> {
  geoJson: GeoJSON | undefined;
}

type ConstituencyMapProps = OptionalGeoJsonLayer &
  Omit<DivPropsNoChildren, "id">;
export const ConstituencyMap = (props: ConstituencyMapProps) => {
  const { key, geoJson, color, ...rest } = props;

  const map = useMap();

  useEffect(() => {
    if (map && geoJson) {
      map.addOverlay({ key: key, geoJson: geoJson, color: color });
    }
  }, [map, key, geoJson, color]);

  return <Map map={map} {...rest} />;
};
