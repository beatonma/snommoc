import type { Metadata, ResolvingMetadata } from "next";
import { getOr404 } from "@/api";
import {
  BillType,
  DateWithdrawn,
  IsAct,
  IsDefeated,
  Sponsors,
} from "@/app/(default-layout)/bills/[parliamentdotuk]/_components";
import { BillTabs } from "@/app/(default-layout)/bills/[parliamentdotuk]/bill";
import { Date } from "@/components/datetime";
import { Html } from "@/components/hooks/html";
import { ContentLayout } from "@/components/page-layout";
import { Prose } from "@/components/prose";
import { Row } from "@/components/row";

type PageProps = {
  params: Promise<{ parliamentdotuk: number }>;
};

const getBill = async (parliamentdotuk: number) =>
  getOr404("/api/bills/{parliamentdotuk}/", {
    path: { parliamentdotuk },
  });

export async function generateMetadata(
  { params }: PageProps,
  parent: ResolvingMetadata,
): Promise<Metadata> {
  const parliamentdotuk = (await params).parliamentdotuk;
  const bill = await getBill(parliamentdotuk);
  const parentTitle = (await parent).title?.absolute;
  return {
    title: bill ? `${bill.title} - ${parentTitle}` : parentTitle,
    description: [`Bill details`, bill.description].filter(Boolean).join(": "),
  };
}

export default async function BillDetailPage({ params }: PageProps) {
  const parliamentdotuk = (await params).parliamentdotuk;
  const bill = await getBill(parliamentdotuk);

  return (
    <ContentLayout layout="CenteredReadable" mainClassName="space-y-8">
      <Row overflow="wrap" className="gap-x-4">
        <span className="text-sm">
          Updated <Date date={bill.last_update} />
        </span>
        <IsAct isAct={bill.is_act} />
        <IsDefeated isDefeated={bill.is_defeated} />
        <DateWithdrawn dateWithdrawn={bill.date_withdrawn} />
      </Row>
      <h1>{bill.title}</h1>

      {bill.description && (
        <Prose>
          <Html html={bill.description} />
        </Prose>
      )}
      <Sponsors sponsors={bill.sponsors} className="space-y-2" />
      <BillType type={bill.type} className="card card-content surface" />

      <BillTabs bill={bill} className="card card-content surface" />
    </ContentLayout>
  );
}
