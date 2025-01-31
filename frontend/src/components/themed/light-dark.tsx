"use client";

import { AppIcon } from "@/components/icon";
import { ComponentProps, useEffect, useMemo, useState } from "react";
import { TextButton } from "@/components/button";

const StorageKey = "theme";
type Theme = "light" | "dark" | "system";
const ThemeController = (
  props: Omit<ComponentProps<"button">, "onClick" | "title">,
) => {
  const [mode, setMode] = useState<Theme>(
    (localStorage.getItem(StorageKey) ?? "system") as Theme,
  );
  const icon: AppIcon = useMemo(() => {
    switch (mode) {
      case "light":
        return "ThemeLightMode";
      case "dark":
        return "ThemeDarkMode";
      case "system":
      default:
        return "ThemeSystemDefault";
    }
  }, [mode]);

  useEffect(() => {
    document.body.dataset.theme = mode;
    localStorage.setItem(StorageKey, mode);
  }, [mode]);

  return (
    <TextButton
      icon={icon}
      onClick={() => setMode(nextTheme(mode) ?? "system")}
      title={`Cycle theme (${mode})`}
      {...props}
    />
  );
};

const nextTheme = (theme: Theme) => {
  const themes: Theme[] = ["light", "dark", "system"];
  return themes[(themes.findIndex((it) => it === theme) + 1) % themes.length];
};

export default ThemeController;
