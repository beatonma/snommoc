import { OptionalDiv } from "@/components/optional";
import { MemberPortrait } from "@/components/member-portrait";
import React from "react";
import Link from "next/link";
import { PartyIconBackground } from "@/components/themed/party";
import type { Metadata } from "next";
import { getMembers, MemberMiniSchema } from "@/api";
import ErrorMessage from "@/components/error";
import { resolveUrl } from "@/env";

export const metadata: Metadata = {
  title: "Members",
  description: "Members list",
};

export default async function Page() {
  const response = await getMembers();
  const members = response.data?.items;

  if (!members) return <ErrorMessage />;

  return (
    <main>
      <a href={resolveUrl("/api/members/")} target="_blank">
        api
      </a>

      <div className="m-2 mb-96 grid grid-cols-[repeat(auto-fit,minmax(300px,400px))] justify-center gap-x-12 gap-y-4">
        {members.map((member) => (
          <Member key={member.parliamentdotuk} {...member} />
        ))}
      </div>
    </main>
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
          className="w-16 shrink-0 rounded-md bg-primary-900"
        />
        <div className="flex flex-col gap-0.5 [&>div]:text-sm">
          <h2 className="text-xl font-semibold">{props.name}</h2>
          <OptionalDiv
            title="Current post"
            condition={props.current_post}
            className="line-clamp-1"
          />
          <div className="separated flex">
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
