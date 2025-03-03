"use client";
import { TextButton, TintedButton } from "@/components/button";
import React, { ComponentPropsWithoutRef, useState } from "react";
import { partyColors } from "@/components/themed/party";
import * as Sample from "@/app/dev/sample";
import {
  MemberItemCard,
  PartyItemCard,
  ConstituencyItemCard,
} from "@/components/models/list-item";
import { HeaderCard } from "@/components/card";
import { MaskedSvg } from "@/components/image";
import Loading from "@/components/loading";
import { ButtonLink } from "@/components/link";
import { useSortable } from "@/components/sortable";
import { TabLayout } from "@/components/tabs";
import { addClass, classes } from "@/util/transforms";
import Row from "@/components/row";
import { getOnColor } from "@/components/themed/color";

export const LoremIpsum: string[] = [
  "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam et malesuada augue, vel tempor ipsum. Donec pellentesque sit amet nunc et sodales. Integer viverra velit at tellus rhoncus viverra. Aenean massa metus, tristique eget ipsum ut, consectetur imperdiet massa. Curabitur blandit massa sapien, eu scelerisque massa posuere eu. Duis tempus vestibulum enim ac gravida. Ut mauris sapien, commodo eu ultricies vel, porttitor imperdiet magna. Vivamus sed arcu in ex viverra maximus. In blandit lacus ut augue faucibus tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus.",
  "Nunc id iaculis tortor. Nunc posuere dolor ut egestas commodo. Cras aliquam convallis commodo. Praesent efficitur commodo gravida. Etiam ac vehicula neque. Nunc fermentum convallis eleifend. In congue gravida ex eu accumsan. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Quisque euismod tincidunt ex sed dictum. Nullam sagittis ultricies ex eu dapibus. Nunc quis mi mollis purus tempus semper. In in arcu elit. Fusce et tellus et ex sollicitudin ultricies eu eu tellus. Aenean pulvinar nunc eget augue congue, nec placerat velit tincidunt. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla laoreet a nisi a consequat.",
  "Curabitur id elementum tellus. Praesent ac lacus cursus, interdum elit at, venenatis diam. Donec feugiat ultricies faucibus. Nulla elit turpis, condimentum at massa a, consectetur laoreet nulla. Mauris porttitor tellus a justo venenatis, sit amet elementum lorem vehicula. Etiam commodo est eu diam tempor, vel auctor sapien suscipit. Ut congue ultricies rutrum. Vestibulum dapibus mi ut gravida pulvinar. Praesent nec dictum mi. Duis ut eros eros.",
  "In hac habitasse platea dictumst. Fusce vehicula purus vel nunc semper sollicitudin et nec justo. Sed placerat nulla non nibh convallis, ut aliquet mauris fringilla. In bibendum, diam sed suscipit finibus, purus turpis tincidunt dolor, eget eleifend felis tellus ut tellus. Nam vehicula sem tincidunt, efficitur ligula ut, scelerisque ante. Aenean quis eros ut tortor tincidunt blandit. Proin maximus in ipsum in dictum. Mauris lacus eros, porttitor sit amet libero non, venenatis condimentum mauris. Interdum et malesuada fames ac ante ipsum primis in faucibus. Integer ac hendrerit ex. Morbi tincidunt mauris sit amet dui luctus, ut consequat elit scelerisque.",
  "Donec congue turpis id elit lobortis aliquam. Vestibulum consequat iaculis laoreet. Pellentesque eget libero sed enim tempus blandit. Quisque id suscipit lectus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Quisque purus lectus, volutpat id neque at, vulputate blandit ligula. Donec vehicula dui at libero maximus auctor. Integer sem nisl, dictum vitae fringilla sit amet, ornare quis urna.",
];

export const ComponentsOverview = () => (
  <>
    <Section name="<Loading />">
      <Loading />
    </Section>

    <TabComponents />
    <ButtonComponents />
    <SortableComponents />
    <CardComponents />

    <BreakpointsPreview />
    <ThemeColors />
  </>
);

const ButtonComponents = () => (
  <>
    <Section name="<TextButton />">
      <Row className="flex-wrap gap-2">
        <TextButton>TextButton</TextButton>
        <TextButton href="#">TextButton</TextButton>
        <TextButton href="#" icon="Wikipedia">
          TextButton
        </TextButton>
        <TextButton onClick={() => console.log("Click!")} icon="Wikipedia">
          TextButton
        </TextButton>
        |
        <TextButton href="#" icon="Wikipedia" />
        <TextButton onClick={() => console.log("Click!")} icon="Wikipedia" />
      </Row>
    </Section>

    <Section name="<TintedButton />">
      <Row className="flex-wrap gap-2">
        <TintedButton>TintedButton</TintedButton>
        <TintedButton href="#">TintedButton</TintedButton>
        <TintedButton href="#" icon="Wikipedia">
          TintedButton
        </TintedButton>
        <TintedButton onClick={() => console.log("Click!")} icon="Wikipedia">
          TintedButton
        </TintedButton>
        |
        <TintedButton href="#" icon="Wikipedia" />
        <TintedButton onClick={() => console.log("Click!")} icon="Wikipedia" />
        <div style={partyColors(Sample.LabourParty)}>
          <TintedButton href="#">Themed TintedButton</TintedButton>
        </div>
      </Row>
    </Section>

    <Section name="<ButtonLink />">
      <Row className="flex-wrap gap-2">
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
    <Section name="<Sortable />" className="block">
      {sortBySelectElement}

      {sortedData?.map((it) => (
        <div key={it.parliamentdotuk}>
          {it.parliamentdotuk} {it.name} {it.party?.name}
        </div>
      )) ?? <Loading />}
    </Section>
  );
};

const Section = (
  props: { name: string } & ComponentPropsWithoutRef<"section">,
) => {
  const { children, ...rest } = addClass(
    props,
    "border-2 pb-4 border-dotted overflow-hidden px-edge",
  );
  return (
    <section id={props.name.replaceAll(/[^\w]/g, "")} {...rest}>
      <h1>
        <pre>{props.name}</pre>
      </h1>
      {props.children}
    </section>
  );
};

const CardComponents = () => (
  <>
    <Section name="<HeaderCard />">
      <HeaderCard
        party={Sample.LabourParty}
        image={
          <MaskedSvg
            src={Sample.LabourParty.logo}
            className="bg-primary size-48"
          />
        }
      >
        <h1>Header card</h1>
        <p>{LoremIpsum.slice(0, 1)}</p>
      </HeaderCard>

      <HeaderCard party={Sample.InvernessConstituency.mp?.party}>
        <h1>No image</h1>
        <p>{LoremIpsum.slice(0, 1)}</p>
      </HeaderCard>

      <HeaderCard party={undefined}>
        <h1>No party</h1>
        <p>{LoremIpsum.slice(0, 1)}</p>
      </HeaderCard>
    </Section>

    <Section name="<MemberItemCard />">
      <div className="search-results-grid">
        <MemberItemCard member={Sample.KeirStarmerItem} label="Featured" />
        {Sample.MemberList.slice(0, 10).map((it) => (
          <MemberItemCard key={it.parliamentdotuk} member={it} />
        ))}
      </div>
    </Section>

    <Section name="<PartyItemCard />">
      <div className="search-results-grid">
        <PartyItemCard party={Sample.LabourParty} />
      </div>
    </Section>

    <Section name="<ConstituencyItemCard />">
      <div className="search-results-grid">
        <ConstituencyItemCard constituency={Sample.InvernessConstituency} />
      </div>
    </Section>
  </>
);

const TabComponents = () => (
  <>
    <Section name="<TabLayout />">
      <TabLayout
        tabs={Sample.MemberList.map((it) => [
          it.name,
          () => <div>{it.party?.name}</div>,
        ])}
      />
    </Section>
  </>
);

const BreakpointsPreview = () => (
  <>
    <Section name="Breakpoints">
      <div className="[&>*]:surface [&>*]:card [&>*]:card-content column gap-2 overflow-x-auto">
        <div className="w-[var(--breakpoint-sm)]">breakpoint-sm</div>
        <div className="w-[var(--breakpoint-md)]">breakpoint-md</div>
        <div className="w-[var(--breakpoint-lg)]">breakpoint-lg</div>
        <div className="w-[var(--breakpoint-xl)]">breakpoint-xl</div>
        <div className="w-[var(--breakpoint-2xl)]">breakpoint-2xl</div>
      </div>
    </Section>

    <Section name="Container breakpoints">
      <div className="[&>*]:surface [&>*]:card [&>*]:card-content column gap-2 overflow-x-auto">
        <div className="w-[var(--container-3xs)]">container-3xs</div>
        <div className="w-[var(--container-2xs)]">container-2xs</div>
        <div className="w-[var(--container-xs)]">container-xs</div>
        <div className="w-[var(--container-sm)]">container-sm</div>
        <div className="w-[var(--container-md)]">container-md</div>
        <div className="w-[var(--container-lg)]">container-lg</div>
        <div className="w-[var(--container-xl)]">container-xl</div>
        <div className="w-[var(--container-2xl)]">container-2xl</div>
        <div className="w-[var(--container-3xl)]">container-3xl</div>
        <div className="w-[var(--container-4xl)]">container-4xl</div>
        <div className="w-[var(--container-5xl)]">container-5xl</div>
        <div className="w-[var(--container-6xl)]">container-6xl</div>
        <div className="w-[var(--container-7xl)]">container-7xl</div>
      </div>
    </Section>
  </>
);

const ThemeColors = () => {
  const gridClass = classes(
    "grid grid-cols-[repeat(auto-fit,200px)] gap-1",
    "font-bold",
    "[&>*]:card-content [&>*]:aspect-square [&>*]:border-2 [&>*]:border-dashed [&>*]:border-current/20",
  );

  const [color, setColor] = useState<string>("#000000");

  return (
    <Section name="Theme colors" className="gap-1">
      <div className={gridClass}>
        <div className="bg-background text-on_background">background</div>
        <div className="bg-surface text-on_surface">surface</div>
        <div className="bg-surface_alt text-on_surface">surface_alt</div>
        <div className="bg-primary text-on_primary">primary</div>
        <div className="bg-accent text-on_accent">accent</div>
      </div>

      <div className={gridClass}>
        <div className="bg-invert_background text-invert_on_background">
          invert background
        </div>
        <div className="bg-invert_surface text-invert_on_surface">
          invert surface
        </div>
        <div className="bg-invert_surface_alt text-invert_on_surface">
          invert surface_alt
        </div>
        <div className="bg-invert_primary text-invert_on_primary">
          invert primary
        </div>
        <div className="bg-invert_accent text-invert_on_accent">
          invert accent
        </div>
      </div>

      <div className={gridClass}>
        <div className="bg-house-commons text-house-on_commons">commons</div>
        <div className="bg-house-commons-dark text-house-on_commons">
          commons-dark
        </div>
        <div className="bg-house-commons-darker text-house-on_commons">
          commons-darker
        </div>
      </div>

      <div className={gridClass}>
        <div className="bg-house-lords text-house-on_lords">lords</div>
        <div className="bg-house-lords-dark text-house-on_lords">
          lords-dark
        </div>
        <div className="bg-house-lords-darker text-house-on_lords">
          lords-darker
        </div>
      </div>

      <div className={gridClass}>
        <div style={{ backgroundColor: color, color: getOnColor(color) }}>
          background
        </div>
        <div
          style={{
            backgroundColor: getOnColor(color),
            color: getOnColor(getOnColor(color)),
          }}
        >
          foreground
        </div>
        <input
          type="color"
          value={color}
          onChange={(ev) => setColor(ev.target.value)}
        />
      </div>
    </Section>
  );
};
