"use client";
import {TextButton, TintedButton} from "@/components/button";
import React, {ComponentPropsWithoutRef} from "react";
import {partyColors} from "@/components/themed/party";
import * as Sample from "@/app/dev/sample";
import {MemberItem} from "@/components/item-member";
import {HeaderCard} from "@/components/card";
import {MaskedSvg} from "@/components/image";
import Loading from "@/components/loading";
import {ButtonLink} from "@/components/link";
import {useSortable} from "@/components/sortable";
import {TabLayout} from "@/components/tabs";
import {addClass} from "@/util/transforms";
import Row from "@/components/row";

const LoremIpsum = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam et malesuada augue, vel tempor ipsum. Donec pellentesque sit amet nunc et sodales. Integer viverra velit at tellus rhoncus viverra. Aenean massa metus, tristique eget ipsum ut, consectetur imperdiet massa. Curabitur blandit massa sapien, eu scelerisque massa posuere eu. Duis tempus vestibulum enim ac gravida. Ut mauris sapien, commodo eu ultricies vel, porttitor imperdiet magna. Vivamus sed arcu in ex viverra maximus. In blandit lacus ut augue faucibus tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus.",
    "Nunc id iaculis tortor. Nunc posuere dolor ut egestas commodo. Cras aliquam convallis commodo. Praesent efficitur commodo gravida. Etiam ac vehicula neque. Nunc fermentum convallis eleifend. In congue gravida ex eu accumsan. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Quisque euismod tincidunt ex sed dictum. Nullam sagittis ultricies ex eu dapibus. Nunc quis mi mollis purus tempus semper. In in arcu elit. Fusce et tellus et ex sollicitudin ultricies eu eu tellus. Aenean pulvinar nunc eget augue congue, nec placerat velit tincidunt. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla laoreet a nisi a consequat.",
    "Curabitur id elementum tellus. Praesent ac lacus cursus, interdum elit at, venenatis diam. Donec feugiat ultricies faucibus. Nulla elit turpis, condimentum at massa a, consectetur laoreet nulla. Mauris porttitor tellus a justo venenatis, sit amet elementum lorem vehicula. Etiam commodo est eu diam tempor, vel auctor sapien suscipit. Ut congue ultricies rutrum. Vestibulum dapibus mi ut gravida pulvinar. Praesent nec dictum mi. Duis ut eros eros.",
    "In hac habitasse platea dictumst. Fusce vehicula purus vel nunc semper sollicitudin et nec justo. Sed placerat nulla non nibh convallis, ut aliquet mauris fringilla. In bibendum, diam sed suscipit finibus, purus turpis tincidunt dolor, eget eleifend felis tellus ut tellus. Nam vehicula sem tincidunt, efficitur ligula ut, scelerisque ante. Aenean quis eros ut tortor tincidunt blandit. Proin maximus in ipsum in dictum. Mauris lacus eros, porttitor sit amet libero non, venenatis condimentum mauris. Interdum et malesuada fames ac ante ipsum primis in faucibus. Integer ac hendrerit ex. Morbi tincidunt mauris sit amet dui luctus, ut consequat elit scelerisque.",
    "Donec congue turpis id elit lobortis aliquam. Vestibulum consequat iaculis laoreet. Pellentesque eget libero sed enim tempus blandit. Quisque id suscipit lectus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Quisque purus lectus, volutpat id neque at, vulputate blandit ligula. Donec vehicula dui at libero maximus auctor. Integer sem nisl, dictum vitae fringilla sit amet, ornare quis urna."]

export const ComponentsOverview = () => (
    <>
        <Section component="Loading">
            <Loading/>
        </Section>

        <TabComponents/>
        <ButtonComponents/>
        <SortableComponents/>
        <CardComponents/>

        <BreakpointsPreview/>
    </>
);

const ButtonComponents = () => (
    <>
        <Section component="TextButton">
            <Row className="px-edge gap-2 flex-wrap">
                <TextButton>TextButton</TextButton>
                <TextButton href="#">TextButton</TextButton>
                <TextButton href="#" icon="Wikipedia">
                    TextButton
                </TextButton>
                <TextButton onClick={() => console.log("Click!")} icon="Wikipedia">
                    TextButton
                </TextButton>
                |
                <TextButton href="#" icon="Wikipedia"/>
                <TextButton onClick={() => console.log("Click!")} icon="Wikipedia"/>
            </Row>
        </Section>

        <Section component="TintedButton">
            <Row className="px-edge gap-2 flex-wrap">
                <TintedButton>TintedButton</TintedButton>
                <TintedButton href="#">TintedButton</TintedButton>
                <TintedButton href="#" icon="Wikipedia">
                    TintedButton
                </TintedButton>
                <TintedButton onClick={() => console.log("Click!")} icon="Wikipedia">
                    TintedButton
                </TintedButton>
                |
                <TintedButton href="#" icon="Wikipedia"/>
                <TintedButton onClick={() => console.log("Click!")} icon="Wikipedia"/>
                <div style={partyColors(Sample.LabourParty)}>
                    <TintedButton href="#">Themed TintedButton</TintedButton>
                </div>
            </Row>
        </Section>

        <Section component="ButtonLink">
            <Row className="px-edge gap-2 flex-wrap">
                <ButtonLink href="https://beatonma.org">Home</ButtonLink>
                <ButtonLink href="mailto:test@beatonma.org">Email</ButtonLink>
                <ButtonLink href="tel:0800 800150">Phone</ButtonLink>
                <ButtonLink href="#">Debug</ButtonLink>
            </Row>
        </Section>
    </>
);

const SortableComponents = () => {
    const {sortedData, sortBySelectElement} = useSortable({
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
            <div className="px-edge">
                {sortBySelectElement}

                {sortedData?.map((it) => (
                    <div key={it.parliamentdotuk}>
                        {it.parliamentdotuk} {it.name} {it.party?.name}
                    </div>
                )) ?? <Loading/>}
            </div>
        </Section>
    );
};

const Section = (props: { component: string } & ComponentPropsWithoutRef<"section">) => {
    const {children, ...rest} = addClass(props, "border-b-2 py-4 sm:border-2 border-dotted sm:p-4 overflow-hidden");
    return (
        <section {...rest}>
            <h1>
                <pre>{`<${props.component} />`}</pre>
            </h1>
            {props.children}
        </section>
    );
};

const CardComponents = () => (
    <>
        {" "}
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
        <Section component="MemberItem">
            <MemberItem member={Sample.KeirStarmerItem}/>
        </Section>
    </>
);

const TabComponents = () => (
    <>
        <Section component="TabLayout">
            <TabLayout
                tabs={Sample.MemberList.map((it) => [
                    it.name,
                    () => <div className="px-edge">{it.party?.name}</div>,
                ])}
            />
        </Section>
    </>
);

const BreakpointsPreview = () => (
    <>
        <section>
            <h2>Breakpoints</h2>

            <div className="[&>*]:surface [&>*]:card [&>*]:card-content flex flex-col gap-2 overflow-x-auto">
                <div className="w-[var(--breakpoint-sm)]">breakpoint-sm</div>
                <div className="w-[var(--breakpoint-md)]">breakpoint-md</div>
                <div className="w-[var(--breakpoint-lg)]">breakpoint-lg</div>
                <div className="w-[var(--breakpoint-xl)]">breakpoint-xl</div>
                <div className="w-[var(--breakpoint-2xl)]">breakpoint-2xl</div>
            </div>
        </section>

        <section>
            <h2>Container breakpoints</h2>
            <div className="[&>*]:surface [&>*]:card [&>*]:card-content flex flex-col gap-2 overflow-x-auto">
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
                <div className="w-[var(--)]container-7xl)]">container-7xl</div>
            </div>
        </section>
    </>
);
