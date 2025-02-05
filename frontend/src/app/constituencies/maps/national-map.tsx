"use client";

import { getNationalConstituencyMaps } from "@/api";
import { Map, useMap } from "@/components/map";
import { useEffect } from "react";
import { rgb } from "@/components/themed/party";
import { GeoJSON } from "geojson";
import { usePagination } from "@/components/paginated/pagination";

export default function NationalMap() {
  const pagination = usePagination(getNationalConstituencyMaps);

  const map = useMap();

  useEffect(() => {
    pagination.items.forEach((constituency) => {
      const boundary = constituency.boundary;
      if (boundary) {
        map?.addOverlay({
          key: constituency.parliamentdotuk,
          geoJson: boundary as unknown as GeoJSON,
          color: rgb(constituency.mp?.party?.theme?.primary),
        });
      }
    });
    // pagination.loadNext?.(); TODO enable
  }, [map, pagination.items, pagination.loadNext]);

  return (
    <Map map={map} className="bg-primary aspect-square max-h-[80vh] w-full" />
  );
}
