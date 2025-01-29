"use client";
import { TabLayout } from "@/components/tabs";
import React, { ReactNode } from "react";
import {
  Posts,
  Parties,
  Houses,
  Constituencies,
  Experiences,
  Committees,
  SubjectsOfInterest,
  RegisteredInterests,
} from "./sections";
import { MemberCareer } from "@/api";

const NotEmpty = (list: unknown[]) => list.length > 0;
const Summarized = (list: unknown[]) => list.length > 1;

const Sections = ({ career }: { career: MemberCareer }) => {
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

export default Sections;
