import { ComponentPropsWithoutRef, Dispatch, SetStateAction } from "react";

export type DivProps = ComponentPropsWithoutRef<"div">;
export type DivPropsNoChildren = Omit<DivProps, "children">;

export type StateSetter<S> = Dispatch<SetStateAction<S>>;
