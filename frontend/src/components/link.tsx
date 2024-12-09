import React, { ComponentPropsWithoutRef } from "react";
import { addClass } from "@/util/transforms";
import Link from "next/link";
import { LinkProps } from "next/dist/client/link";
import { ButtonLinkProps, TextButton } from "@/components/button";
import type { AppIcon } from "@/components/icon";
import { WebAddress } from "@/api";

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
    "text-accent-950 hover:text-accent-800",
    "dark:text-accent-200 dark:hover:text-accent-300",
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
        {links.map((it) => {
          if (it != null && typeof it === "object") {
            return (
              <ButtonLink
                key={it?.url}
                href={it.url}
                defaultDisplayText={it.description}
              />
            );
          }
          return <ButtonLink key={it} href={it} />;
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
  if (!href) return null;

  const values = webDisplayValues(href);

  return (
    <TextButton
      icon={icon ?? values.icon}
      href={href}
      title={defaultDisplayText ?? undefined}
      {...rest}
      target="_blank"
      referrerPolicy="same-origin"
      rel="noopener nofollow"
    >
      {values.displayText ?? defaultDisplayText}
    </TextButton>
  );
};

interface WebHost {
  pattern: RegExp;
  icon: AppIcon;

  /**
   * A function which edits the <display> capture group to make it suitable as displayText.
   */
  clean?: (display: string | undefined) => string | undefined;
}
const WebHosts: WebHost[] = [
  {
    pattern: /(https:\/\/)?(www\.)?(x|twitter)\.com\/(?<display>[\w.-]+).*/,
    icon: "Twitter",
  },
  {
    pattern: /(https:\/\/)?(www\.)?facebook\.com\/(?<display>[\w.-]+).*/,
    icon: "Facebook",
  },
  {
    pattern: /(https:\/\/)?(www\.)?instagram\.com\/(?<display>[\w.-]+).*/,
    icon: "Instagram",
  },
  {
    pattern: /mailto:(?<display>.+)/,
    icon: "Email",
  },
  {
    pattern: /tel:(?<display>.+)/,
    icon: "Phone",
  },
  {
    pattern: /fax:(?<display>.+)/,
    icon: "Fax",
  },
  {
    pattern: /(https:\/\/)?(\w+\.)?wikipedia\.org\/wiki\/(?<display>.+)/,
    icon: "Wikipedia",
    clean: (display) =>
      display?.replaceAll("_", " ")?.replace("(UK)", "")?.trim(),
  },
  {
    pattern: /(https:\/\/)?(www\.)?(?<display>[\w.-]+\.(org|com|co.uk))\/?/,
    icon: "Home",
  },
];
const webDisplayValues = (
  url: string,
): {
  displayText: string | undefined;
  icon: AppIcon | undefined;
} => {
  let displayText: string | undefined;
  let icon: AppIcon | undefined;

  for (const host of WebHosts) {
    const match = host.pattern.exec(url);
    if (!match) continue;

    displayText = match.groups?.["display"];
    if (host.clean) {
      displayText = host.clean(displayText);
    }
    icon = host.icon;

    break;
  }

  if (!displayText) {
    displayText = URL.parse(url)?.hostname?.replace("www.", "");
  }

  return {
    displayText: displayText,
    icon: icon,
  };
};
