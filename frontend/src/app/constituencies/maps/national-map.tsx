"use client";

import { ConstituencyMiniBoundary, PartyTerritory, get } from "@/api";
import { type LayerKey, Map, useMap } from "@/components/map";
import {
  ComponentPropsWithoutRef,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { PartyIconBackground } from "@/components/themed/party";
import { usePagination } from "@/components/paginated/pagination";
import { MemberItem } from "@/components/item-member";
import { ConstituencyLink, hrefFor } from "@/components/linked-data";
import { addClass, classes } from "@/util/transforms";
import { usePassiveGeoLocation } from "@/components/map/geolocation";
import { GeoLocation, UkParliamentLocation } from "@/components/map/geography";
import { DivPropsNoChildren } from "@/types/react";
import Loading from "@/components/loading";
import Row from "@/components/row";
import Link from "next/link";
import { MapRenderer } from "@/components/map/map";

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
    <div className="relative w-full">
      <Map map={map} className="card aspect-square max-h-[80vh] w-full" />

      <PartyTerritoryKey
        parties={territories}
        className="row gap-2 overflow-auto sm:pointer-events-none sm:absolute sm:top-0 sm:left-0 sm:block [&>*]:shrink-0"
        onClickParty={filterByParty}
      />

      <SelectedConstituenciesInfo
        constituencies={focussedConstituencies}
        className="sm:absolute sm:right-0 sm:bottom-0 sm:m-2"
      />
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

const PartyTerritoryKey = (
  props: {
    parties: PartyTerritory[] | undefined;
    onClickParty: (partyId: number) => void;
  } & ComponentPropsWithoutRef<"ul">,
) => {
  const { parties, onClickParty, ...rest } = addClass(
    props,
    "text-sm max-sm:py-4 max-sm:px-edge",
  );
  if (!parties) return null;
  return (
    <ul {...rest}>
      {parties.map((party) => (
        <li
          key={party.parliamentdotuk}
          className={classes(
            "row hover:bg-surface-hover chip-content pointer-events-auto w-fit cursor-pointer list-none gap-1",
            "sm:bg-surface/80",
            "max-sm:chip",
          )}
          onClick={() => onClickParty(party.parliamentdotuk)}
        >
          <div
            className="size-em rounded-sm border-1"
            style={{ backgroundColor: party.theme?.primary }}
          />
          <div className="line-clamp-1">{party.name}</div>
        </li>
      ))}
    </ul>
  );
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

const SelectedConstituenciesInfo = (
  props: {
    constituencies: ConstituencyMiniBoundary[];
  } & DivPropsNoChildren,
) => {
  const { constituencies, ...rest } = addClass(props, "sm:w-listitem_card");
  const MaxVisibleItems = 3;

  if (constituencies.length === 0) return null;
  if (constituencies.length === 1) {
    const item = constituencies[0]!;
    return (
      <PartyIconBackground
        party={item.mp?.party}
        {...addClass(rest, "card sm:w-listitem_card w-full")}
      >
        <h2 className="card-content">
          <ConstituencyLink constituency={item} />
        </h2>
        {item.mp ? (
          <MemberItem
            member={item.mp}
            showConstituency={false}
            usePartyTheme={false}
            defaultPartyTheme={null}
          />
        ) : null}
      </PartyIconBackground>
    );
  }

  if (constituencies.length <= MaxVisibleItems) {
    // A few items selected
    return (
      <Row {...addClass(rest, "gap-2 flex-wrap")}>
        {constituencies.map((item) => (
          <Link
            key={item.parliamentdotuk}
            href={hrefFor("constituency", item.parliamentdotuk)}
          >
            <PartyIconBackground
              className="card card-content shrink-0 font-bold"
              party={item.mp?.party}
            >
              {item.name}
            </PartyIconBackground>
          </Link>
        ))}
      </Row>
    );
  }

  // Many items selected
  return (
    <div {...addClass(rest, "card card-content")}>
      <h3>{constituencies.length} selected</h3>
      <ul className="max-h-64 overflow-auto">
        {constituencies
          .sort((a, b) => a.name.localeCompare(b.name))
          .map((item) => (
            <li key={item.parliamentdotuk}>
              <Link href={hrefFor("constituency", item.parliamentdotuk)}>
                {item.name}
              </Link>
            </li>
          ))}
      </ul>
    </div>
  );
};
