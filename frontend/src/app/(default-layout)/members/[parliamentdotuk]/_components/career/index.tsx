"use client";

import React from "react";
import { ResponseOf } from "@/api/client";
import { useGet } from "@/api/hooks";
import { MemberCareer } from "@/api/schema";
import { DateRange } from "@/components/datetime";
import { LoadingSpinner } from "@/components/loading";
import { SeparatedRow } from "@/components/row";
import { useTabContent } from "@/components/tabs";
import { TabLayout } from "@/components/tabs";
import {
  CommitteeLink,
  ConstituencyLink,
  HouseLink,
  OrganisationLink,
  PartyLink,
  PostLink,
} from "@/features/linked-data";
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

  if (career === "loading") return <LoadingSpinner />;
  if (!career) return null;

  return (
    <div className="surface card card-content space-y-2">
      <h2>Career</h2>
      <CareerTabLayout parliamentdotuk={parliamentdotuk} career={career} />
    </div>
  );
};

const CareerTabLayout = (props: {
  parliamentdotuk: number;
  career: Career;
}) => {
  const { parliamentdotuk, career } = props;

  const tabs = useTabContent([
    {
      title: "Summary",
      content: () => (
        <CareerSummary
          houses={career.houses}
          parties={career.parties}
          constituencies={career.constituencies}
        />
      ),
    },
    {
      title: "Subjects",
      condition: Object.keys(career.subjects_of_interest).length > 0,
      content: () => (
        <SubjectsOfInterest subjects={career.subjects_of_interest} />
      ),
    },
    {
      title: "Posts",
      condition: career.posts.length > 0,
      content: () => <Posts posts={career.posts} />,
    },
    {
      title: "Committees",
      condition: career.committees.length > 0,
      content: () => <Committees committees={career.committees} />,
    },
    {
      title: "Registered Interests",
      condition: career.interests.length > 0,
      content: () => <RegisteredInterests interests={career.interests} />,
    },
    {
      title: "Experiences",
      condition: career.experiences.length > 0,
      content: () => <Experiences experiences={career.experiences} />,
    },
    {
      title: "Voting History",
      content: () => (
        <SectionLayout>
          <MemberVotingHistory parliamentdotuk={parliamentdotuk} />
        </SectionLayout>
      ),
    },
  ]);

  return <TabLayout contentProps={{ className: "py-8" }} tabs={tabs} />;
};

/**
 * Display a reduced UI for sections that don't have much to say.
 */
const CareerSummary = (props: CareerSummaryData) => {
  const { houses, parties, constituencies } = props;

  if (!houses.length && !parties.length && !constituencies.length) return null;

  return (
    <section className="space-y-2">
      {parties.map((it) => (
        <InlineDateRangeItem key={it.start} start={it.start} end={it.end}>
          <span>
            <PartyLink party={it.party} /> member
          </span>
        </InlineDateRangeItem>
      ))}
      {constituencies.map((it) => (
        <InlineDateRangeItem key={it.start} start={it.start} end={it.end}>
          <span>
            MP for <ConstituencyLink constituency={it.constituency} />
          </span>
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
