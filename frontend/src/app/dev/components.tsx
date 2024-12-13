"use client";
import { TextButton, TintedButton } from "@/components/button";
import React, { CSSProperties } from "react";
import { ChildrenProps } from "@/types/common";

const Theme: CSSProperties = {
  // @ts-expect-error: Custom css variables not in CSSProperties spec.
  "--accent": "212 19 144",
  "--on_accent": "255 255 255",
};

export const ComponentsOverview = () => (
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

        <div style={Theme}>
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
