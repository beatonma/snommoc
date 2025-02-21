import React from "react";
import NationalMap from "./national-map";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "National map",
  description: "National map of UK constituencies",
};

export default async function Page() {
  return <NationalMap />;
}
