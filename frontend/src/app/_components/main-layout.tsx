import { ReactNode } from "react";
import { GlobalFooter } from "@/app/_components/global-footer";
import { GlobalHeader } from "@/app/_components/global-header";
import { classes } from "@/util/transforms";
import styles from "./main-layout.module.css";

export const DefaultLayout = ({
  children,
}: Readonly<{
  children: ReactNode;
}>) => {
  return (
    <CommonLayout className={styles.defaultLayout}>{children}</CommonLayout>
  );
};

export const FixedLayout = ({
  children,
}: Readonly<{
  children: ReactNode;
}>) => {
  return <CommonLayout className={styles.fixedLayout}>{children}</CommonLayout>;
};

const CommonLayout = ({
  className,
  children,
}: {
  className: string | undefined;
  children: ReactNode;
}) => {
  return (
    <body className={classes(className, "surface-background")}>
      <GlobalHeader />

      <div className={styles.globalContentWrapper}>{children}</div>

      <GlobalFooter />
    </body>
  );
};
