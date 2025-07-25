import type { Metadata, ResolvingMetadata } from "next";
import React, { ReactNode } from "react";
import { getOr404 } from "@/api";
import type { ConstituencyMini, HouseType, MemberProfile } from "@/api/schema";
import { FullCareer } from "@/app/(default-layout)/members/[parliamentdotuk]/_components/career";
import { PhysicalAddress } from "@/app/(default-layout)/members/_components/address";
import { Date } from "@/components/datetime";
import { OptionalDiv, OptionalSpan, onlyIf } from "@/components/optional";
import { ContentLayout } from "@/components/page-layout";
import { HeaderCard } from "@/features/cards";
import { ConstituencyLink, PartyLink } from "@/features/linked-data";
import {
  MemberPortrait,
  ParliamentThumbnailSize,
} from "@/features/member-portrait";
import { itemThemeCss } from "@/features/themed/item-theme";
import { WebLinks } from "@/features/weblinks";
import { Nullish } from "@/types/common";
import { Props } from "@/types/react";
import { addClass } from "@/util/transforms";

type PageProps = {
  params: Promise<{ parliamentdotuk: number }>;
};

const getMember = async (parliamentdotuk: number) =>
  getOr404("/api/members/{parliamentdotuk}/", {
    path: { parliamentdotuk },
  });

export async function generateMetadata(
  { params }: PageProps,
  parent: ResolvingMetadata,
): Promise<Metadata> {
  const parliamentdotuk = (await params).parliamentdotuk;
  const member = await getMember(parliamentdotuk);
  const parentTitle = (await parent).title?.absolute;
  return {
    title: member ? `${member.name} - ${parentTitle}` : parentTitle,
    description: `Member profile`,
  };
}

export default async function MemberProfilePage({ params }: PageProps) {
  const parliamentdotuk = (await params).parliamentdotuk;
  const member = await getMember(parliamentdotuk);

  return (
    <main className="space-y-8">
      <ContentLayout
        layout="CenteredReadable"
        mainElement="div"
        style={itemThemeCss(member.party)}
      >
        <MemberCard member={member} />
        <MemberDetail member={member} className="px-edge" />
      </ContentLayout>

      <ContentLayout
        layout="CenteredFeed"
        mainElement="div"
        style={itemThemeCss(member.party)}
      >
        <FullCareer parliamentdotuk={member.parliamentdotuk} />
      </ContentLayout>
    </main>
  );
}

type MemberComponentProps = Props<"section", { member: MemberProfile }>;

const MemberCard = (props: MemberComponentProps) => {
  const { member, ...rest } = addClass(props, "column");

  return (
    <section {...rest}>
      <HeaderCard
        themeSource={member.party}
        inlineImage={onlyIf(member.portrait, (portrait) => (
          <a href={portrait.full ?? undefined}>
            <MemberPortrait
              name={member.name}
              src={portrait.wide}
              aspect="aspect-wide"
              width={ParliamentThumbnailSize}
              className="max-sm:hidden"
              priority
            />
          </a>
        ))}
        hero={onlyIf(member.portrait, (portrait) => (
          <a href={portrait.full ?? undefined}>
            <MemberPortrait
              name={member.name}
              src={portrait.full}
              aspect="aspect-wide"
              width={640}
              className="sm:hidden object-top"
              priority
            />
          </a>
        ))}
      >
        <h1>{member.name}</h1>

        <WebLinks links={[...member.address.web, member.wikipedia]} />

        <div className="flex flex-wrap gap-1">
          <PartyLink title="Party" party={member.party} />
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
        <ConstituencyLink title="Constituency" constituency={constituency} />,
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
            Inactive since <Date date={it} dateFormat="Short" />
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
