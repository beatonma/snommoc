import { Fragment } from "react";
import { BillDetail } from "@/api/schema";
import { InlineLink } from "@/components/button";
import { Chip } from "@/components/chip";
import { Date } from "@/components/datetime";
import { Html } from "@/components/hooks/html";
import { onlyIf } from "@/components/optional";
import { Prose } from "@/components/prose";
import { Row, SeparatedRow } from "@/components/row";
import { MemberItemCard } from "@/features/cards";
import { OrganisationItemCard } from "@/features/cards/list-item";
import { HouseLink } from "@/features/linked-data";
import { DivPropsNoChildren, Props } from "@/types/react";

export const Sponsors = (
  props: DivPropsNoChildren<{
    sponsors: BillDetail["sponsors"];
  }>,
) => {
  const { sponsors, ...rest } = props;
  return (
    <div {...rest}>
      <h2 className="prose-h3">Sponsors</h2>

      <Row
        overflow="scroll"
        className="gap-x-4 narrow-cards"
        vertical="items-start"
      >
        {sponsors.map((it) => (
          <Fragment key={it.id}>
            {onlyIf(it.profile, (profile) => (
              <MemberItemCard member={profile} layout="hero" />
            ))}
            {onlyIf(it.organisation, (org) => (
              <OrganisationItemCard organisation={org} />
            ))}
          </Fragment>
        ))}
      </Row>
    </div>
  );
};

export const BillType = (
  props: DivPropsNoChildren<{ type: BillDetail["type"] }>,
) => {
  const { type, ...rest } = props;
  const { name, description, category } = type;

  return (
    <Prose {...rest}>
      <Row overflow="wrap" vertical="items-baseline" className="gap-x-2">
        <strong title="Bill type">{name}</strong>
      </Row>

      <Html html={description} />
    </Prose>
  );
};

type Stage = BillDetail["stages"][number];
export const Stages = (
  props: DivPropsNoChildren<{
    current: BillDetail["current_stage"];
    stages: Stage[];
  }>,
) => {
  const { current, stages, ...rest } = props;
  return (
    <div {...rest}>
      {stages.map((it, index) => (
        <Stage key={index} stage={it} />
      ))}
    </div>
  );
};
const Stage = (props: DivPropsNoChildren<{ stage: Stage }>) => {
  const { stage, ...rest } = props;
  return (
    <div {...rest}>
      <span>
        {stage.house && (
          <>
            <HouseLink house={stage.house} />
            {": "}
          </>
        )}
        <strong>{stage.description}</strong>
      </span>

      {stage.sittings.length && (
        <ul className="ps-2">
          {stage.sittings.map((it) => (
            <li key={it}>
              <Date key={it} date={it} />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

type Session = BillDetail["sessions"][number];
export const Sessions = (
  props: DivPropsNoChildren<{
    introduced: BillDetail["session_introduced"];
    sessions: Session[];
  }>,
) => {
  const { introduced: introduced, sessions, ...rest } = props;

  return (
    <div {...rest}>
      {sessions.map((it) => (
        <Session key={it.parliamentdotuk} session={it} />
      ))}
    </div>
  );
};
const Session = (props: DivPropsNoChildren<{ session: Session }>) => {
  const { session, ...rest } = props;
  return (
    <div {...rest}>
      {session.name || `Unnamed session #${session.parliamentdotuk}`}
    </div>
  );
};

type Publication = BillDetail["publications"][number];
export const Publications = (
  props: DivPropsNoChildren<{
    publications: BillDetail["publications"];
  }>,
) => {
  const { publications, ...rest } = props;
  return (
    <div {...rest}>
      {publications.map((it) => (
        <Publication key={it.parliamentdotuk} publication={it} />
      ))}
    </div>
  );
};
const Publication = (
  props: DivPropsNoChildren<{ publication: Publication }>,
) => {
  const { publication, ...rest } = props;
  return (
    <div {...rest}>
      <SeparatedRow className="text-sm text-reduced">
        <div>{publication.type}</div>
        <Date date={publication.date} />

        {onlyIf(publication.links.length > 0, () => (
          <Row overflow="wrap" className="gap-x-2 colorful-links">
            {publication.links.map((link) => (
              <InlineLink key={link.url} href={link.url}>
                <ContentType contentType={link.content_type} />
              </InlineLink>
            ))}
          </Row>
        ))}
      </SeparatedRow>

      <div>{publication.title}</div>
    </div>
  );
};
const ContentType = ({
  contentType,
}: {
  contentType: Publication["links"][number]["content_type"];
}) => {
  switch (contentType) {
    case "text/html":
      return "HTML";
    case "application/pdf":
      return "PDF";
    default:
      return contentType;
  }
};

export const IsAct = (
  props: Props<typeof Chip, { isAct: BillDetail["is_act"] }, "children">,
) => {
  const { isAct, ...rest } = props;
  return onlyIf(isAct, <Chip {...rest}>Act</Chip>);
};

export const IsDefeated = (
  props: Props<
    typeof Chip,
    { isDefeated: BillDetail["is_defeated"] },
    "children"
  >,
) => {
  const { isDefeated, ...rest } = props;
  return onlyIf(isDefeated, <Chip {...rest}>Act</Chip>);
};

export const DateWithdrawn = (
  props: Props<
    "span",
    {
      dateWithdrawn: BillDetail["date_withdrawn"];
    },
    "children"
  >,
) => {
  const { dateWithdrawn, ...rest } = props;
  return onlyIf(
    dateWithdrawn,
    <span {...rest}>
      Withdrawn <Date date={dateWithdrawn} />
    </span>,
  );
};
