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

export default function NationalMap() {
  const [territories, setTerritories] = useState<PartyTerritory[]>();
  const [focus, setFocus] = useState<LayerKey | undefined>();
  const isFocusLocked = useRef<boolean>(false);
  const userLocation: GeoLocation | undefined =
    usePassiveGeoLocation(UkParliamentLocation);
  const constituencies = usePagination(
    "/api/maps/constituencies/",
    userLocation,
  );

  useEffect(() => {
    get("/api/maps/parties/").then((it) => {
      setTerritories(it.data);
    });
  }, []);
  const focussedConstituency = useMemo(() => {
    if (focus) {
      return constituencies.items.find((it) => it.parliamentdotuk === focus);
    }
  }, [focus, constituencies.items]);

  useEffect(() => {
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
  }, [territories]);

  const onClickFeature = useCallback(
    (id: LayerKey | undefined) => {
      if (id) {
        if (id === focus) isFocusLocked.current = !isFocusLocked.current;
        else {
          isFocusLocked.current = true;
        }
      } else {
        isFocusLocked.current = false;
      }
      setFocus(id);
    },
    [focus],
  );

  const map = useMap({
    provider: null,
    viewOptions: {
      minResolution: 75,
    },
    events: {
      onHover: (id) => {
        if (!isFocusLocked.current) {
          setFocus(id);
        }
      },
      onClick: (id) => onClickFeature(id),
    },
  });

  useEffect(() => {
    constituencies.items.forEach((constituency) => {
      const boundary = constituency.boundary;
      if (boundary) {
        map?.addOverlay({
          layerKey: constituency.parliamentdotuk,
          geoJson: JSON.parse(boundary),
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
}

const ConstituencyHoverInfo = (
  props: {
    info: ConstituencyMap | undefined;
  } & DivPropsNoChildren,
) => {
  const { info, ...rest } = addClass(props, "card w-listitem_card");
  if (!info) return null;
  return (
    <div {...rest}>
      <PartyIconBackground party={info.mp?.party} className="w-listitem_card">
        <h2 className="card-content">
          <ConstituencyLink constituency={info} />
        </h2>
        {info.mp ? (
          <MemberItem
            member={info.mp}
            showConstituency={false}
            usePartyTheme={false}
            defaultPartyTheme={null}
          />
        ) : null}
      </PartyIconBackground>
    </div>
  );
};

const TerritoryInfo = (
  props: {
    parties: PartyTerritory[] | undefined;
  } & ComponentPropsWithoutRef<"ul">,
) => {
  const { parties, ...rest } = addClass(props, "text-sm");
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
