"use client";

import { useMemo } from "react";
import { BillDetail } from "@/api/schema";
import { TabLayout, useTabContent } from "@/components/tabs";
import { DivPropsNoChildren } from "@/types/react";
import { Publications, Sessions, Stages } from "./_components";

export const BillTabs = (props: DivPropsNoChildren<{ bill: BillDetail }>) => {
  const { bill, ...rest } = props;
  const tabs = useTabContent(
    useMemo(
      () => [
        {
          title: "Publications",
          condition: bill.publications.length > 0,
          content: () => (
            <Publications
              publications={bill.publications}
              className="space-y-4"
            />
          ),
        },
        {
          title: "Stages & Sittings",
          condition: !!bill.current_stage || bill.stages.length > 0,
          content: () => (
            <Stages
              current={bill.current_stage}
              stages={bill.stages}
              className="space-y-4"
            />
          ),
        },
        {
          title: "Sessions",
          condition: !!bill.session_introduced || bill.sessions.length > 0,
          content: () => (
            <Sessions
              introduced={bill.session_introduced}
              sessions={bill.sessions}
            />
          ),
        },
      ],
      [bill],
    ),
  );

  return (
    <TabLayout tabs={tabs} contentProps={{ className: "py-4" }} {...rest} />
  );
};
