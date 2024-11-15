import { ConstituencyMini, MemberProfile, type Party } from "@/api";
import { PhysicalAddress, WebAddress } from "@/components/address";
import React, { ComponentPropsWithoutRef } from "react";
import { PartyIconBackground } from "@/components/themed/party";
import { MemberPortrait } from "@/components/member-portrait";
import type { Metadata, ResolvingMetadata } from "next";
import ErrorMessage from "@/components/error";
import { getMember } from "@/api";
import { TextButton } from "@/components/button";
import { classes } from "@/util/react";
import { OptionalDiv } from "@/components/optional";

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

  console.log(`member: ${member} | ${response.error}`);

  if (!member) return <ErrorMessage />;

  return (
    <div>
      <main className="flex flex-col">
        <MemberCard member={member} className="flex items-center" />

        <MemberDetail member={member} className="p-2" />
        <MemberCareer member={member} className="p-2" />
      </main>

      <a href={`/api/members/${member.parliamentdotuk}/`} target="_blank">
        api
      </a>
    </div>
  );
}

interface MemberComponentProps extends ComponentPropsWithoutRef<"section"> {
  member: MemberProfile;
}

const MemberCard = (props: MemberComponentProps) => {
  const { member, className, ...rest } = props;

  return (
    <section className={classes(className, "flex-col")} {...rest}>
      <PartyIconBackground
        party={member.party}
        className="flex min-w-full flex-col gap-4 p-2 sm:min-w-[60vw] sm:max-w-[80vw] sm:flex-row sm:rounded-lg sm:p-4"
      >
        <MemberPortrait
          name={member.name}
          src={member.portrait?.wide}
          aspectClassName="aspect-[3/2]"
          className="[:has(>img)]:w-full h-[220px] self-center overflow-hidden rounded-lg bg-surface-900/10 sm:w-auto"
        />

        <div className="flex flex-col gap-1">
          <h1 className="sm:w-max">{member.name}</h1>

          <div className="flex flex-wrap gap-x-4">
            {member.address.web.map((addr) => (
              <WebAddress
                key={addr.url}
                url={addr.url}
                description={addr.description}
              />
            ))}
          </div>

          <div>
            <OptionalDiv condition={member.current_post} title="Current post" />

            <div className="flex gap-1">
              <Party party={member.party} />
              <MpStatus
                active={member.active}
                house={member.house}
                constituency={member.constituency}
              />
            </div>
          </div>
        </div>
      </PartyIconBackground>
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

const MpStatus = ({
  active,
  house,
  constituency,
}: {
  active: boolean;
  house: string | null | undefined;
  constituency: ConstituencyMini | null;
}) => {
  if (!active || house?.toLowerCase() !== "commons") return null;

  if (!constituency) return <span>MP</span>;

  return (
    <span>
      MP for{" "}
      <TextButton
        title="Constituency"
        href={`/constituencies/${constituency.parliamentdotuk}/`}
      >
        {constituency.name}
      </TextButton>
    </span>
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
