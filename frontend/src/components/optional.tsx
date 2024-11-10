import { ReactNode } from "react";

interface OptionalProps<T> {
  condition: T | null | undefined;
  children: (obj: T) => ReactNode;
}
export const Optional = <T extends any>(props: OptionalProps<T>) => {
  if (props.condition) {
    return <>{props.children(props.condition)}</>;
  }
};
