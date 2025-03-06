"use client";

import React, { useCallback, useEffect, useMemo, useState } from "react";
import { ConstituencyMiniBoundary, PartyTerritory, get } from "@/api";
import Loading, { LoadingBar } from "@/components/loading";
import { type LayerKey, Map, useMap } from "@/components/map";
import { GeoLocation, UkParliamentLocation } from "@/components/map/geography";
import { usePassiveGeoLocation } from "@/components/map/geolocation";
import { MapRenderer } from "@/components/map/map";
import {
  ConstituencyLink,
  PartyLink,
  PersonLink,
} from "@/components/models/linked-data";
import { onlyIf } from "@/components/optional";
import { usePagination } from "@/components/paginated/pagination";
import { PartyIconBackground } from "@/components/themed/party";
import { DivPropsNoChildren } from "@/types/react";
import PartyTerritoryKey from "./_components/party-filter";
import SelectedConstituenciesInfo from "./_components/selected";
import "./style.css";

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
  const loadingProgress = useMemo(
    () =>
      (constituencies.items.length / (constituencies.availableItems || 1)) *
      100,
    [constituencies],
  );

  const [focussedPartyId, setFocussedPartyId] = useState<number>();
  const [focussedConstituencyIds, setFocussedConstituencyIds] = useState<
    LayerKey[]
  >([]);
  const focussedConstituencies = useMemo(
    () =>
      constituencies.items.filter((it) =>
        focussedConstituencyIds.includes(it.parliamentdotuk),
      ),
    [focussedConstituencyIds, constituencies.items],
  );

  const [hovered, setHovered] = useState<LayerKey>();
  const hoveredConstituency: ConstituencyMiniBoundary | undefined =
    useMemo(() => {
      if (!hovered) return undefined;
      return constituencies.items.find((it) => it.parliamentdotuk === hovered);
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

  const onSelectFeatures = useCallback(
    (layers: LayerKey[], resetPartyFocus: boolean = true) => {
      setFocussedConstituencyIds(layers);
      if (resetPartyFocus) {
        setFocussedPartyId(undefined);
      }
    },
    [],
  );

  const filterByParty = useCallback(
    (partyId: number) => {
      map?.selectFeatures("partyId", partyId, { fit: true });
      setFocussedPartyId(partyId);
      onSelectFeatures(
        constituencies.items
          .filter((it) => it.mp?.party?.parliamentdotuk === partyId)
          .map((it) => it.parliamentdotuk),
        false,
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
    if (focussedPartyId) {
      filterByParty(focussedPartyId);
    }

    constituencies.loadNext?.();
  }, [map, constituencies.items, constituencies.loadNext]);

  return (
    <div className="map-layout">
      <Map map={map} className="map-layout--map">
        <HoveredConstituency
          constituency={hoveredConstituency}
          className="touch:hidden absolute bottom-0 right-0 z-10 m-2"
        />
        <LoadingMessage
          progress={loadingProgress}
          className="chip surface absolute bottom-0 left-0 z-10 m-2"
        />
      </Map>

      <div className="map-layout--overlays">
        <PartyTerritoryKey
          parties={territories}
          className="map-layout--key"
          focussedPartyId={focussedPartyId}
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

const LoadingMessage = (props: { progress: number } & DivPropsNoChildren) => {
  const { progress, ...rest } = props;
  return (
    <div {...rest}>
      {onlyIf(
        progress < 100,
        <p className="chip-content">Loading constituency maps…</p>,
      )}
      <LoadingBar progress={progress} />
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
          cssColor: `color-mix(in srgb, ${party.theme?.primary}, white)`,
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
          cssColor: `transparent`,
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
        className="chip chip-content pointer-events-none"
      >
        <div className="column items-end">
          <ConstituencyLink constituency={constituency} className="text-lg" />

          {onlyIf(constituency?.mp, (mp) => (
            <>
              <PersonLink person={mp} />
              <PartyLink party={mp?.party} showDot={false} />
            </>
          ))}
        </div>
      </PartyIconBackground>
    </div>
  );
};
