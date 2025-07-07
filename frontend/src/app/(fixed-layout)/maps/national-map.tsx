"use client";

import React, { useCallback, useEffect, useMemo, useState } from "react";
import { get } from "@/api";
import { ConstituencyMiniBoundary, PartyTerritory } from "@/api/schema";
import { LoadingBar, LoadingSpinner } from "@/components/loading";
import { onlyIf } from "@/components/optional";
import {
  ConstituencyLink,
  PartyLink,
  PersonLink,
} from "@/features/linked-data";
import { type LayerKey, Map, useMap } from "@/features/map";
import { GeoLocation, UkParliamentLocation } from "@/features/map/geography";
import { usePassiveGeoLocation } from "@/features/map/geolocation";
import { MapRenderer } from "@/features/map/map";
import { usePagination } from "@/features/paginated";
import { PartyIconBackground } from "@/features/themed/item-theme";
import { DivPropsNoChildren } from "@/types/react";
import { classes } from "@/util/transforms";
import { PartyTerritoryKey } from "./_components/party-filter";
import { SelectedConstituenciesInfo } from "./_components/selected";
import styles from "./national-map.module.css";

export const NationalMap = () => {
  const userLocation: GeoLocation | undefined =
    usePassiveGeoLocation(UkParliamentLocation);

  if (!userLocation) return <LoadingSpinner />;

  return <NationalMapWithLocation userLocation={userLocation} />;
};

const NationalMapWithLocation = ({
  userLocation,
}: {
  userLocation: GeoLocation;
}) => {
  const [territories, setTerritories] = useState<PartyTerritory[]>();
  const constituencies = usePagination("/api/maps/constituencies/", {
    query: userLocation,
  });
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
  }, [
    map,
    constituencies.items,
    constituencies.loadNext,
    filterByParty,
    focussedPartyId,
  ]);

  return (
    <div
      className={classes(
        styles.nationalMapLayout,
        "h-full gap-2 overflow-hidden",
      )}
    >
      <Map map={map} className={classes(styles.map, "card surface size-full")}>
        <HoveredConstituency
          constituency={hoveredConstituency}
          className="touch:hidden absolute bottom-0 right-0 z-10 m-2"
        />
        <LoadingMessage
          progress={loadingProgress}
          className="chip surface absolute bottom-0 left-0 z-10 m-2"
        />
      </Map>

      <div
        className={classes(
          styles.overlays,
          "contents max-h-full overflow-y-hidden",
        )}
      >
        <PartyTerritoryKey
          parties={territories}
          className={classes(
            styles.key,
            "px-edge row-scroll items-center gap-x-4 gap-y-2 py-4 text-base",
          )}
          focussedPartyId={focussedPartyId}
          onClickParty={filterByParty}
        />

        <SelectedConstituenciesInfo
          constituencies={focussedConstituencies}
          className={classes(
            styles.info,
            "mx-auto h-fit max-h-full overflow-hidden",
          )}
        />
      </div>
    </div>
  );
};

const LoadingMessage = (props: DivPropsNoChildren<{ progress: number }>) => {
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
  props: DivPropsNoChildren<{
    constituency: ConstituencyMiniBoundary | undefined;
  }>,
) => {
  const { constituency, ...rest } = props;

  return (
    <div {...rest}>
      <PartyIconBackground
        themeSource={constituency?.mp?.party}
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
