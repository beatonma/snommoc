"use client";

import { useState } from "react";
import { LoremIpsum } from "@/app/(default-layout)/dev/components";
import {
  ContentLayout,
  _private,
} from "@/components/page-layout/content-layout";
import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";

type LayoutName = keyof typeof _private.PageLayouts;
export const PageLayoutPreview = () => {
  const [layout, setLayout] = useState<LayoutName>("CenteredFeed");

  return (
    <div>
      <select
        className="mb-8"
        onChange={(e) => setLayout(e.target.value as LayoutName)}
      >
        {Object.entries(_private.PageLayouts).map(([key, value]) => (
          <option value={key} key={key}>
            {key}
          </option>
        ))}
      </select>

      <Layout layout={layout} />
    </div>
  );
};

const Layout = ({ layout }: { layout: LayoutName }) => {
  return (
    <ContentLayout
      layout={layout}
      className="gap-2"
      secondary={<Card className="surface-lords">Secondary</Card>}
      sidebarLeft={
        <Card className="bg-house-lords-dark text-house-on-lords">Left</Card>
      }
      sidebarRight={
        <Card className="bg-house-lords-darker text-house-on-lords">Right</Card>
      }
    >
      <Card className="surface-commons">
        <h1>Main</h1>
        <h2>{layout}</h2>
        {LoremIpsum.map((it, index) => (
          <p key={index}>{it}</p>
        ))}
      </Card>
    </ContentLayout>
  );
};

const Card = (props: DivProps) => (
  <div
    {...addClass(
      props,
      "card card-content surface size-full min-h-100 column gap-2",
    )}
  />
);
