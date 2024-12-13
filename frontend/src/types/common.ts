import { ReactNode } from "react";

export type Nullish = null | undefined;
export type MaybeString = string | undefined;

export interface ClassNameProps {
  className?: MaybeString;
}

export interface ChildrenProps {
  children?: ReactNode;
}
