import React, { CSSProperties, ElementType, ReactNode, useMemo } from "react";
import { onlyIf } from "@/components/optional";
import { DivProps, Props } from "@/types/react";
import { classes } from "@/util/transforms";
import styles from "./content-layout.module.css";

interface ContentLayoutDefinition {
  className: string | undefined;
  defaultConstraints: ContentConstraints;
}
type ContentLayout = "PrimarySecondary" | "CenteredReadable" | "CenteredFeed";
const ContentLayouts: Record<ContentLayout, ContentLayoutDefinition> = {
  /** Wide main content */
  CenteredFeed: {
    className: styles.centeredFeed,
    defaultConstraints: {
      main: {
        max: "var(--spacing-max-grid-width)",
        min: 0,
      },
    },
  },

  /** Narrow main content for comfortable reading  */
  CenteredReadable: {
    className: styles.centeredReadable,
    defaultConstraints: {
      main: {
        max: "var(--spacing-readable)",
        min: 0,
      },
    },
  },

  /** Two-paned content */
  PrimarySecondary: {
    className: styles.primarySecondary,
    defaultConstraints: {
      secondary: {
        max: "30%",
        min: 0,
      },
    },
  },
};

interface Constraints {
  min: string | 0;
  max: string | 0;
}
interface ContentConstraints {
  main?: Constraints;
  secondary?: Constraints;
}
interface ContentLayoutProps {
  layout: ContentLayout;

  children?: ReactNode;
  secondary?: ReactNode;
  sidebarLeft?: ReactNode;
  sidebarRight?: ReactNode;

  mainElement?: ElementType;
  mainClassName?: string;

  constraints?: ContentConstraints;
}

export const ContentLayout = (props: DivProps<ContentLayoutProps>) => {
  const {
    layout: layoutName,
    className,
    children,
    secondary,
    sidebarLeft,
    sidebarRight,
    mainElement = "main",
    mainClassName,
    constraints: _constraints,
    ...rest
  } = props;

  const layout = ContentLayouts[layoutName]!;
  const constraints: CSSProperties = useMemo(
    () => constraintsToStyle(_constraints ?? layout.defaultConstraints),
    [_constraints, layout.defaultConstraints],
  );

  return (
    <div className={styles.contentLayoutWrapper} style={constraints}>
      <div className={classes(layout.className, className)} {...rest}>
        <CustomElement
          elementName={mainElement}
          className={classes(mainClassName, styles.main)}
        >
          {children}
        </CustomElement>
        <div className={styles.secondary}>{secondary}</div>

        <div className="contents">
          <div className={styles.sidebarLeft}>{sidebarLeft}</div>
          <div className={styles.sidebarRight}>{sidebarRight}</div>
        </div>
      </div>
    </div>
  );
};

const CustomElement = <T extends ElementType>(
  props: Props<T, { elementName: T }>,
) => {
  const { elementName, ...rest } = props;

  return React.createElement(elementName, rest);
};

const constraintsToStyle = (
  constraints: ContentConstraints | undefined,
): CSSProperties => {
  const main = onlyIf(constraints?.main, (it) => ({
    "--content-layout--main-content--minwidth": it.min,
    "--content-layout--main-content--maxwidth": it.max,
  }));
  const secondary = onlyIf(constraints?.secondary, (it) => ({
    "--content-layout--secondary-content--minwidth": it.min,
    "--content-layout--secondary-content--maxwidth": it.max,
  }));

  return { ...main, ...secondary } as CSSProperties;
};

export const _private = {
  PageLayouts: ContentLayouts,
};
