import { ReactNode } from "react";
import { DefaultLayout } from "@/app/_components/main-layout";

export default async function Layout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  return <DefaultLayout>{children}</DefaultLayout>;
}
