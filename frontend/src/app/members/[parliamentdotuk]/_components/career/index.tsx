import React, { ReactNode } from "react";
import { MemberCareer, get } from "@/api";
import { DateRange } from "@/components/datetime";
import { ErrorMessage } from "@/components/dev";
import { Optional } from "@/components/optional";
import { SeparatedRow } from "@/components/row";
import { TabLayout } from "@/components/tabs";
import {
  CommitteeLink,
  OrganisationLink,
  PostLink,
} from "@/features/linked-data";
import { RegisteredInterests } from "./registered-interests";
import {
  BlockItem,
  type CareerConstituency,
  type CareerHouse,
  type CareerParty,
  type CareerSummary,
  ConstituencyItem,
  DateRangeItem,
  HouseItem,
  ListSection,
  PartyItem,
  SecondaryStyle,
  Section,
  SummaryListSection,
} from "./shared";

export const Career = async (props: { parliamentdotuk: number }) => {
  const { parliamentdotuk } = props;
  const response = await get("/api/members/{parliamentdotuk}/career/", {
    path: { parliamentdotuk },
  });
  const career = response.data;

  if (!career) return <ErrorMessage error="Career not available." />;

  return (
    <>
      <h2>Career</h2>

      <Summary
        houses={career.houses}
        parties={career.parties}
        constituencies={career.constituencies}
      />

      <CareerSections career={career} />
    </>
  );
};

const NotEmpty = (list: unknown[]) => list.length > 0;
const Summarized = (list: unknown[]) => list.length > 1;

const CareerSections = ({ career }: { career: MemberCareer }) => {
  const nonEmptySections = [
    section("Houses", career.houses, Summarized, () => (
      <Houses houses={career.houses} />
    )),
    section("Parties", career.parties, Summarized, () => (
      <Parties parties={career.parties} />
    )),
    section("Constituencies", career.constituencies, Summarized, () => (
      <Constituencies constituencies={career.constituencies} />
    )),
    section(
      "Subjects",
      career.subjects_of_interest,
      (it) => Object.keys(it).length > 0,
      () => <SubjectsOfInterest subjects={career.subjects_of_interest} />,
    ),
    section("Posts", career.posts, NotEmpty, () => (
      <Posts posts={career.posts} />
    )),
    section("Committees", career.committees, NotEmpty, () => (
      <Committees committees={career.committees} />
    )),
    section("Registered Interests", career.interests, NotEmpty, () => (
      <RegisteredInterests interests={career.interests} />
    )),
    section("Experiences", career.experiences, NotEmpty, () => (
      <Experiences experiences={career.experiences} />
    )),
  ].filter(Boolean) as [string, () => ReactNode][];

  if (nonEmptySections.length <= 1) {
    return <>{nonEmptySections.map((it) => it[1]())}</>;
  }

  return <TabLayout tabs={nonEmptySections} />;
};

const section = <T,>(
  name: string,
  items: T,
  condition: (items: T) => boolean,
  block: () => ReactNode,
) => {
  if (!condition(items)) {
    return null;
  }

  return [name, block];
};

/**
 * Display a reduced UI for sections that don't have much to say.
 */
const Summary = (props: CareerSummary) => {
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

const Parties = ({ parties }: { parties: CareerParty[] }) => (
  <SummaryListSection
    title="Parties"
    data={parties}
    block={(it) => <PartyItem item={it as CareerParty} />}
  />
);

const Constituencies = ({
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

const Houses = ({ houses }: { houses: CareerHouse[] }) => (
  <SummaryListSection
    title="Houses"
    data={houses}
    block={(it) => <HouseItem item={it as CareerHouse} />}
  />
);

const Posts = ({ posts }: { posts: MemberCareer["posts"] }) => (
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

const Committees = ({
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

const Experiences = ({
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

const SubjectsOfInterest = ({
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
