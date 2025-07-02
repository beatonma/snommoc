"use client";

import React, { ReactNode, useMemo } from "react";
import { ResponseOf } from "@/api/client";
import { useGet } from "@/api/hooks";
import { MemberCareer } from "@/api/schema";
import { DateRange } from "@/components/datetime";
import { LoadingSpinner } from "@/components/loading";
import { SeparatedRow } from "@/components/row";
import { TabContent } from "@/components/tabs";
import { TabLayout } from "@/components/tabs";
import {
  CommitteeLink,
  ConstituencyLink,
  HouseLink,
  OrganisationLink,
  PartyLink,
  PostLink,
} from "@/features/linked-data";
import { Nullish } from "@/types/common";
import {
  type CareerSummary as CareerSummaryData,
  DateRangeItem,
  InlineDateRangeItem,
  ListSection,
  SecondaryStyle,
  Section,
  SectionLayout,
} from "./components";
import { RegisteredInterests } from "./registered-interests";
import { MemberVotingHistory } from "./votes";

type Career = ResponseOf<"/api/members/{parliamentdotuk}/career/">;

export const FullCareer = (props: { parliamentdotuk: number }) => {
  const { parliamentdotuk } = props;
  const career = useGet("/api/members/{parliamentdotuk}/career/", {
    path: { parliamentdotuk },
  });

  const tabs: TabContent<string>[] | null = useMemo(() => {
    if (career === "loading" || !career) return null;
    return [
      ...getCareerTabs(career),
      [
        "Voting history",
        () => (
          <SectionLayout title="Voting History">
            <MemberVotingHistory parliamentdotuk={parliamentdotuk} />
          </SectionLayout>
        ),
      ],
    ];
  }, [parliamentdotuk, career]);

  if (career === "loading") return <LoadingSpinner />;
  if (!career) return null;
  if (!tabs) return null;

  return (
    <div className="surface card card-content space-y-2">
      <h2>Career</h2>
      <TabLayout contentProps={{ className: "py-8" }} tabs={tabs} />
    </div>
  );
};

const getCareerTabs = (career: Career | Nullish): TabContent<string>[] => {
  if (!career) return [];
  return [
    [
      "Summary",
      () => (
        <CareerSummary
          houses={career.houses}
          parties={career.parties}
          constituencies={career.constituencies}
        />
      ),
    ],
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
  ].filter(Boolean) as TabContent<string>[];
};

const NotEmpty = (list: unknown[]) => list.length > 0;

const section = <T,>(
  name: string,
  items: T,
  condition: (items: T) => boolean,
  block: () => ReactNode,
): TabContent<string> | null => {
  if (!condition(items)) {
    return null;
  }

  return [name, block];
};

/**
 * Display a reduced UI for sections that don't have much to say.
 */
const CareerSummary = (props: CareerSummaryData) => {
  const { houses, parties, constituencies } = props;

  if (!houses.length && !parties.length && !constituencies.length) return null;

  return (
    <section>
      {parties.map((it) => (
        <InlineDateRangeItem key={it.start} start={it.start} end={it.end}>
          <PartyLink party={it.party} />
        </InlineDateRangeItem>
      ))}
      {constituencies.map((it) => (
        <InlineDateRangeItem key={it.start} start={it.start} end={it.end}>
          MP for <ConstituencyLink constituency={it.constituency} />
        </InlineDateRangeItem>
      ))}
      {houses.map((it) => (
        <InlineDateRangeItem key={it.start} start={it.start} end={it.end}>
          <HouseLink house={it.house} longFormat={true} />
        </InlineDateRangeItem>
      ))}
    </section>
  );
};

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
        <div>
          <div>
            <span>{it.title}</span>
            <span className="text-reduced"> at </span>
            <OrganisationLink organisation={it.organisation} />
          </div>

          <SeparatedRow className={SecondaryStyle}>
            <span>{it.category}</span>
            <DateRange start={it.start} end={it.end} />
          </SeparatedRow>
        </div>
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
