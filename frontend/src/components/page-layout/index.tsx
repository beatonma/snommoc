import React, {
  CSSProperties,
  ComponentPropsWithoutRef,
  JSX,
  ReactNode,
  useMemo,
} from "react";
import { onlyIf } from "@/components/optional";
import { DivProps } from "@/types/react";
import { classes } from "@/util/transforms";
import "./page-layout.css";

interface PageLayoutDefinition {
  className: string;
  defaultConstraints: ContentConstraints;
}
type PageLayout = "PrimarySecondary" | "CenteredReadable" | "CenteredFeed";
export const PageLayouts: Record<PageLayout, PageLayoutDefinition> = {
  /** Wide main content */
  CenteredFeed: {
    className: "grid-centered-feed",
    defaultConstraints: {
      main: {
        max: "var(--spacing-max-grid-width)",
        min: 0,
      },
    },
  },

  /** Narrow main content for comfortable reading  */
  CenteredReadable: {
    className: "grid-centered-readable",
    defaultConstraints: {
      main: {
        max: "var(--spacing-readable)",
        min: 0,
      },
    },
  },

  /** Two-paned content */
  PrimarySecondary: {
    className: "grid-primary-secondary",
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
interface PageLayoutProps {
  layout: PageLayout;

  children?: ReactNode;
  secondary?: ReactNode;
  sidebarLeft?: ReactNode;
  sidebarRight?: ReactNode;

  mainElement?: keyof JSX.IntrinsicElements;
  mainClassName?: string;

  constraints?: ContentConstraints;
}
export default function PageLayout(props: DivProps<PageLayoutProps>) {
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

  const layout = PageLayouts[layoutName]!;
  const constraints: CSSProperties = useMemo(
    () => constraintsToStyle(_constraints ?? layout.defaultConstraints),
    [_constraints, layout.defaultConstraints],
  );

  return (
    <div className="page-layout--wrapper" style={constraints}>
      <div className={classes(layout.className, className)} {...rest}>
        <CustomElement
          elementName={mainElement}
          className={classes(mainClassName, "page-layout--main")}
        >
          {children}
        </CustomElement>
        <div className="page-layout--secondary">{secondary}</div>

        <div className="page-layout--sidebar-container contents">
          <div className="page-layout--sidebar-left">{sidebarLeft}</div>
          <div className="page-layout--sidebar-right">{sidebarRight}</div>
        </div>
      </div>
    </div>
  );
}

const CustomElement = <T extends keyof JSX.IntrinsicElements>(
  props: { elementName: T } & ComponentPropsWithoutRef<T>,
) => {
  const { elementName, ...rest } = props;

  return React.createElement(elementName, rest);
};

const constraintsToStyle = (
  constraints: ContentConstraints | undefined,
): CSSProperties => {
  const main = onlyIf(constraints?.main, (it) => ({
    "--page-layout--main-content--minwidth": it.min,
    "--page-layout--main-content--maxwidth": it.max,
  }));
  const secondary = onlyIf(constraints?.secondary, (it) => ({
    "--page-layout--secondary-content--minwidth": it.min,
    "--page-layout--secondary-content--maxwidth": it.max,
  }));

  return { ...main, ...secondary } as CSSProperties;
};
