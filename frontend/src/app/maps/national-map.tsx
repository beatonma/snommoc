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
import "./style.css";
import { DivPropsNoChildren } from "@/types/react";
import {
  ConstituencyLink,
  PartyLink,
  PersonLink,
} from "@/components/linked-data";
import { PartyIconBackground } from "@/components/themed/party";
import { onlyIf } from "@/components/optional";
import Row from "@/components/row";

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
  const constituencies = usePagination(
    "/api/maps/constituencies/",
    userLocation,
  );

  const [focus, setFocus] = useState<LayerKey[]>([]);
  const focussedConstituencies = useMemo(
    () =>
      constituencies.items.filter((it) => focus.includes(it.parliamentdotuk)),
    [focus, constituencies.items],
  );

  const [hovered, setHovered] = useState<LayerKey>();
  const hoveredConstituency: ConstituencyMiniBoundary | undefined =
    useMemo(() => {
      if (!hovered) return undefined;
      const result = constituencies.items.find(
        (it) => it.parliamentdotuk === hovered,
      );
      console.log(`${hovered} found ${result}`);
      return result;
    }, [hovered, constituencies.items]);

  const map = useMap({
    provider: null,
    viewOptions: {
      minResolution: 75,
    },
    events: {
      onHover: (id) => setHovered(id),
      onSelect: (ids) => onSelectFeatures(ids),
    },
  });

  const onSelectFeatures = useCallback((layers: LayerKey[]) => {
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
    <div className="map-layout">
      <Map map={map} className="map-layout--map">
        <HoveredConstituency
          constituency={hoveredConstituency}
          className="touch:hidden absolute right-0 bottom-0 z-10 m-2"
        />
      </Map>

      <div className="map-layout--overlays">
        <PartyTerritoryKey
          parties={territories}
          className="map-layout--key"
          onClickParty={filterByParty}
        />

        <SelectedConstituenciesInfo
          constituencies={focussedConstituencies}
          className="map-layout--info"
        />
      </div>
    </div>
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

const HoveredConstituency = (
  props: DivPropsNoChildren & {
    constituency: ConstituencyMiniBoundary | undefined;
  },
) => {
  const { constituency, ...rest } = props;

  return (
    <div {...rest}>
      <PartyIconBackground
        party={constituency?.mp?.party}
        className="chip chip-content"
      >
        <div className="flex flex-col items-end">
          <ConstituencyLink constituency={constituency} className="text-lg" />

          {onlyIf(constituency?.mp, (mp) => (
            <div>
              <PersonLink person={mp} />
              {", "}
              <PartyLink party={mp?.party} />
            </div>
          ))}
        </div>
      </PartyIconBackground>
    </div>
  );
};
