"use client";

import { DependencyList, ReactNode, useId, useMemo, useState } from "react";
import {
  DivProps,
  DivPropsNoChildren,
  Props,
  PropsExcept,
} from "@/types/react";
import { addClass } from "@/util/transforms";

export type TabContent<T extends string> = [T, () => ReactNode];
interface TabLayoutProps<T extends string> {
  tabs: TabContent<T>[];
  defaultTab?: T;
  tabProps?: PublicTabProps;
  contentProps?: PropsExcept<"div", "children" | "role" | "aria-labelledby">;
}
export const TabLayout = <T extends string>(
  props: DivPropsNoChildren<TabLayoutProps<T>>,
) => {
  const { tabs, defaultTab, tabProps, contentProps, ...rest } = props;
  const tabNames: T[] = useMemo(() => tabs.map((it) => it[0]), [tabs]);

  const [currentTab, setCurrentTab] = useState<T>(defaultTab ?? tabNames[0]!);
  const [currentTabId, setCurrentTabId] = useState<string>();
  const tabPanelId = useId();

  const content = useMemo(
    () => tabs.find((it) => it[0] === currentTab)?.[1],
    [tabs, currentTab],
  );

  if (!tabs.length) return null;

  return (
    <div {...rest}>
      <TabBar
        currentTab={currentTab}
        tabs={tabNames}
        onClickTab={(tab: T, tabId: string) => {
          setCurrentTabId(tabId);
          setCurrentTab(tab);
        }}
        tabProps={{
          ...tabProps,
          "aria-controls": tabPanelId,
        }}
      />

      <div role="tabpanel" aria-labelledby={currentTabId} {...contentProps}>
        {content?.()}
      </div>
    </div>
  );
};

interface TabBarProps<T extends string> {
  tabs: T[];
  currentTab: T;
  onClickTab: (tab: T, tabId: string) => void;
  tabProps: PublicTabProps;
}
const TabBar = <T extends string>(
  props: DivPropsNoChildren<TabBarProps<T>>,
) => {
  const { tabs, currentTab, onClickTab, tabProps, ...rest } = addClass(
    props,
    "row-scroll gap-2",
  );

  return (
    <nav role="tablist" {...rest}>
      {tabs.map((tab) => (
        <Tab
          key={tab}
          aria-selected={tab === currentTab}
          onClick={(tabId: string) => onClickTab(tab, tabId)}
          {...tabProps}
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
type PublicTabProps = Props<
  typeof Tab,
  object,
  "aria-selected" | "children" | "onClick"
>;
const Tab = (props: DivProps<TabProps, "id" | "role">) => {
  const { onClick, ...rest } = addClass(
    props,
    "shrink-0 cursor-pointer px-2 pb-1 pt-2 transition-all flex items-center",
    "border-b-2 border-current/50 text-reduced hover:bg-hover text-sm select-none",
    "aria-selected:text-current aria-selected:border-b-4 aria-selected:border-primary aria-selected:font-bold aria-selected:text-lg aria-selected:bg-primary/5",
  );
  const tabId = useId();

  return <div id={tabId} role="tab" onClick={() => onClick(tabId)} {...rest} />;
};

interface MaybeTabContent<T extends string> {
  title: T;
  condition?: boolean;
  content: () => ReactNode;
}
export const useTabContent = <T extends string>(
  content: MaybeTabContent<T>[],
  deps?: DependencyList,
): TabContent<T>[] => {
  return useMemo(
    () =>
      content
        .filter((it) => it.condition !== false)
        .map((it) => [it.title, it.content]),
    [deps],
  );
};
