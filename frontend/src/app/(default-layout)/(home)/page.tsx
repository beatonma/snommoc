import { ReactNode } from "react";
import { getOrNull } from "@/api";
import { ResponseOf } from "@/api/client";
import { Button, InlineLink } from "@/components/button";
import { Callout } from "@/components/callout";
import { useHtml } from "@/components/hooks/html";
import { LoadingSpinner } from "@/components/loading";
import { Optional } from "@/components/optional";
import { ContentLayout } from "@/components/page-layout";
import { Prose } from "@/components/prose";
import { Row } from "@/components/row";
import { DivisionItemCard, MemberItemCard } from "@/features/cards";
import { BillItemCard } from "@/features/cards/list-item";
import { navigationHref } from "@/navigation";
import { DivProps, DivPropsNoChildren } from "@/types/react";
import { addClass, classes } from "@/util/transforms";
import styles from "./home.module.css";

type Zeitgeist = ResponseOf<"/api/zeitgeist/">;
type ServerMessage = Zeitgeist["motd"][number];
type Person = Zeitgeist["people"][number];
type Division = Zeitgeist["divisions"][number];
type Bill = Zeitgeist["bills"][number];

export const dynamic = "force-dynamic";

export default async function Home() {
  const zeitgeist = await getOrNull("/api/zeitgeist/");

  if (!zeitgeist) return <LoadingSpinner />;
  const { people, divisions, bills, motd } = zeitgeist;

  return (
    <ContentLayout layout="CenteredFeed">
      <ServerMessages messages={motd} />

      <section>
        <Prose className="card card-content surface mx-auto">
          <h2>Welcome</h2>

          <p>
            The site you are viewing now is for{" "}
            <strong>demo purposes only</strong>. You are welcome to look around
            but beware that data is incomplete and not scheduled for regular
            updates because, for demo purposes, that would just be a waste of
            electricity. User accounts are also disabled.
          </p>

          <p>
            For more information on Commons see{" "}
            <InlineLink href={navigationHref("about")}>here</InlineLink>.
          </p>

          <p>
            Feel free to{" "}
            <InlineLink href="https://beatonma.org/contact/">
              contact me
            </InlineLink>{" "}
            if you have any comments or suggestions.
          </p>
        </Prose>
      </section>

      <div className={classes(styles.zeitgeist, "gap-y-8")}>
        <People people={people} className={classes(styles.people, "gap-x-4")} />
        <Divisions
          divisions={divisions}
          className={classes(styles.divisions, "full-cards")}
        />
        <Bills bills={bills} className={classes(styles.bills, "full-cards")} />
      </div>
    </ContentLayout>
  );
}

const ServerMessages = (props: { messages: ServerMessage[] }) => {
  const { messages } = props;

  if (!messages.length) return null;

  return (
    <section className="space-y-4 py-4">
      {messages.map((it, index) => (
        <ServerMessage key={index} message={it} />
      ))}
    </section>
  );
};

const ServerMessage = ({ message }: { message: ServerMessage }) => {
  const html = useHtml(message.description);
  return (
    <Callout className="readable justify-self-center">
      <strong>{message.title}</strong>
      <div>{html}</div>
      <Optional
        value={message.action_url}
        block={(url) => (
          <Button className="self-end border-2 border-primary/25" href={url}>
            More
          </Button>
        )}
      />
    </Callout>
  );
};

const People = (props: DivPropsNoChildren<{ people: Person[] }>) => {
  const { people, ...rest } = props;
  return (
    <ZeitgeistSection
      title="People"
      moreHref={navigationHref("people")}
      {...rest}
    >
      <Row overflow="scroll" className="gap-x-4 narrow-cards" padEdge>
        {people.map((it) => (
          <MemberItemCard
            key={it.target.parliamentdotuk}
            layout="hero"
            member={it.target}
          />
        ))}
      </Row>
    </ZeitgeistSection>
  );
};

const Divisions = (props: DivPropsNoChildren<{ divisions: Division[] }>) => {
  const { divisions, ...rest } = props;
  return (
    <ZeitgeistSection
      title="Divisions"
      moreHref={navigationHref("divisions")}
      {...addClass(rest, "px-edge")}
    >
      <div className="space-y-4">
        {divisions.map((it) => (
          <DivisionItemCard
            key={it.target.parliamentdotuk}
            division={it.target}
            className=""
          />
        ))}
      </div>
    </ZeitgeistSection>
  );
};

const Bills = (props: DivPropsNoChildren<{ bills: Bill[] }>) => {
  const { bills, ...rest } = props;
  return (
    <ZeitgeistSection
      title="Bills"
      moreHref={navigationHref("bills")}
      {...addClass(rest, "px-edge")}
    >
      <div className="space-y-4">
        {bills.map((it) => (
          <BillItemCard
            key={it.target.parliamentdotuk}
            bill={it.target}
            className=""
          />
        ))}
      </div>
    </ZeitgeistSection>
  );
};

const ZeitgeistSection = (
  props: DivProps<{
    title: string;
    moreHref: string;
    children: ReactNode;
  }>,
) => {
  const { title, moreHref, children, ...rest } = props;
  return (
    <div {...addClass(rest, "space-y-4")}>
      <h2 className="px-edge">
        <InlineLink href={moreHref}>{title}</InlineLink>
      </h2>
      {children}
    </div>
  );
};
