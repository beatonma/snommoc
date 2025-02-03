import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";
import React from "react";

export default function PageContent(props: DivProps) {
  return (
    <div
      {...addClass(
        props,
        "flex flex-col items-center gap-y-16 overflow-x-hidden",
      )}
    />
  );
}
