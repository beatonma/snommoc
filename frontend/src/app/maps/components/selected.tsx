import { ConstituencyMiniBoundary, Party } from "@/api";
import { DivPropsNoChildren } from "@/types/react";
import { addClass } from "@/util/transforms";
import { PartyIconBackground } from "@/components/themed/party";
import { ConstituencyLink, PartyLink } from "@/components/linked-data";
import { MemberItem } from "@/components/item-member";
import { CSSProperties, useMemo } from "react";

type Single = {
  constituency: ConstituencyMiniBoundary;
} & DivPropsNoChildren;
type Multi = {
  constituencies: ConstituencyMiniBoundary[];
} & DivPropsNoChildren;

export const SelectedConstituenciesInfo = (props: Multi) => {
  const { constituencies, ...rest } = addClass(props, "sm:w-listitem_card");

  if (constituencies.length === 0) return null;
  if (constituencies.length === 1) {
    return <SingleSelection constituency={constituencies[0]!} {...rest} />;
  }

  return <ManySelected constituencies={constituencies} {...rest} />;
};

const SingleSelection = (props: Single) => {
  const { constituency, ...rest } = props;
  return (
    <PartyIconBackground
      party={constituency.mp?.party}
      {...addClass(rest, "card sm:w-listitem_card w-full")}
    >
      <h2 className="card-content">
        <ConstituencyLink constituency={constituency} />
      </h2>
      {constituency.mp ? (
        <MemberItem
          member={constituency.mp}
          showConstituency={false}
          usePartyTheme={false}
          defaultPartyTheme={null}
        />
      ) : null}
    </PartyIconBackground>
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
    <div {...addClass(rest, "card card-content bg-surface_alt")}>
      <h3>{constituencies.length} selected</h3>
      <ul className="list-none overflow-auto sm:max-h-48">
        {groupedByParty.map((group) => (
          <li key={group.party.parliamentdotuk} className="my-2">
            <PartyLink party={group.party} />
            <ul
              className="list-inside pl-1"
              style={
                {
                  "--color-list-marker": group.party.theme?.primary,
                } as CSSProperties
              }
            >
              {group.constituencies.map((item) => (
                <li key={item.parliamentdotuk}>
                  <ConstituencyLink constituency={item} />
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </div>
  );
};
