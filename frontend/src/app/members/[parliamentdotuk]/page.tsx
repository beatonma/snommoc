import type { Metadata, ResolvingMetadata } from "next";
import React, { ComponentPropsWithoutRef, ReactNode } from "react";
import {
  ConstituencyMini,
  HouseType,
  MemberProfile,
  type Party,
  get,
} from "@/api";
import Career from "@/app/members/[parliamentdotuk]/career";
import { PhysicalAddress } from "@/app/members/_components/address";
import { TextButton } from "@/components/button";
import { HeaderCard } from "@/components/card";
import { Date } from "@/components/datetime";
import ErrorMessage from "@/components/error";
import { LinkGroup } from "@/components/link";
import { MemberPortrait } from "@/components/models/member-portrait";
import { OptionalDiv, OptionalSpan, onlyIf } from "@/components/optional";
import PageLayout from "@/components/page-layout";
import { partyColors } from "@/components/themed/party";
import { Nullish } from "@/types/common";
import { addClass } from "@/util/transforms";

type PageProps = {
  params: Promise<{ parliamentdotuk: number }>;
};

const getMember = async (parliamentdotuk: number) =>
  get("/api/members/{parliamentdotuk}/", {
    path: { parliamentdotuk },
  });

export async function generateMetadata(
  { params }: PageProps,
  parent: ResolvingMetadata,
): Promise<Metadata> {
  const parliamentdotuk = (await params).parliamentdotuk;
  const member = (await getMember(parliamentdotuk)).data;
  const parentTitle = (await parent).title?.absolute;
  return {
    title: member ? `${member.name} - ${parentTitle}` : parentTitle,
    description: `Member profile`,
  };
}

export default async function Page({ params }: PageProps) {
  const parliamentdotuk = (await params).parliamentdotuk;
  const response = await getMember(parliamentdotuk);
  const member = response.data;

  if (!member) return <ErrorMessage />;

  return (
    <PageLayout layout="CenteredReadable" style={partyColors(member.party)}>
      <MemberCard member={member} />
      <MemberDetail member={member} className="insets-x" />
      <MemberCareer member={member} className="insets-x" />
    </PageLayout>
  );
}

interface MemberComponentProps extends ComponentPropsWithoutRef<"section"> {
  member: MemberProfile;
}

const MemberCard = (props: MemberComponentProps) => {
  const { member, ...rest } = addClass(props, "column");

  return (
    <section {...rest}>
      <HeaderCard
        party={member.party}
        image={onlyIf(member.portrait, (portrait) => (
          <a href={portrait.full ?? undefined}>
            <MemberPortrait
              name={member.name}
              src={portrait.wide}
              aspectClassName="aspect-3/2"
              className="h-[220px] sm:w-auto [:has(>img)]:w-full"
            />
          </a>
        ))}
      >
        <h1>{member.name}</h1>

        <LinkGroup links={[...member.address.web, member.wikipedia]} />

        <div className="flex flex-wrap gap-1">
          <Party party={member.party} />
          <Status
            status={member.status}
            house={member.house}
            constituency={member.constituency}
            lordType={member.lord_type}
          />
        </div>

        <CurrentPositions
          posts={member.current_posts}
          committees={member.current_committees}
        />
      </HeaderCard>
    </section>
  );
};

const Party = ({ party }: { party: Party | null }) => {
  if (!party) return null;
  return (
    <TextButton title="Party" href={`/parties/${party.parliamentdotuk}/`}>
      {party.name}
    </TextButton>
  );
};

const Status = (props: {
  status: MemberProfile["status"];
  house: HouseType | Nullish;
  constituency: ConstituencyMini | null;
  lordType: string | Nullish;
}) => {
  const { status, house, constituency, lordType } = props;

  const titleParts: ReactNode[] = [];
  if (!status.is_current) {
    titleParts.push("Former ");
  }
  if (house === "Commons") {
    titleParts.push("MP");
    if (constituency) {
      titleParts.push(
        " for ",
        <TextButton
          title="Constituency"
          href={`/constituencies/${constituency.parliamentdotuk}/`}
        >
          {constituency.name}
        </TextButton>,
      );
    }
  } else if (house === "Lords") {
    titleParts.push(`Lord - ${lordType}`);
  }

  let inactivityStatus: ReactNode;
  if (status.is_current && !status.is_active) {
    inactivityStatus = (
      <OptionalDiv
        className="basis-full"
        value={status.since}
        block={(it) => (
          <>
            Inactive since <Date date={it} />
            <OptionalSpan
              value={status.description}
              block={(it) => `: ${it}`}
            />
          </>
        )}
      />
    );
  }

  return (
    <div className="align-baseline">
      {titleParts}
      {inactivityStatus}
    </div>
  );
};

const CurrentPositions = (props: {
  posts: MemberProfile["current_posts"];
  committees: MemberProfile["current_committees"];
}) => {
  const { posts, committees } = props;

  if (!posts.length && !committees.length) {
    return null;
  }

  return (
    <div className="text-sm">
      {posts.map((post, index) => (
        <p key={index}>{post}</p>
      ))}

      {committees.map((it, index) => (
        <p key={index}>{it.name}</p>
      ))}
    </div>
  );
};

const MemberDetail = (props: MemberComponentProps) => {
  const { member, ...rest } = props;
  return (
    <section {...rest}>
      <h2>Contact</h2>
      <div className="flex max-w-full flex-wrap gap-4 overflow-x-auto">
        {member.address.physical.map((it) => (
          <PhysicalAddress key={it.address} className="shrink-0 p-1" {...it} />
        ))}
      </div>
    </section>
  );
};

const MemberCareer = (props: MemberComponentProps) => {
  const { member, ...rest } = props;
  return (
    <section {...rest}>
      <Career parliamentdotuk={member.parliamentdotuk} />
    </section>
  );
};
