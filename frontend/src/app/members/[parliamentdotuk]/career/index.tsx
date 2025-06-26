import React from "react";
import { get } from "@/api";
import { Summary } from "@/app/members/[parliamentdotuk]/career/sections";
import { ErrorMessage } from "@/components/error";
import CareerSections from "./career-sections";

export default async function Career(props: { parliamentdotuk: number }) {
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
}
