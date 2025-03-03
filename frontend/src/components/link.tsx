"use client";
import React, {
  ComponentPropsWithoutRef,
  HTMLAttributeReferrerPolicy,
  useState,
} from "react";
import { addClass } from "@/util/transforms";
import Link from "next/link";
import { LinkProps } from "next/dist/client/link";
import { ButtonLinkProps, TextButton } from "@/components/button";
import { AppIcon } from "@/components/icon";
import { WebAddress } from "@/api";
import { Nullish } from "@/types/common";

/**
 * Props signature for next/link Link component.
 */
export type NextLinkProps = Omit<
  React.AnchorHTMLAttributes<HTMLAnchorElement>,
  keyof LinkProps
> &
  LinkProps &
  React.RefAttributes<HTMLAnchorElement>;

export const TextLink = (props: NextLinkProps) => {
  const styledProps = addClass(
    props,
    "transition-colors",
    "text-primary hover:text-mix_primary_current",
  );

  return (
    <Link
      referrerPolicy="same-origin"
      rel="noopener nofollow"
      {...styledProps}
    />
  );
};

type LinkGroupProps = {
  links?: (string | WebAddress | null)[];
} & ComponentPropsWithoutRef<"div">;
export const LinkGroup = (props: LinkGroupProps) => {
  const { links, children, ...rest } = addClass(
    props,
    "flex flex-row flex-wrap gap-x-4 gap-y-0",
  );

  if (links) {
    return (
      <div {...rest}>
        {links.map((it, index) => {
          if (it != null && typeof it === "object") {
            return (
              <ButtonLink
                key={index}
                href={it.url}
                defaultDisplayText={it.description}
              />
            );
          }
          return <ButtonLink key={index} href={it} />;
        })}
      </div>
    );
  }

  return <div {...rest}>{children}</div>;
};

export const ButtonLink = (
  props: ButtonLinkProps & { defaultDisplayText?: string | null },
) => {
  const { href, defaultDisplayText, icon, ...rest } = addClass(props, "w-fit");
  const values = resolveLinkValues(href, icon, defaultDisplayText);

  if (!href) return null;
  if (!values) return null;

  const linkProps = {
    target: "_blank",
    referrerPolicy: "same-origin" as HTMLAttributeReferrerPolicy,
    rel: "noopener nofollow",
  };

  if (values.confirmAction)
    return <ConfirmButtonLink values={values} {...rest} {...linkProps} />;

  if (!values.confirmAction) {
    return (
      <TextButton
        icon={icon ?? values.icon}
        href={values.url}
        title={values.title}
        {...rest}
        {...linkProps}
      >
        {values.displayText}
      </TextButton>
    );
  }
};

const ConfirmButtonLink = (
  props: Omit<ButtonLinkProps, "href" | "icon"> & {
    values: ResolvedLinkValues;
  },
) => {
  const { values, ...rest } = props;
  const [isExpanded, setIsExpanded] = useState<boolean>(false);

  const content = isExpanded ? (
    <>
      <div className="flex items-center justify-between gap-x-4">
        <TextButton icon={values.icon}>{values.displayText}</TextButton>
        <TextButton
          icon="Close"
          onClick={() => setIsExpanded(false)}
        ></TextButton>
      </div>
      <TextButton
        href={values.url}
        title={values.title}
        {...addClass(rest, "text-primary self-end")}
      >
        {values.confirmAction}
      </TextButton>
    </>
  ) : (
    <TextButton
      icon={values.icon}
      onClick={() => setIsExpanded(true)}
      title={values.title}
      {...rest}
    >
      {values.displayText}
    </TextButton>
  );

  const expandedClasses = isExpanded ? "card surface min-w-48 p-2" : "";

  return (
    <div className={`${expandedClasses} column gap-2 transition-all`}>
      {content}
    </div>
  );
};

interface WebHost {
  pattern: RegExp;
  icon: AppIcon;
  title: string;
  confirmAction?: {
    confirmationMessage: string;
  };

  /**
   * A function which edits the <display> capture group to make it suitable as displayText.
   */
  clean?: (display: string | undefined) => string | undefined;

  /**
   * A function which edits the given URL to make sure it is valid.
   */
  cleanUrl?: (url: string) => string;
}
interface ResolvedLinkValues {
  url: string;
  title: string | undefined;
  displayText: string | undefined;
  icon: AppIcon | undefined;
  confirmAction: string | undefined;
}
const WebHosts: WebHost[] = [
  {
    title: "Twitter / X",
    pattern: /(https:\/\/)?(www\.)?(x|twitter)\.com\/(?<display>[\w.-]+).*/,
    icon: "Twitter",
  },
  {
    title: "Facebook",
    pattern: /(https:\/\/)?(www\.)?facebook\.com\/(?<display>[\w.-]+).*/,
    icon: "Facebook",
  },
  {
    title: "Instagram",
    pattern: /(https:\/\/)?(www\.)?instagram\.com\/(?<display>[\w.-]+).*/,
    icon: "Instagram",
  },
  {
    title: "Email",
    pattern: /mailto:(?<display>.+)/,
    icon: "Email",
    confirmAction: {
      confirmationMessage: "Write an email",
    },
  },
  {
    title: "Phone",
    pattern: /tel:(?<display>.+)/,
    icon: "Phone",
    confirmAction: {
      confirmationMessage: "Call",
    },
    cleanUrl: (url) => url.replaceAll(/\s/g, ""),
  },
  {
    title: "Fax",
    pattern: /fax:(?<display>.+)/,
    icon: "Fax",
    confirmAction: {
      confirmationMessage: "Send a fax",
    },
  },
  {
    title: "Wikipedia",
    pattern: /(https:\/\/)?(\w+\.)?wikipedia\.org\/wiki\/(?<display>.+)/,
    icon: "Wikipedia",
    clean: (display) =>
      display?.replaceAll("_", " ")?.replace("(UK)", "")?.trim(),
  },
  {
    title: "Website",
    pattern: /(https:\/\/)?(www\.)?(?<display>[\w.-]+\.(org|com|co.uk))\/?/,
    icon: "Home",
  },
  {
    title: "Debug",
    pattern: /#/,
    icon: "Commons",
    confirmAction: {
      confirmationMessage: "Confirm?",
    },
  },
];
const resolveLinkValues = (
  url: string | Nullish,
  icon: AppIcon | undefined,
  defaultDisplayText: string | Nullish,
): ResolvedLinkValues | null => {
  if (!url) return null;

  let cleanUrl: string = url;
  let displayText: string | undefined;
  let hostIcon: AppIcon | undefined;
  let title: string | undefined;
  let confirmAction: string | undefined;

  for (const host of WebHosts) {
    const match = host.pattern.exec(url);
    if (!match) continue;

    displayText = match.groups?.["display"] ?? defaultDisplayText ?? host.title;
    if (host.clean) {
      displayText = host.clean(displayText);
    }
    if (host.cleanUrl) {
      cleanUrl = host.cleanUrl(cleanUrl);
    }
    hostIcon = host.icon;
    title = host.title ?? defaultDisplayText;
    confirmAction = host.confirmAction?.confirmationMessage;

    break;
  }

  if (!displayText) {
    displayText = URL.parse(url)?.hostname?.replace("www.", "");
  }

  return {
    url: cleanUrl,
    title: title,
    displayText: displayText,
    icon: icon ?? hostIcon,
    confirmAction: confirmAction,
  };
};
