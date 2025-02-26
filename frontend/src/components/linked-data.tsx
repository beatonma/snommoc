import type {
  Committee,
  ConstituencyMini,
  HouseType,
  MemberMiniSchema,
  Organisation,
  Party,
  Post,
} from "@/api";
import { ButtonProps, TextButton } from "@/components/button";
import React from "react";
import { Nullish } from "@/types/common";
import { TextLink } from "@/components/link";
import Row from "@/components/row";
import { DivPropsNoChildren } from "@/types/react";
import { addClass } from "@/util/transforms";

export const hrefFor = (
  type: "party" | "constituency" | "person",
  parliamentdotuk: number,
): string =>
  ({
    constituency: () => `/constituencies/${parliamentdotuk}/`,
    party: () => `/parties/${parliamentdotuk}/`,
    person: () => `/members/${parliamentdotuk}/`,
  })[type]();

interface DotTextProps {
  color: string | undefined;
  text: string;
}
export const DotText = (props: DotTextProps & DivPropsNoChildren) => {
  const { color, text, ...rest } = addClass(props, "items-baseline gap-1.5");
  if (!color) return <span>{text}</span>;
  return (
    <Row {...rest}>
      <span
        className="size-ch rounded-full align-middle"
        style={{ backgroundColor: color }}
      />
      <span>{text}</span>
    </Row>
  );
};

export const PartyLink = ({
  party,
  showDot = true,
  ...rest
}: {
  party: Party | Nullish;
  showDot?: boolean;
} & ButtonProps) => {
  if (!party) return null;
  const color = showDot ? party.theme?.primary : undefined;

  return (
    <TextButton href={hrefFor("party", party.parliamentdotuk)} {...rest}>
      <DotText color={color} text={party.name} />
    </TextButton>
  );
};

export const HouseLink = (props: {
  house: HouseType;
  longFormat?: boolean;
  showDot?: boolean;
}) => {
  const { house, longFormat = false, showDot = true } = props;

  const text = longFormat ? `House of ${house}` : house;
  const color = showDot
    ? {
        Commons: "var(--color-house-commons)",
        Lords: "var(--color-house-lords)",
      }[house]
    : undefined;

  return <DotText color={color} text={text} />;
};

export const PersonLink = ({
  person,
  fallback,
  ...rest
}: {
  fallback?: string;
  person: Pick<MemberMiniSchema, "name" | "parliamentdotuk"> | Nullish;
} & ButtonProps) => {
  if (!person) {
    if (fallback) return <>{fallback}</>;
    return null;
  }

  return (
    <TextButton href={hrefFor("person", person.parliamentdotuk)} {...rest}>
      {person.name}
    </TextButton>
  );
};

export const ConstituencyLink = ({
  constituency,
  ...rest
}: {
  constituency: Pick<ConstituencyMini, "name" | "parliamentdotuk"> | Nullish;
} & ButtonProps) => {
  if (!constituency) return null;

  return (
    <TextButton
      href={hrefFor("constituency", constituency.parliamentdotuk)}
      {...rest}
    >
      {constituency.name}
    </TextButton>
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
    return <TextLink href={organisation.url}>{organisation.name}</TextLink>;
  }
  return organisation.name;
};
