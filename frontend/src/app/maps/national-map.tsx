"use client";

import { ConstituencyMiniBoundary, PartyTerritory, get } from "@/api";
import { type LayerKey, Map, useMap } from "@/components/map";
import React, {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { usePagination } from "@/components/paginated/pagination";
import { usePassiveGeoLocation } from "@/components/map/geolocation";
import { GeoLocation, UkParliamentLocation } from "@/components/map/geography";
import Loading from "@/components/loading";
import { MapRenderer } from "@/components/map/map";
import { SelectedConstituenciesInfo } from "@/app/maps/components/selected";
import { PartyTerritoryKey } from "./components/party-filter";
import { classes } from "@/util/transforms";
import PageLayout from "@/components/page";

export default function NationalMap() {
  const userLocation: GeoLocation | undefined =
    usePassiveGeoLocation(UkParliamentLocation);

  if (!userLocation) return <Loading />;

  return <NationalMapWithLocation userLocation={userLocation} />;
}

const NationalMapWithLocation = ({
  userLocation,
}: {
  userLocation: GeoLocation;
}) => {
  const [territories, setTerritories] = useState<PartyTerritory[]>();
  const [focus, setFocus] = useState<LayerKey[]>([]);
  const isFocusLocked = useRef<boolean>(false);
  const constituencies = usePagination(
    "/api/maps/constituencies/",
    userLocation,
  );
  const focussedConstituencies = useMemo(
    () =>
      constituencies.items.filter((it) => focus.includes(it.parliamentdotuk)),
    [focus, constituencies.items],
  );

  const map = useMap({
    provider: null,
    viewOptions: {
      minResolution: 75,
    },
    events: {
      onHover: (id) => {
        if (!isFocusLocked.current) {
          setFocus(id === undefined ? [] : [id]);
        }
      },
      onSelect: (ids) => onSelectFeatures(ids),
    },
  });

  const onSelectFeatures = useCallback((layers: LayerKey[]) => {
    isFocusLocked.current = layers.length > 0;
    setFocus(layers);
  }, []);

  const filterByParty = useCallback(
    (partyId: number) => {
      map?.selectFeatures("partyId", partyId, { fit: true });
      onSelectFeatures(
        constituencies.items
          .filter((it) => it.mp?.party?.parliamentdotuk === partyId)
          .map((it) => it.parliamentdotuk),
      );
    },
    [map, constituencies.items, onSelectFeatures],
  );

  useEffect(() => {
    get("/api/maps/parties/").then((it) => {
      setTerritories(it.data);
    });
  }, []);

  useEffect(() => {
    if (!map) return;
    if (!territories) return;
    addPartyTerritories(territories, map);
  }, [map, territories]);

  useEffect(() => {
    if (!map) return;
    addConstituencyBoundaries(constituencies.items, map);
    constituencies.loadNext?.();
  }, [map, constituencies.items, constituencies.loadNext]);

  return (
    <PageLayout layout="CenteredFeed">
      <div className="relative w-full">
        <Map map={map} className="card aspect-square max-h-[80vh] w-full" />

        <PartyTerritoryKey
          parties={territories}
          className={classes(
            "row gap-2 overflow-auto",
            "sm:pointer-events-none sm:absolute sm:top-0 sm:left-0 sm:block",
            "[&>*]:shrink-0",
          )}
          onClickParty={filterByParty}
        />

        <SelectedConstituenciesInfo
          constituencies={focussedConstituencies}
          className="sm:absolute sm:right-0 sm:bottom-0 sm:m-2"
        />
      </div>
    </PageLayout>
  );
};

const addPartyTerritories = (
  territories: PartyTerritory[],
  map: MapRenderer,
) => {
  territories?.forEach((party) => {
    const boundary = party.territory;
    if (boundary) {
      map?.addOverlay({
        layerKey: party.parliamentdotuk,
        geoJson: JSON.parse(boundary),
        style: {
          stroke: false,
          fill: {
            color: party.theme?.primary,
          },
        },
      });
    }
  });
};

const addConstituencyBoundaries = (
  constituencies: ConstituencyMiniBoundary[],
  map: MapRenderer,
) => {
  constituencies.forEach((constituency) => {
    const boundary = constituency.boundary;
    if (boundary) {
      map?.addOverlay({
        layerKey: constituency.parliamentdotuk,
        geoJson: JSON.parse(boundary),
        properties: {
          color: constituency.mp?.party?.theme?.primary,
          selectable: true,
          partyId: constituency.mp?.party?.parliamentdotuk,
        },
        style: {
          stroke: true,
          fill: {
            color: "transparent",
            opacityPercent: 100,
          },
        },
        zIndex: 10,
      });
    }
  });
};
