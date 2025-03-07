import React, { useMemo } from "react";
import { ConstituencyMiniBoundary, Party } from "@/api";
import {
  ConstituencyLink,
  HouseLink,
  PartyLink,
} from "@/components/models/linked-data";
import { MemberItemCard } from "@/components/models/list-item";
import { onlyIf } from "@/components/optional";
import Row from "@/components/row";
import { PartyTheme } from "@/components/themed/party";
import { DivPropsNoChildren } from "@/types/react";
import { addClass } from "@/util/transforms";

type Single = {
  constituency: ConstituencyMiniBoundary;
} & DivPropsNoChildren;
type Multi = {
  constituencies: ConstituencyMiniBoundary[];
} & DivPropsNoChildren;

export default function SelectedConstituenciesInfo(props: Multi) {
  const { constituencies, ...rest } = addClass(
    props,
    "md:w-listitem_card w-full",
  );

  if (constituencies.length === 0) return <NoSelection {...rest} />;
  if (constituencies.length === 1) {
    return <SingleSelection constituency={constituencies[0]!} {...rest} />;
  }

  return <ManySelected constituencies={constituencies} {...rest} />;
}

const NoSelection = (props: DivPropsNoChildren) => {
  return (
    <div
      {...addClass(
        props,
        "card card-content surface-accent column gap-2 text-lg",
      )}
    >
      <h2>Parliamentary constituencies</h2>
      <p>
        The UK is divided into 650 constituencies which each elect a Member of
        Parliament (MP) to the{" "}
        <HouseLink house="Commons" longFormat={true} showDot={false} />
      </p>
      <p>
        Tap a constituency for more information, or select a party to see the
        constituencies they represent.
      </p>
    </div>
  );
};

const SingleSelection = (props: Single) => {
  const { constituency, ...rest } = addClass(
    props,
    "card bg-[color-mix(in_srgb,var(--primary)_15%,var(--surface))]",
  );
  return (
    <PartyTheme party={constituency.mp?.party} {...rest}>
      <h2>
        <ConstituencyLink constituency={constituency} className="p-2" />
      </h2>
      {onlyIf(constituency.mp, (mp) => (
        <MemberItemCard
          member={mp}
          showConstituency={false}
          className="block hover bg-transparent"
        />
      ))}
    </PartyTheme>
  );
};

interface GroupedByParty {
  party: Party;
  constituencies: ConstituencyMiniBoundary[];
}
const ManySelected = (props: Multi) => {
  const { constituencies, ...rest } = props;
  const groupedByParty: GroupedByParty[] = useMemo(() => {
    const parties: Record<string, Party> = {};
    const groups: Record<string, ConstituencyMiniBoundary[]> = {};

    constituencies.forEach((item) => {
      const party = item.mp?.party;
      if (!party) return;
      const id = party.parliamentdotuk.toString();
      parties[id] = party;
      groups[id] = [...(groups[id] ?? []), item];
    });

    const orderedPartyIds: string[] = Object.keys(parties).sort(
      (a, b) => groups[a]!.length - groups[b]!.length,
    );
    return orderedPartyIds.map((partyId) => {
      return {
        party: parties[partyId],
        constituencies: groups[partyId]?.sort((a, b) =>
          a.name.localeCompare(b.name),
        ),
      } as GroupedByParty;
    });
  }, [constituencies]);

  return (
    <div
      {...addClass(
        rest,
        "card card-content surface-accent grid grid-rows-[min-content_1fr]",
      )}
    >
      <h3>{constituencies.length} selected</h3>
      <ul className="list-none overflow-x-hidden overflow-y-auto">
        {groupedByParty.map((group) => (
          <li key={group.party.parliamentdotuk} className="my-2">
            <PartyLink party={group.party} />

            <ul className="list-none pl-1">
              {group.constituencies.map((item) => (
                <li
                  key={item.parliamentdotuk}
                  className="max-w-full overflow-x-hidden"
                >
                  <Row className="gap-2">
                    <div
                      className="size-1 rounded-sm"
                      style={{ backgroundColor: group.party.theme?.primary }}
                    />
                    <ConstituencyLink constituency={item} />
                  </Row>
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </div>
  );
};
