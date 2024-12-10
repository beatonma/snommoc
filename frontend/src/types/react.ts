import { ComponentPropsWithoutRef } from "react";

export type DivProps = ComponentPropsWithoutRef<"div">;
export type DivPropsNoChildren = Omit<DivProps, "children">;
