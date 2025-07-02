import Icon from "@/components/icon";
import { DivPropsNoChildren } from "@/types/react";
import styles from "./loading-spinner.module.css";

export const LoadingSpinner = (props: DivPropsNoChildren) => (
  <div className={styles.loadingSpinner} {...props}>
    <Icon icon="CommonsPerson" />
    <Icon icon="CommonsTie" />
    <Icon icon="CommonsTie" />
  </div>
);
