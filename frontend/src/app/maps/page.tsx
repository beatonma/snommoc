import { Metadata } from "next";
import React from "react";
import { NationalMap } from "./national-map";

export const metadata: Metadata = {
  title: "National map",
  description: "National map of UK constituencies",
};

export default async function Page() {
  return <NationalMap />;
}
