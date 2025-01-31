"use client";
import { ReactNode, useId, useMemo, useState } from "react";
import { addClass } from "@/util/transforms";
import { DivProps, DivPropsNoChildren } from "@/types/react";

interface TabLayoutProps<T extends string> {
  tabs: [T, () => ReactNode][];
  defaultTab?: T;
}
export const TabLayout = <T extends string>(props: TabLayoutProps<T>) => {
  const { tabs, defaultTab, ...rest } = props;
  const tabNames: T[] = useMemo(() => tabs.map((it) => it[0]), [tabs]);

  const [currentTab, setCurrentTab] = useState<T>(defaultTab ?? tabNames[0]!);
  const [currentTabId, setCurrentTabId] = useState<string>();
  const tabPanelId = useId();

  const content = useMemo(
    () => tabs.find((it) => it[0] === currentTab)?.[1],
    [tabs, currentTab],
  );

  return (
    <div {...rest}>
      <TabBar
        currentTab={currentTab}
        tabs={tabNames}
        onClickTab={(tab: T, tabId: string) => {
          setCurrentTabId(tabId);
          setCurrentTab(tab);
        }}
        tabAttributes={{
          "aria-controls": tabPanelId,
        }}
      />

      <div role="tabpanel" aria-labelledby={currentTabId}>
        {content?.()}
      </div>
    </div>
  );
};

interface TabBarProps<T extends string> {
  tabs: T[];
  currentTab: T;
  onClickTab: (tab: T, tabId: string) => void;
  tabAttributes: Record<string, string>;
}
const TabBar = <T extends string>(
  props: TabBarProps<T> & DivPropsNoChildren,
) => {
  const { tabs, currentTab, onClickTab, tabAttributes, ...rest } = addClass(
    props,
    "flex flex-row gap-2 overflow-x-auto",
  );

  return (
    <nav role="tablist" {...rest}>
      {tabs.map((tab) => (
        <Tab
          key={tab}
          aria-selected={tab === currentTab}
          onClick={(tabId: string) => onClickTab(tab, tabId)}
          {...tabAttributes}
        >
          {tab}
        </Tab>
      ))}
    </nav>
  );
};

interface TabProps {
  onClick: (tabId: string) => void;
}
const Tab = (
  props: TabProps & Omit<DivProps, keyof TabProps | "id" | "role">,
) => {
  const { onClick, ...rest } = addClass(
    props,
    "cursor-pointer px-2 pb-1 pt-2 transition-colors whitespace-nowrap",
    "border-b-2",
    "aria-selected:border-primary aria-selected:font-bold",
  );
  const tabId = useId();

  return <div id={tabId} role="tab" onClick={() => onClick(tabId)} {...rest} />;
};
