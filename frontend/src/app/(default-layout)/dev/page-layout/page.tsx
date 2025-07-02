import { Metadata } from "next";
import { PageLayoutPreview } from "@/app/(default-layout)/dev/page-layout/layout-preview";

export const metadata: Metadata = {
  title: "Page layout",
  description: "UI components",
};

export default function PageLayoutPreviewPage() {
  return <PageLayoutPreview />;
}
