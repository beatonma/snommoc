import {
  ComponentPropsWithRef,
  ComponentPropsWithoutRef,
  Dispatch,
  ElementType,
  SetStateAction,
} from "react";

/* Create a type with the properties of Element and Extra, without the properties of Except.
 * If a property is found on both Element and Extra, the signature from Extra will override. */
export type Props<
  Element extends ElementType = "div",
  Extra extends object = object,
  Except extends keyof ComponentPropsWithoutRef<Element> | keyof Extra = never,
> = Extra & Omit<ComponentPropsWithoutRef<Element>, keyof Extra | Except>;

/* Create a type with the properties of Element and Extra, without the properties of Except.
 * If a property is found on both Element and Extra, the signature from Extra will override. */
export type PropsWithRef<
  Element extends ElementType = "div",
  Extra extends object = object,
  Except extends keyof ComponentPropsWithoutRef<Element> | keyof Extra = never,
> = Extra & Omit<ComponentPropsWithRef<Element>, keyof Extra | Except>;

export type DivProps<
  Extra extends object = object,
  Except extends keyof ComponentPropsWithoutRef<"div"> | keyof Extra = never,
> = Props<"div", Extra, Except>;
export type DivPropsNoChildren<
  Extra extends object = object,
  Except extends keyof ComponentPropsWithoutRef<"div"> | keyof Extra = never,
> = Props<"div", Extra, "children" | Except>;

export type PropsExcept<
  Element extends ElementType,
  Except extends keyof ComponentPropsWithoutRef<Element>,
> = Props<Element, object, Except>;

export type StateSetter<T> = Dispatch<SetStateAction<T>>;
export type State<T> = [T, StateSetter<T>];

export type ClassNameProps = Pick<Props, "className">;
