"use client";

import { getNationalConstituencyMaps, NationalBoundary } from "@/api";
import { type LayerKey, Map, useMap } from "@/components/map";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { PartyIconBackground, rgb } from "@/components/themed/party";
import { usePagination } from "@/components/paginated/pagination";
import { MemberItem } from "@/components/item-member";
import { ConstituencyLink } from "@/components/linked-data";

export default function NationalMap() {
  const pagination = usePagination(getNationalConstituencyMaps);
  const [focus, setFocus] = useState<LayerKey | undefined>();
  const isFocusLocked = useRef<boolean>(false);

  const focussedConstituency = useMemo(() => {
    if (focus) {
      return pagination.items.find((it) => it.parliamentdotuk === focus);
    }
  }, [focus, pagination.items]);

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
      minResolution: 300,
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
    pagination.items.forEach((constituency) => {
      const boundary = constituency.boundary;
      if (boundary) {
        map?.addOverlay({
          layerKey: constituency.parliamentdotuk,
          geoJson: JSON.parse(boundary),
          color: rgb(constituency.mp?.party?.theme?.primary),
        });
      }
    });
    pagination.loadNext?.();
  }, [map, pagination.items, pagination.loadNext]);

  return (
    <Map map={map} className="aspect-square max-h-[80vh] w-full">
      <ConstituencyHoverInfo info={focussedConstituency} />
    </Map>
  );
}

const ConstituencyHoverInfo = ({
  info,
}: {
  info: NationalBoundary | undefined;
}) => {
  if (!info) return null;
  return (
    <div className="w-listitem_card absolute right-0 bottom-0">
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
