import { MemberCareer } from "@/api";
import {
  CommitteeLink,
  OrganisationLink,
  PostLink,
} from "@/components/models/linked-data";
import { DateRange } from "@/components/datetime";
import { SeparatedRow } from "@/components/collection";
import React, { ReactNode } from "react";
import {
  BlockItem,
  ConstituencyItem,
  HouseItem,
  ListSection,
  PartyItem,
  SecondaryStyle,
  Section,
  SummaryListSection,
  type CareerConstituency,
  type CareerHouse,
  type CareerParty,
  type CareerSummary,
  DateRangeItem,
} from "./shared";
import { Optional } from "@/components/optional";
export { default as RegisteredInterests } from "./registered-interests";

/**
 * Display a reduced UI for sections that don't have much to say.
 */
export const Summary = (props: CareerSummary) => {
  const { houses, parties, constituencies } = props;

  const SummaryItem = <T,>(props: {
    items: T[];
    block: (item: T) => ReactNode;
  }) => (
    <Optional
      value={props.items[0]}
      condition={() => props.items.length === 1}
      block={props.block}
    />
  );

  return (
    <section>
      <SummaryItem items={parties} block={(it) => <PartyItem item={it} />} />
      <SummaryItem
        items={constituencies}
        block={(it) => <ConstituencyItem prefix="MP for" item={it} />}
      />
      <SummaryItem
        items={houses}
        block={(it) => (
          <HouseItem item={it} longFormat={true} prefix="Member of" />
        )}
      />
    </section>
  );
};

export const Parties = ({ parties }: { parties: CareerParty[] }) => (
  <SummaryListSection
    title="Parties"
    data={parties}
    block={(it) => <PartyItem item={it as CareerParty} />}
  />
);

export const Constituencies = ({
  constituencies,
}: {
  constituencies: CareerConstituency[];
}) => (
  <SummaryListSection
    title="Constituencies"
    data={constituencies}
    block={(it) => <ConstituencyItem item={it as CareerConstituency} />}
  />
);

export const Houses = ({ houses }: { houses: CareerHouse[] }) => (
  <SummaryListSection
    title="Houses"
    data={houses}
    block={(it) => <HouseItem item={it as CareerHouse} />}
  />
);

export const Posts = ({ posts }: { posts: MemberCareer["posts"] }) => (
  <ListSection
    title="Posts"
    data={posts}
    block={(post) => (
      <DateRangeItem start={post.start} end={post.end}>
        <PostLink post={post} />
      </DateRangeItem>
    )}
  />
);

export const Committees = ({
  committees,
}: {
  committees: MemberCareer["committees"];
}) => (
  <ListSection
    title="Committees"
    data={committees}
    block={(it) => (
      <DateRangeItem start={it.start} end={it.end}>
        <CommitteeLink committee={it} />
      </DateRangeItem>
    )}
  />
);

export const Experiences = ({
  experiences,
}: {
  experiences: MemberCareer["experiences"];
}) => {
  return (
    <ListSection
      title="Non-parliamentary experience"
      data={experiences}
      block={(it) => (
        <BlockItem>
          <div>
            <span>{it.title}</span>
            <span> at </span>
            <OrganisationLink organisation={it.organisation} />
          </div>

          <SeparatedRow className={SecondaryStyle}>
            <span>{it.category}</span>
            <DateRange start={it.start} end={it.end} />
          </SeparatedRow>
        </BlockItem>
      )}
    />
  );
};

export const SubjectsOfInterest = ({
  subjects,
}: {
  subjects: MemberCareer["subjects_of_interest"];
}) => (
  <Section
    className="gap-y-4"
    title="Subjects of interest"
    data={subjects}
    block={(data) =>
      Object.entries(data).map(([category, items]) => (
        <div key={category}>
          <div className="text-lg">{category}</div>
          <ul>
            {items.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      ))
    }
  />
);
