import { ReactNode } from "react";

export type Nullish = null | undefined;
export type MaybeString = string | undefined;

export interface ClassNameProps {
  className?: MaybeString;
}

export interface ChildrenProps {
  children?: ReactNode;
}

/**
 * Symmetric difference of types A and B.
 * XOR<A, B> can have attributes from A, or from type B, but not both.
 */
export type XOR<A, B> =
  | (A & { [K in Exclude<keyof B, keyof A>]?: never })
  | (B & { [K in Exclude<keyof A, keyof B>]?: never });
