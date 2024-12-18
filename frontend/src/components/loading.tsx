import { DivPropsNoChildren } from "@/types/react";
import { Icon } from "@/components/icon";

export default function Loading(props: DivPropsNoChildren) {
  return (
    <div className="loading" {...props}>
      <Icon icon="CommonsPerson" />
      <Icon icon="CommonsTie" />
      <Icon icon="CommonsTie" />
    </div>
  );
}
