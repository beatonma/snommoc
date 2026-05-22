"use client";

import React, { useCallback, useEffect, useMemo, useState } from "react";
import { get } from "@/api";
import { ConstituencyMiniBoundary, PartyTerritory } from "@/api/schema";
import { LoadingBar, LoadingSpinner } from "@/components/loading";
import { onlyIf } from "@/components/optional";
import { SeparatedRow } from "@/components/row";
import { type LayerKey, Map, useMap } from "@/features/map";
import { GeoLocation, UkParliamentLocation } from "@/features/map/geography";
import { usePassiveGeoLocation } from "@/features/map/geolocation";
import { MapRenderer } from "@/features/map/map";
import { usePagination } from "@/features/paginated";
import { Paginated } from "@/features/paginated/pagination";
import { PartyIconBackground } from "@/features/themed/item-theme";
import { DivPropsNoChildren, StateSetter } from "@/types/react";
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

const NationalMapWithLocation = (props: { userLocation: GeoLocation }) => {
  const { userLocation } = props;
  const constituencies = usePagination("/api/maps/constituencies/", {
    query: userLocation,
  });
  const partyTerritories = usePartyTerritories();
  const [focussedConstituencies, setFocussedConstituencyIds] =
    useFocussedConstituencies(constituencies);
  const [hoveredConstituency, setHoveredConstituency] =
    useHoveredConstituency(constituencies);

  const loadingProgress = useMemo(
    () =>
      (constituencies.items.length / (constituencies.availableItems || 1)) *
      100,
    [constituencies],
  );

  const map = useMap(
    useMemo(
      () => ({
        provider: null,
        viewOptions: {
          minResolution: 75,
        },
        events: {
          onHover: (id) => setHoveredConstituency(id),
          onSelect: (ids) => setFocussedConstituencyIds(ids),
        },
      }),
      [setFocussedConstituencyIds, setHoveredConstituency],
    ),
  );

  const filterByParty = useCallback(
    (partyId: number) => {
      map?.selectFeatures("partyId", partyId, { fit: true });
      setFocussedConstituencyIds(
        constituencies.items
          .filter((it) => it.mp?.party?.parliamentdotuk === partyId)
          .map((it) => it.parliamentdotuk),
      );
    },
    [map, constituencies.items, setFocussedConstituencyIds],
  );

  useEffect(() => {
    if (!map) return;
    if (!partyTerritories) return;
    addPartyTerritories(partyTerritories, map);
  }, [map, partyTerritories]);

  useEffect(() => {
    if (!map) return;
    addConstituencyBoundaries(constituencies.items, map);
    constituencies.loadNext?.();
  }, [map, constituencies]);

  return (
    <NationalMapLayout
      map={map}
      hoveredConstituency={hoveredConstituency}
      focussedConstituencies={focussedConstituencies}
      territories={partyTerritories}
      onClickParty={filterByParty}
      loadingProgress={loadingProgress}
    />
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

const NationalMapLayout = (props: {
  map: MapRenderer | undefined;
  hoveredConstituency: ConstituencyMiniBoundary | undefined;
  focussedConstituencies: ConstituencyMiniBoundary[];
  territories: PartyTerritory[] | undefined;
  onClickParty: (partyId: number) => void;
  loadingProgress: number;
}) => {
  const {
    map,
    hoveredConstituency,
    focussedConstituencies,
    territories,
    onClickParty,
    loadingProgress,
  } = props;
  return (
    <div
      className={classes(
        styles.nationalMapLayout,
        "h-full gap-2 overflow-hidden",
      )}
    >
      <Map
        map={map}
        className={classes(styles.map, "card surface size-full")}
        permissionUi={(button) => (
          <div
            className={classes(
              styles.map,
              "surface-alt flex items-center justify-center",
            )}
          >
            {button}
          </div>
        )}
      >
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
          onClickParty={onClickParty}
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

const HoveredConstituency = (
  props: DivPropsNoChildren<{
    constituency: ConstituencyMiniBoundary | undefined;
  }>,
) => {
  const { constituency, ...rest } = props;
  if (!constituency) return null;

  return (
    <div {...rest}>
      <PartyIconBackground
        themeSource={constituency.mp?.party}
        className="card card-content pointer-events-none"
      >
        <div className="space text-end">
          <div className="text-lg font-bold">{constituency.name}</div>

          {onlyIf(constituency.mp, (mp) => (
            <SeparatedRow separator="comma">
              <span>{mp.name}</span>
              <span>{mp.party?.name}</span>
            </SeparatedRow>
          ))}
        </div>
      </PartyIconBackground>
    </div>
  );
};

const usePartyTerritories = (): PartyTerritory[] | undefined => {
  const [territories, setTerritories] = useState<PartyTerritory[]>();
  useEffect(() => {
    get("/api/maps/parties/").then((it) => {
      setTerritories(it.data);
    });
  }, []);

  return territories;
};

const useFocussedConstituencies = (
  constituencies: Paginated<ConstituencyMiniBoundary>,
): [ConstituencyMiniBoundary[], StateSetter<LayerKey[]>] => {
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

  return [focussedConstituencies, setFocussedConstituencyIds];
};

const useHoveredConstituency = (
  constituencies: Paginated<ConstituencyMiniBoundary>,
): [
  ConstituencyMiniBoundary | undefined,
  StateSetter<LayerKey | undefined>,
] => {
  const [hovered, setHovered] = useState<LayerKey>();
  const hoveredConstituency: ConstituencyMiniBoundary | undefined =
    useMemo(() => {
      if (!hovered) return undefined;
      return constituencies.items.find((it) => it.parliamentdotuk === hovered);
    }, [hovered, constituencies.items]);

  return [hoveredConstituency, setHovered];
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
