import { ReactNode } from "react";
import { FixedLayout } from "@/app/_components/main-layout";

export default async function Layout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  return <FixedLayout>{children}</FixedLayout>;
}
