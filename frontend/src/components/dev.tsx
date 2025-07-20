"use client";

import { useEffect } from "react";
import { Callout } from "@/components/callout";
import { DivProps, DivPropsNoChildren } from "@/types/react";
import { addClass } from "@/util/transforms";

interface TodoProps {
  message: string;
}
export const Todo = (props: DivPropsNoChildren<TodoProps>) => {
  const { message, ...rest } = props;

  const content = ["TODO", message].filter(Boolean).join(": ");
  useEffect(() => {
    console.warn(content);
  }, [content]);

  return <div {...addClass(rest, "bg-[#ff0]/60 text-[#000]")}>{content}</div>;
};

export const Placeholder = (props: DivPropsNoChildren) => {
  return (
    <Callout {...props}>
      <strong>This page is a placeholder.</strong>
      <p>
        Useful content is intended to be here, but it&#39;s not ready quite yet
        - sorry about that.
      </p>
    </Callout>
  );
};

export const Stub = (props: DivProps) => {
  return (
    <div
      {...addClass(
        props,
        "bg-accent/10 outline-1 outline-dashed outline-accent outline-offset-4",
      )}
    />
  );
};

export const ErrorMessage = ({ error }: { error?: string }) => (
  <div className="bg-red-800 text-white">
    {["Error", error].filter(Boolean).join(": ")}
  </div>
);
