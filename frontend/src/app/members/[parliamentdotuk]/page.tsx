import {
  ConstituencyMini,
  HouseType,
  MemberProfile,
  MemberStatus,
  type Party,
} from "@/api";
import { PhysicalAddress } from "@/app/members/components/address";
import React, { ComponentPropsWithoutRef, ReactNode } from "react";
import { MemberPortrait } from "@/components/member-portrait";
import type { Metadata, ResolvingMetadata } from "next";
import ErrorMessage from "@/components/error";
import { getMember } from "@/api";
import { TextButton } from "@/components/button";
import { addClass } from "@/util/transforms";
import { OptionalDiv, OptionalSpan } from "@/components/optional";
import { HeaderCard } from "@/components/card";
import { LinkGroup } from "@/components/link";
import { Nullish } from "@/types/common";
import { Date } from "@/components/datetime";
import { partyStyle } from "@/components/themed/party";
import PageContent from "@/components/page";

type PageProps = {
  params: Promise<{ parliamentdotuk: number }>;
};

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
    <PageContent style={partyStyle(member.party)}>
      <main className="readable">
        <MemberCard member={member} />

        <MemberDetail member={member} className="p-2" />
        <MemberCareer member={member} className="p-2" />
      </main>
    </PageContent>
  );
}

interface MemberComponentProps extends ComponentPropsWithoutRef<"section"> {
  member: MemberProfile;
}

const MemberCard = (props: MemberComponentProps) => {
  const { member, ...rest } = addClass(props, "flex-col");

  return (
    <section {...rest}>
      <HeaderCard
        party={member.party}
        image={
          <MemberPortrait
            name={member.name}
            src={member.portrait?.wide}
            aspectClassName="aspect-[3/2]"
            className="[:has(>img)]:w-full h-[220px] bg-surface-900/10 sm:w-auto"
          />
        }
      >
        <h1>{member.name}</h1>

        <LinkGroup links={[...member.address.web, member.wikipedia]} />

        <div>
          <OptionalDiv value={member.current_posts} title="Current post" />

          <div className="flex flex-wrap gap-1">
            <Party party={member.party} />
            <Status
              status={member.status}
              house={member.house}
              constituency={member.constituency}
              lordType={member.lord_type}
            />
          </div>
        </div>
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
  status: MemberStatus;
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
            Inactive since{" "}
            <Date date={it} dateFormat={{ month: "long", year: "numeric" }} />
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
    <>
      {titleParts}
      {inactivityStatus}
    </>
  );
};

const MemberDetail = (props: MemberComponentProps) => {
  const { member, ...rest } = props;
  return (
    <section {...rest}>
      <h2 className="py-2">Contact</h2>
      <div className="flex gap-4 overflow-x-auto">
        {member.address.physical.map((it) => (
          <PhysicalAddress key={it.address} className="shrink-0 p-1" {...it} />
        ))}
      </div>
    </section>
  );
};

const MemberCareer = (props: MemberComponentProps) => {
  const { member, ...rest } = props;
  return <section {...rest}>todo member career</section>;
};
