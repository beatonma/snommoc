import { DivPropsNoChildren } from "@/types/react";
import { addClass } from "@/util/transforms";
import { useEffect } from "react";

export default function Todo(props: DivPropsNoChildren & { message: string }) {
  const { message, ...rest } = props;

  const content = ["TODO", message].filter(Boolean).join(": ");
  useEffect(() => {
    console.warn(content);
  }, []);

  return <div {...addClass(rest, "bg-[#ff0]/50 text-[#000]")}>{content}</div>;
}
