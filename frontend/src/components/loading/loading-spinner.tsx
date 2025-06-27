import Icon from "@/components/icon";
import { DivPropsNoChildren } from "@/types/react";

export const LoadingSpinner = (props: DivPropsNoChildren) => (
  <div className="loading" {...props}>
    <Icon icon="CommonsPerson" />
    <Icon icon="CommonsTie" />
    <Icon icon="CommonsTie" />
  </div>
);
