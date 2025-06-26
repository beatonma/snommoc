"use client";

import { useEffect } from "react";
import { Constituency } from "@/api";
import { Map, useMap } from "@/components/map";
import { DivPropsNoChildren } from "@/types/react";

type ConstituencyMapProps = DivPropsNoChildren<
  {
    constituency: Constituency;
  },
  "id"
>;
export const ConstituencyMap = (props: ConstituencyMapProps) => {
  const { constituency, ...rest } = props;
  const map = useMap({ fitToExtents: true });

  useEffect(() => {
    const geoJson = constituency.boundary
      ? JSON.parse(constituency.boundary)
      : null;
    if (map && geoJson) {
      map.addOverlay({
        layerKey: constituency.parliamentdotuk,
        geoJson: geoJson,
        style: {
          stroke: true,
          cssColor: `color-mix(in srgb, ${constituency.mp?.party?.theme?.primary ?? "transparent"} 30%, transparent)`,
        },
      });
    }
  }, [map, constituency]);

  return <Map map={map} {...rest} />;
};
