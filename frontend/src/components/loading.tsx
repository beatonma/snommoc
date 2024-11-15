import { ComponentPropsWithoutRef } from "react";

export default function Loading(
  props: Omit<ComponentPropsWithoutRef<"div">, "children">,
) {
  return <div {...props}>LOADING</div>;
}
