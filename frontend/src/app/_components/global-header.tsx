import Link from "next/link";
import { GlobalNavigation } from "@/app/_components/global-navigation";
import { Button, InlineButton } from "@/components/button";
import { Row } from "@/components/row";
import { ThemeController } from "@/features/themed/light-dark";
import { navigationHref } from "@/navigation";
import { classes } from "@/util/transforms";
import style from "./global-header.module.css";

export const GlobalHeader = () => (
  <header
    className={classes(
      style.globalHeader,
      "surface gap-x-4 gap-y-4 px-edge py-4 mb-4",
    )}
  >
    <div className="font-semibold text-current/95 text-3xl leading-none">
      <Link href="/">Commons</Link>
    </div>

    <GlobalNavigation />

    <Row className={classes(style.toolbar, "gap-x-2")}>
      <Button href={navigationHref("about")}>About</Button>
      <ThemeController />
    </Row>
  </header>
);
