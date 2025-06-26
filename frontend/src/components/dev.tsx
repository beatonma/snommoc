"use client";

import { useEffect } from "react";
import { DivPropsNoChildren } from "@/types/react";
import { addClass } from "@/util/transforms";

export const Todo = (props: DivPropsNoChildren<{ message: string }>) => {
  const { message, ...rest } = props;

  const content = ["TODO", message].filter(Boolean).join(": ");
  useEffect(() => {
    console.warn(content);
  }, [content]);

  return <div {...addClass(rest, "bg-[#ff0]/60 text-[#000]")}>{content}</div>;
};
