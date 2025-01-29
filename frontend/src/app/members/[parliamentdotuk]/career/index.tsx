import { getMemberCareer } from "@/api";
import ErrorMessage from "@/components/error";
import React from "react";
import {
  Posts,
  Parties,
  Houses,
  Constituencies,
  Experiences,
  Committees,
  SubjectsOfInterest,
  Summary,
  RegisteredInterests,
} from "./sections";

export default async function Career(props: { parliamentdotuk: number }) {
  const { parliamentdotuk } = props;
  const response = await getMemberCareer(parliamentdotuk);
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

      <Houses houses={career.houses} />
      <Parties parties={career.parties} />
      <Constituencies constituencies={career.constituencies} />

      <SubjectsOfInterest subjects={career.subjects_of_interest} />

      <Posts posts={career.posts} />
      <Committees committees={career.committees} />
      <RegisteredInterests interests={career.interests} />
      <Experiences experiences={career.experiences} />
    </>
  );
}
