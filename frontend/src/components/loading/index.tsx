import Icon from "@/components/icon";
import { DivPropsNoChildren } from "@/types/react";
import "./loading.css";

export { LoadingBar } from "./loading-bar";

export const Loading = (props: DivPropsNoChildren) => (
  <div className="loading" {...props}>
    <Icon icon="CommonsPerson" />
    <Icon icon="CommonsTie" />
    <Icon icon="CommonsTie" />
  </div>
);
