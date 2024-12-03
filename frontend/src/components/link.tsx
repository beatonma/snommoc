import React from "react";
import { addClass } from "@/util/react";
import Link from "next/link";
import { LinkProps } from "next/dist/client/link";

/**
 * Props signature for next/link Link component.
 */
type NextLinkProps = Omit<
  React.AnchorHTMLAttributes<HTMLAnchorElement>,
  keyof LinkProps
> &
  LinkProps &
  React.RefAttributes<HTMLAnchorElement>;

export const StyledLink = (props: NextLinkProps) => {
  const styledProps = addClass(
    props,
    "transition-colors",
    "text-accent-900 hover:text-accent-800",
    "dark:text-accent-200 dark:hover:text-accent-300",
  );

  return <Link {...styledProps} />;
};
