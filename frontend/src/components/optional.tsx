import React, { ElementType, ReactNode, createElement } from "react";
import { Props } from "@/types/react";

type OptionalProps<T> = {
  value: T | null | undefined;
  condition?: (value: T) => boolean;
  block?: (value: T) => ReactNode;
};

type OptionalElementProps<E extends ElementType, T> = Props<
  E,
  OptionalProps<T>,
  "children"
>;

const OptionalElement = <E extends ElementType, T>(
  props: { element: E | null } & OptionalElementProps<E, T>,
) => {
  const { element, value, condition, block, ...rest } = props;

  if (!isTruthy(value, condition)) return null;

  const content = (block ?? ((obj) => `${obj}`))(value);
  if (element) {
    return createElement(element, rest, content);
  }
  return <>{content}</>;
};

export const OptionalDiv = <T,>(props: OptionalElementProps<"div", T>) => (
  <OptionalElement element="div" {...props} />
);

export const OptionalSpan = <T,>(props: OptionalElementProps<"span", T>) => (
  <OptionalElement element="span" {...props} />
);

export const Optional = <T,>(props: OptionalProps<T>) => (
  <OptionalElement element={null} {...props} />
);

export const onlyIf = <T, R>(
  value: T | null | undefined,
  block: R | ((value: T) => R),
): R | undefined => {
  if (isTruthy(value)) {
    return isFunction(block) ? block(value) : block;
  }
};

const isTruthy = <T,>(
  value: T | null | undefined,
  condition?: (value: T) => boolean,
): value is T => {
  if (value == null) return false;
  if (condition) return condition(value);
  if (value === false) return false;
  if (Array.isArray(value) && value.length === 0) return false;

  return true;
};
const isFunction = <T, R>(
  value: R | ((value: T) => R),
): value is (value: T) => R => {
  return typeof value === "function";
};
