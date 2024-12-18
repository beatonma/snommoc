"use client";
import { TextButton, TintedButton } from "@/components/button";
import React from "react";
import { ChildrenProps } from "@/types/common";
import { partyThemeVariableStyle } from "@/components/themed/party";
import * as Sample from "@/app/dev/sample";
import { MemberItem } from "@/components/item-member";
import { HeaderCard } from "@/components/card";
import { MaskedSvg } from "@/components/image";
import Loading from "@/components/loading";

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

        <div style={partyThemeVariableStyle(Sample.LabourParty)}>
          <TintedButton href="#">Themed TintedButton</TintedButton>
        </div>
      </Row>
    </Section>
  </>
);

const Section = (props: { component: string } & ChildrenProps) => {
  return (
    <section className="border-2 border-dotted p-4">
      <h1 className="mb-4">
        <pre>{`<${props.component} />`}</pre>
      </h1>
      {props.children}
    </section>
  );
};

const Row = (props: ChildrenProps) => (
  <div className="flex flex-wrap gap-2">{props.children}</div>
);
