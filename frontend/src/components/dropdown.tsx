"use client";

import { ReactNode } from "react";
import { Props } from "@/types/react";

export const Dropdown = (props: Props<"details", { summary: ReactNode }>) => {
  const { children, summary, ...rest } = props;
  return (
    <details {...rest}>
      <summary className="hover">{summary}</summary>
      {children}
    </details>
  );
};
