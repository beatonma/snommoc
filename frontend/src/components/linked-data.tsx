import type { ConstituencyMini, MemberMiniSchema, Party } from "@/api";
import { TextButton } from "@/components/button";
import React from "react";
import { Nullish } from "@/types/common";
import { rgb } from "@/components/themed/party";

export const PartyLink = ({
  party,
  showDot = true,
}: {
  party: Party | Nullish;
  showDot?: boolean;
}) => {
  if (!party) return null;

  const content = showDot ? (
    <div className="flex items-center gap-1.5">
      <div
        className="size-2 rounded-full"
        style={{ backgroundColor: rgb(party.theme?.primary) }}
      ></div>
      <div>{party.name}</div>
    </div>
  ) : (
    party.name
  );

  return (
    <TextButton href={`/parties/${party.parliamentdotuk}/`}>
      {content}
    </TextButton>
  );
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
  constituency: ConstituencyMini | Nullish;
}) => {
  if (!constituency) return null;

  return (
    <TextButton href={`/constituencies/${constituency.parliamentdotuk}/`}>
      {constituency.name}
    </TextButton>
  );
};
