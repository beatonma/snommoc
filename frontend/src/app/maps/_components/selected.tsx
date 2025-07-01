import React, { useMemo } from "react";
import { ConstituencyMiniBoundary, Party } from "@/api/schema";
import { onlyIf } from "@/components/optional";
import { MemberItemCard } from "@/features/cards";
import { ConstituencyLink, HouseLink, PartyLink } from "@/features/linked-data";
import { ItemTheme } from "@/features/themed/item-theme";
import { DivPropsNoChildren } from "@/types/react";
import { addClass } from "@/util/transforms";

type Single = DivPropsNoChildren<{
  constituency: ConstituencyMiniBoundary;
}>;
type Multi = DivPropsNoChildren<{
  constituencies: ConstituencyMiniBoundary[];
}>;

export const SelectedConstituenciesInfo = (props: Multi) => {
  const { constituencies, ...rest } = addClass(
    props,
    "md:w-listitem-card w-full",
  );

  if (constituencies.length === 0) return <NoSelection {...rest} />;
  if (constituencies.length === 1) {
    return <SingleSelection constituency={constituencies[0]!} {...rest} />;
  }

  return <ManySelected constituencies={constituencies} {...rest} />;
};

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
  const { constituency, ...rest } = addClass(props, "card surface");
  return (
    <ItemTheme themeSource={constituency.mp?.party} {...rest}>
      <h2>
        <ConstituencyLink constituency={constituency} className="p-2" />
      </h2>
      {onlyIf(constituency.mp, (mp) => (
        <MemberItemCard
          member={mp}
          showConstituency={false}
          className="block bg-transparent"
        />
      ))}
    </ItemTheme>
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
                <li key={item.parliamentdotuk}>
                  <ConstituencyLink
                    constituency={item}
                    icon={
                      <span
                        className="size-1 rounded-xs"
                        style={{ backgroundColor: group.party.theme?.primary }}
                      ></span>
                    }
                  />
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </div>
  );
};
