import React from "react";
import type {
  Committee,
  ConstituencyMini,
  HouseType,
  MemberMiniSchema,
  Organisation,
  Party,
  Post,
} from "@/api/schema";
import { ButtonProps, InlineButton, InlineLink } from "@/components/button";
import { onlyIf } from "@/components/optional";
import { navigationHref } from "@/navigation";
import { Nullish } from "@/types/common";

export const PartyLink = (
  props: {
    party: Party | Nullish;
    showDot?: boolean;
  } & ButtonProps,
) => {
  const { party, title, showDot = true, ...rest } = props;
  if (!party) return null;
  const color = showDot ? party.theme?.primary : undefined;

  return (
    <InlineButton
      title={title || party.name}
      href={onlyIf(
        !("onClick" in rest),
        navigationHref("party", party.parliamentdotuk),
      )}
      iconProps={onlyIf(showDot, {
        className: "rounded-xs border-1 border-current/50",
        style: { backgroundColor: color },
      })}
      {...rest}
    >
      {party.name}
    </InlineButton>
  );
};

export const HouseLink = (
  props: {
    house: HouseType;
    longFormat?: boolean;
    showDot?: boolean;
  } & ButtonProps,
) => {
  const { house, title, longFormat = false, showDot = true } = props;

  const text = longFormat ? `House of ${house}` : house;
  const color = showDot
    ? {
        Commons: "var(--color-house-commons)",
        Lords: "var(--color-house-lords)",
      }[house]
    : undefined;

  return (
    <InlineButton
      title={title || `House of ${house}`}
      iconProps={onlyIf(showDot, {
        className: "rounded-full",
        style: { backgroundColor: color },
      })}
    >
      {text}
    </InlineButton>
  );
};

export const PersonLink = (
  props: {
    fallback?: string;
    person: Pick<MemberMiniSchema, "name" | "parliamentdotuk"> | Nullish;
  } & ButtonProps,
) => {
  const { person, fallback, title, ...rest } = props;
  if (!person) {
    if (fallback) return <>{fallback}</>;
    return null;
  }

  return (
    <InlineButton
      href={navigationHref("person", person.parliamentdotuk)}
      title={title || person.name}
      {...rest}
    >
      {person.name}
    </InlineButton>
  );
};

export const ConstituencyLink = (
  props: {
    constituency: Pick<ConstituencyMini, "name" | "parliamentdotuk"> | Nullish;
    dotColor?: string;
  } & ButtonProps,
) => {
  const { constituency, dotColor, title, ...rest } = props;
  if (!constituency) return null;

  return (
    <InlineButton
      href={navigationHref("constituency", constituency.parliamentdotuk)}
      title={title || constituency.name}
      iconProps={onlyIf(!!dotColor, {
        className: "rounded-xs border-1 border-current/50",
        style: { backgroundColor: dotColor },
      })}
      {...rest}
    >
      {constituency.name}
    </InlineButton>
  );
};

export const PostLink = ({ post }: { post: Post | Nullish }) => {
  return post?.name ?? null;
};

export const CommitteeLink = ({
  committee,
}: {
  committee: Committee | Nullish;
}) => {
  return committee?.name ?? null;
};

export const OrganisationLink = ({
  organisation,
}: {
  organisation: Organisation | Nullish;
}) => {
  if (!organisation) return null;
  if (organisation.url) {
    return <InlineLink href={organisation.url}>{organisation.name}</InlineLink>;
  }
  return organisation.name;
};
