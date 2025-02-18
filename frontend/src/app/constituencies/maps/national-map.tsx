"use client";

import { ConstituencyMap, PartyTerritory, get } from "@/api";
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
import { addClass } from "@/util/transforms";
import { usePassiveGeoLocation } from "@/components/map/geolocation";
import { GeoLocation, UkParliamentLocation } from "@/components/map/geography";
import { DivPropsNoChildren } from "@/types/react";
import Loading from "@/components/loading";
import Row from "@/components/row";
import Link from "next/link";

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
    territories?.forEach((party) => {
      const boundary = party.territory;
      if (boundary) {
        map?.addOverlay({
          layerKey: party.parliamentdotuk,
          geoJson: JSON.parse(boundary),
          style: {
            stroke: false,
            fill: {
              color:
                party.theme?.primary ??
                document.body
                  .computedStyleMap()
                  .get("--color-house-commons")
                  ?.toString(),
            },
          },
        });
      }
    });
  }, [map, territories]);

  useEffect(() => {
    constituencies.items.forEach((constituency) => {
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
            },
          },
          zIndex: 10,
        });
      }
    });
    constituencies.loadNext?.();
  }, [map, constituencies.items, constituencies.loadNext]);

  return (
    <Map map={map} className="card aspect-square max-h-[80vh] w-full">
      <TerritoryInfo
        parties={territories}
        className="absolute top-0 left-0"
        onClickParty={filterByParty}
      />

      <ConstituencyHoverInfo
        constituencies={focussedConstituencies}
        className="absolute right-0 bottom-0 m-2"
      />
    </Map>
  );
};

const ConstituencyHoverInfo = (
  props: {
    constituencies: ConstituencyMap[];
  } & DivPropsNoChildren,
) => {
  const { constituencies, ...rest } = addClass(props, "w-listitem_card");
  const MaxVisibleItems = 3;

  if (constituencies.length === 0) return null;
  if (constituencies.length === 1) {
    const item = constituencies[0]!;
    return (
      <div {...addClass(rest, "card")}>
        <PartyIconBackground party={item.mp?.party} className="w-listitem_card">
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
      </div>
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
      <h3>{constituencies.length} items</h3>
      <div className="max-h-64 overflow-auto">
        {constituencies
          .sort((a, b) => a.name.localeCompare(b.name))
          .map((item) => (
            <p key={item.parliamentdotuk}>
              <Link href={hrefFor("constituency", item.parliamentdotuk)}>
                {item.name}
              </Link>
            </p>
          ))}
      </div>
    </div>
  );
};

const TerritoryInfo = (
  props: {
    parties: PartyTerritory[] | undefined;
    onClickParty: (partyId: number) => void;
  } & ComponentPropsWithoutRef<"ul">,
) => {
  const { parties, onClickParty, ...rest } = addClass(
    props,
    "text-sm pointer-events-none",
  );
  if (!parties) return null;
  return (
    <ul {...rest}>
      {parties.map((party) => (
        <li
          key={party.parliamentdotuk}
          className="row bg-surface/80 pointer-events-auto w-fit cursor-pointer list-none gap-1 px-2 py-1"
          onClick={() => onClickParty(party.parliamentdotuk)}
        >
          <div
            className="size-em rounded-sm border-1"
            style={{ backgroundColor: party.theme?.primary }}
          />
          <div>{party.name}</div>
        </li>
      ))}
    </ul>
  );
};
