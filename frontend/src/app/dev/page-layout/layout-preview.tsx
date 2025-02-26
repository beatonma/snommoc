"use client";
import PageLayout, { PageLayouts } from "@/components/page";
import { DivProps } from "@/types/react";
import { addClass } from "@/util/transforms";
import { useState } from "react";

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
      secondary={<Card className="bg-house-lords">Secondary</Card>}
      sidebarLeft={<Card className="bg-house-lords-dark">Left</Card>}
      sidebarRight={<Card className="bg-house-lords-darker">Right</Card>}
    >
      <Card className="bg-house-commons">
        <h1>Main</h1>
        <h2>{layout}</h2>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque
          ut leo sed velit condimentum convallis quis nec odio. In erat nunc,
          elementum et venenatis volutpat, posuere eget elit. Pellentesque
          habitant morbi tristique senectus et netus et malesuada fames ac
          turpis egestas. Vestibulum sed aliquet ligula, non feugiat nisl. Sed
          lobortis risus sit amet dolor aliquet scelerisque. Duis eu ligula in
          elit ultricies tempor. Nulla facilisi.
        </p>
        <p>
          Maecenas ultricies libero ac diam porta molestie. Quisque pulvinar
          sollicitudin dapibus. In hac habitasse platea dictumst. Aliquam nisi
          arcu, interdum a fringilla vel, iaculis et felis. Ut tempor elit eu
          nulla interdum, id bibendum dui tempus. Vestibulum sit amet commodo
          nunc, sit amet sagittis sem. Praesent ac leo blandit, maximus sem in,
          volutpat odio. Etiam magna turpis, blandit pretium semper et, lobortis
          at lectus. Vivamus elementum, mauris et scelerisque condimentum, nulla
          massa porttitor erat, at aliquam diam tellus in erat. Donec convallis
          dolor vitae est congue, eget pulvinar nisl consectetur. Praesent
          sagittis, purus a ultrices accumsan, orci libero facilisis odio, eget
          luctus massa ligula vehicula libero. Aliquam placerat vehicula ipsum a
          posuere. Vestibulum non hendrerit est, nec condimentum ligula. Sed
          justo erat, aliquam ac volutpat ac, efficitur id ligula.
        </p>

        <p>
          Proin faucibus ornare turpis, ut imperdiet diam congue ac. Praesent
          sodales risus luctus, varius nisl eu, feugiat lectus. Nam porta
          vulputate semper. Aliquam auctor posuere nunc, at faucibus velit
          luctus at. Sed eros ipsum, commodo vitae nisi et, pulvinar
          sollicitudin sapien. Cras ullamcorper at ligula et efficitur. In sit
          amet euismod quam, sed fermentum risus.
        </p>
        <p>
          Morbi vel turpis eros. Nulla facilisi. Nunc nunc dolor, suscipit id
          justo sed, lacinia volutpat leo. Aenean quis facilisis turpis, a
          auctor diam. Cras et urna luctus, egestas risus nec, posuere augue.
          Nullam eleifend eu leo id dapibus. Quisque eget tortor pharetra,
          aliquam mauris id, facilisis sapien. Sed vel ipsum at massa cursus
          lacinia ut nec metus. Maecenas vestibulum leo id ultrices rutrum. Sed
          turpis nulla, pretium in nisl at, efficitur cursus dui. Sed pharetra
          risus eu pulvinar rhoncus. Nam vel pretium dui. Etiam eu lectus
          scelerisque enim mollis aliquet a ut sapien. Donec eleifend tristique
          quam sed molestie. Nulla ac ultrices arcu.
        </p>
        <p>
          Pellentesque malesuada interdum leo ut sollicitudin. Nullam varius
          placerat lectus non semper. Nunc aliquet nisi id ligula fermentum
          consequat. Suspendisse blandit imperdiet magna, id suscipit arcu
          mattis quis. Duis at felis ac ante aliquet pretium at eget neque.
          Donec ornare orci quam, at fringilla turpis sagittis consequat. Sed
          dignissim orci et ligula mollis pharetra. Nullam vestibulum nunc
          auctor risus mollis convallis. Praesent sodales convallis massa in
          ultricies. Quisque eleifend eros id dolor posuere mattis.
        </p>
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
