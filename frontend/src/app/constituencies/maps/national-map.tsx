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
import { ConstituencyLink } from "@/components/linked-data";
import { addClass } from "@/util/transforms";
import { usePassiveGeoLocation } from "@/components/map/geolocation";
import { GeoLocation, UkParliamentLocation } from "@/components/map/geography";
import { DivPropsNoChildren } from "@/types/react";
import Loading from "@/components/loading";
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
  const [focus, setFocus] = useState<LayerKey[]>([]);
  const isFocusLocked = useRef<boolean>(false);
  const constituencies = usePagination(
    "/api/maps/constituencies/",
    userLocation,
  );
  const focussedConstituency = useMemo(
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
      <TerritoryInfo parties={territories} className="absolute top-0 left-0" />
      <ConstituencyHoverInfo
        info={focussedConstituency}
        className="absolute right-0 bottom-0 m-2"
      />
    </Map>
  );
};

const ConstituencyHoverInfo = (
  props: {
    info: ConstituencyMap[];
  } & DivPropsNoChildren,
) => {
  const { info, ...rest } = addClass(props, "w-listitem_card");
  const MaxVisibleItems = 3;

  if (info.length === 0) return null;
  if (info.length === 1) {
    const item = info[0]!;
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

  const hiddenItems = info.length - MaxVisibleItems;
  return (
    <Row {...addClass(rest, "gap-2 flex-wrap")}>
      {info.slice(0, MaxVisibleItems).map((item) => (
        <PartyIconBackground
          className="card card-content shrink-0"
          party={item.mp?.party}
          key={item.parliamentdotuk}
        >
          <ConstituencyLink constituency={item} />
        </PartyIconBackground>
      ))}
      {hiddenItems > 0 ? `and ${hiddenItems} more` : null}
    </Row>
  );
};

const TerritoryInfo = (
  props: {
    parties: PartyTerritory[] | undefined;
  } & ComponentPropsWithoutRef<"ul">,
) => {
  const { parties, ...rest } = addClass(props, "text-sm pointer-events-none");
  if (!parties) return null;
  return (
    <ul {...rest}>
      {parties.map((party) => (
        <li
          key={party.parliamentdotuk}
          className="row bg-surface/80 w-fit list-none gap-1 px-2 py-1"
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
