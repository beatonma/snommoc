import { DivProps } from "@/types/react";
import React from "react";
import { addClass } from "@/util/transforms";

export const SeparatedRow = (props: DivProps) => {
  return (
    <div
      {...addClass(
        props,
        `[&>*:not(:last-child)]:after:content-['-'] [&>*:not(:last-child)]:after:mx-1 flex flex-wrap`,
      )}
    />
  );
};
