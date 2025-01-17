"use client";
import { TextButton, TintedButton } from "@/components/button";
import React from "react";
import { ChildrenProps } from "@/types/common";
import { partyStyle } from "@/components/themed/party";
import * as Sample from "@/app/dev/sample";
import { MemberItem } from "@/components/item-member";
import { HeaderCard } from "@/components/card";
import { MaskedSvg } from "@/components/image";
import Loading from "@/components/loading";
import { ButtonLink } from "@/components/link";
import { useSortable } from "@/components/sortable";

export const ComponentsOverview = () => (
  <>
    <Section component="Loading">
      <Loading />
    </Section>

    <ButtonComponents />

    <Section component="HeaderCard">
      <HeaderCard
        party={Sample.LabourParty}
        image={
          <MaskedSvg
            src={Sample.LabourParty.logo}
            className="size-64 bg-white"
          />
        }
      >
        <h1>Header card</h1>
        <p>Text content</p>
      </HeaderCard>
    </Section>

    <Section component="MemberItem">
      <MemberItem member={Sample.KeirStarmerItem} />
    </Section>
  </>
);

const ButtonComponents = () => (
  <>
    <SortableComponents />

    <Section component="TextButton">
      <Row>
        <TextButton>TextButton</TextButton>
        <TextButton href="#">TextButton</TextButton>
        <TextButton href="#" icon="Wikipedia">
          TextButton
        </TextButton>
        <TextButton onClick={() => console.log("Click!")} icon="Wikipedia">
          TextButton
        </TextButton>
      </Row>
    </Section>

    <Section component="TintedButton">
      <Row>
        <TintedButton>TintedButton</TintedButton>
        <TintedButton href="#">TintedButton</TintedButton>
        <TintedButton href="#" icon="Wikipedia">
          TintedButton
        </TintedButton>
        <TintedButton onClick={() => console.log("Click!")} icon="Wikipedia">
          TintedButton
        </TintedButton>

        <div style={partyStyle(Sample.LabourParty)}>
          <TintedButton href="#">Themed TintedButton</TintedButton>
        </div>
      </Row>
    </Section>

    <Section component="ButtonLink">
      <Row>
        <ButtonLink href="https://beatonma.org">Home</ButtonLink>
        <ButtonLink href="mailto:test@beatonma.org">Email</ButtonLink>
        <ButtonLink href="tel:0800 800150">Phone</ButtonLink>
        <ButtonLink href="#">Debug</ButtonLink>
      </Row>
    </Section>
  </>
);

const SortableComponents = () => {
  const { sortedData, sortBySelectElement } = useSortable({
    data: Sample.MemberList,
    defaultSort: "parliamentdotuk",
    sortOptions: {
      parliamentdotuk: {
        name: "ID",
        sort: (a, b) => a.parliamentdotuk - b.parliamentdotuk,
      },
      name: {
        name: "Name",
        sort: (a, b) => a.name.localeCompare(b.name),
      },
      party: {
        name: "Party",
        sort: (a, b) =>
          (a.party?.name ?? "")?.localeCompare(b.party?.name ?? ""),
      },
    },
  });

  return (
    <Section component="Sortable">
      <div>
        {sortBySelectElement}

        {sortedData?.map((it) => (
          <div key={it.parliamentdotuk}>
            {it.parliamentdotuk} {it.name} {it.party?.name}
          </div>
        )) ?? <Loading />}
      </div>
    </Section>
  );
};

const Section = (props: { component: string } & ChildrenProps) => {
  return (
    <section className="border-2 border-dotted p-4">
      <h1>
        <pre>{`<${props.component} />`}</pre>
      </h1>
      {props.children}
    </section>
  );
};

const Row = (props: ChildrenProps) => (
  <div className="flex flex-wrap items-start gap-2">{props.children}</div>
);
