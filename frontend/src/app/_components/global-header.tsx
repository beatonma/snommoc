import Link from "next/link";
import { GlobalNavigation } from "@/app/_components/global-navigation";
import { ThemeController } from "@/features/themed/light-dark";

export const GlobalHeader = () => (
  <header className="surface gap-x-4 px-edge py-2 mb-2">
    <h1>
      <Link href="/">Commons</Link>
    </h1>

    <GlobalNavigation />

    <div className="toolbar">
      <ThemeController className="p-2" />
    </div>
  </header>
);
