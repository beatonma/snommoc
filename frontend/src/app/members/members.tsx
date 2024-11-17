"use client";
import { getMembers, type MemberMiniSchema } from "@/api";
import Link from "next/link";
import { PartyIconBackground } from "@/components/themed/party";
import { MemberPortrait } from "@/components/member-portrait";
import { OptionalDiv } from "@/components/optional";
import React from "react";
import { SearchListPage } from "@/components/page/list-page";

export default function MembersList() {
  return (
    <SearchListPage
      loader={getMembers}
      itemComponent={(member) => (
        <Member key={member.parliamentdotuk} {...member} />
      )}
    />
  );
}

const Member = (props: MemberMiniSchema) => {
  return (
    <Link
      href={`/members/${props.parliamentdotuk}/`}
      className="flex overflow-hidden sm:rounded-lg"
    >
      <PartyIconBackground party={props.party} className="flex grow gap-3 p-3">
        <MemberPortrait
          name={props.name}
          src={props.portrait}
          className="w-16 shrink-0 overflow-hidden rounded-md bg-primary-900"
        />
        <div className="flex flex-col gap-0.5 [&>div]:text-sm">
          <h2 className="text-xl font-semibold">{props.name}</h2>
          <OptionalDiv
            title="Current post"
            condition={props.current_post}
            className="line-clamp-1"
          />
          <div className="separated flex flex-wrap">
            <OptionalDiv
              title="Party"
              condition={props.party?.name}
              className="line-clamp-1"
            />
            <OptionalDiv
              title="Constituency"
              condition={props.constituency?.name}
              className="line-clamp-1"
            />
          </div>
        </div>
      </PartyIconBackground>
    </Link>
  );
};
