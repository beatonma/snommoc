import React from "react";
import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";

export const Row = (props: DivProps) => <div {...addClass(props, "row")} />;

export const SeparatedRow = (props: DivProps) => (
  <div
    {...addClass(
      props,
      `[&>*:not(:last-child)]:after:content-['·'] [&>*:not(:last-child)]:after:mx-1 flex flex-wrap`,
    )}
  />
);
