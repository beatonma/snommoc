"use client";
import PageLayout, { PageLayouts } from "@/components/page";
import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";
import { useState } from "react";
import { LoremIpsum } from "@/app/dev/components";

type LayoutName = keyof typeof PageLayouts;
export default function PageLayoutPreview() {
  const [layout, setLayout] = useState<LayoutName>("CenteredFeed");

  return (
    <div>
      <select
        className="mb-8"
        onChange={(e) => setLayout(e.target.value as LayoutName)}
      >
        {Object.entries(PageLayouts).map(([key, value]) => (
          <option value={key} key={key}>
            {key}
          </option>
        ))}
      </select>

      <Layout layout={layout} />
    </div>
  );
}

const Layout = ({ layout }: { layout: LayoutName }) => {
  return (
    <PageLayout
      layout={layout}
      className="gap-2"
      secondary={<Card className="surface-lords">Secondary</Card>}
      sidebarLeft={
        <Card className="bg-house-lords-dark text-house-on_lords">Left</Card>
      }
      sidebarRight={
        <Card className="bg-house-lords-darker text-house-on_lords">Right</Card>
      }
    >
      <Card className="surface-commons">
        <h1>Main</h1>
        <h2>{layout}</h2>
        {LoremIpsum.map((it, index) => (
          <p key={index}>{it}</p>
        ))}
      </Card>
    </PageLayout>
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
