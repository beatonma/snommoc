"use client";

import { DivPropsNoChildren } from "@/types/react";

import { Map, useMap } from "@/components/map";
import { useEffect } from "react";
import { Constituency } from "@/api";
import { rgb } from "@/components/themed/party";

type ConstituencyMapProps = {
  constituency: Constituency;
} & Omit<DivPropsNoChildren, "id">;
export const ConstituencyMap = (props: ConstituencyMapProps) => {
  const { constituency, ...rest } = props;
  const map = useMap();

  useEffect(() => {
    const geoJson = constituency.boundary
      ? JSON.parse(constituency.boundary)
      : null;
    if (map && geoJson) {
      map.addOverlay({
        layerKey: constituency.parliamentdotuk,
        geoJson: geoJson,
        color: rgb(constituency.mp?.party?.theme?.primary),
      });
    }
  }, [map, constituency]);

  return <Map map={map} {...rest} />;
};
