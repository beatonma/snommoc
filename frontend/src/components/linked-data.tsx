import type {
  Committee,
  ConstituencyMini,
  HouseType,
  MemberMiniSchema,
  Organisation,
  Party,
  Post,
} from "@/api";
import { TextButton } from "@/components/button";
import React from "react";
import { Nullish } from "@/types/common";
import { TextLink } from "@/components/link";

interface DotTextProps {
  color: string | undefined;
  text: string;
}
const DotText = (props: DotTextProps) => {
  const { color, text } = props;
  if (!color) return <span>{text}</span>;
  return (
    <div className="flex items-baseline gap-1.5">
      <span
        className="size-[1ch] rounded-full align-middle"
        style={{ backgroundColor: color }}
      />
      <span>{text}</span>
    </div>
  );
};

export const PartyLink = ({
  party,
  showDot = true,
}: {
  party: Party | Nullish;
  showDot?: boolean;
}) => {
  if (!party) return null;
  const color = showDot ? party.theme?.primary : undefined;

  return (
    <TextButton href={`/parties/${party.parliamentdotuk}/`}>
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
}: {
  fallback?: string;
  person: MemberMiniSchema | Nullish;
}) => {
  if (!person) {
    if (fallback) return <>{fallback}</>;
    return null;
  }

  return (
    <TextButton href={`/members/${person.parliamentdotuk}/`}>
      {person.name}
    </TextButton>
  );
};

export const ConstituencyLink = ({
  constituency,
}: {
  constituency: Pick<ConstituencyMini, "name" | "parliamentdotuk"> | Nullish;
}) => {
  if (!constituency) return null;

  return (
    <TextButton href={`/constituencies/${constituency.parliamentdotuk}/`}>
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
