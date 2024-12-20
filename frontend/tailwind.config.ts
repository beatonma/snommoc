import type { Config } from "tailwindcss";
import colors from "tailwindcss/colors";

export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      screens: {
        md: "863px",
      },
      colors: {
        surface: {
          DEFAULT: "rgb(var(--surface))",
          ...colors.neutral,
        },
        on_surface: {
          DEFAULT: "rgb(var(--on_surface))",
        },
        primary: {
          DEFAULT: "rgb(var(--primary))",
          ...colors.slate,
        },
        on_primary: "rgb(var(--on_primary))",
        accent: {
          DEFAULT: "rgb(var(--accent))",
          ...colors.amber,
        },
        on_accent: "rgb(var(--on_accent))",
        house: {
          commons: {
            DEFAULT: "rgb(var(--commons))",
            dark: "#005434",
            darker: "#004229",
          },
          on_commons: colors.white,
          lords: {
            DEFAULT: "rgb(var(--lords))",
            dark: "#540016",
            darker: "#420012",
          },
          on_lords: colors.white,
        },
      },
      listStyleType: {
        square: "square",
      },
      transitionDuration: {
        DEFAULT: "220ms",
      },
    },
  },
  plugins: [],
} satisfies Config;
