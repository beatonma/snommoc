"use client";
import { InfiniteScroll, PaginationLoader } from "@/components/pagination";
import { getMembers, MemberMiniSchema } from "@/api";
import Link from "next/link";
import { PartyIconBackground } from "@/components/themed/party";
import { MemberPortrait } from "@/components/member-portrait";
import { OptionalDiv } from "@/components/optional";
import React, { useEffect, useRef, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";

const QueryParam = "query";

export default function MembersList() {
  const router = useRouter();
  const search = useSearchParams();
  const [query, setQuery] = useState<string>(search.get(QueryParam) ?? "");
  const activeQuery = useRef(query);
  const [resetFlag, setResetFlag] = useState<boolean>();

  useEffect(() => {
    const q = search.get(QueryParam) ?? "";
    if (q === activeQuery.current) return;
    setQuery(q);
    activeQuery.current = q;
    setResetFlag((it) => !it);
  }, [search]);

  return (
    <div>
      <form
        className="flex justify-center gap-2 p-4"
        action={() => {
          activeQuery.current = query;
          router.push(`?${QueryParam}=${query}`);
          setResetFlag((it) => !it);
        }}
      >
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit">Search</button>
      </form>

      <PaginatedMembersList
        loader={(offset) => getMembers(offset, activeQuery.current)}
        resetFlag={resetFlag}
      />
    </div>
  );
}

const PaginatedMembersList = (props: {
  loader: PaginationLoader<MemberMiniSchema>;
  resetFlag?: boolean;
}) => {
  return (
    <InfiniteScroll
      loader={props.loader}
      resetFlag={props.resetFlag}
      className="m-2 mb-96 grid grid-cols-[repeat(auto-fit,minmax(300px,400px))] justify-center gap-x-12 gap-y-4"
      itemComponent={(member) => (
        <Member key={member.parliamentdotuk} {...member} />
      )}
    />
  );
};

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
