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
      colors: {
        surface: colors.neutral,
        primary: colors.slate,
        accent: colors.amber,
        house: {
          commons: {
            DEFAULT: "#006e46",
            dark: "#005434",
            darker: "#004229",
          },
          on_commons: colors.white,
          lords: {
            DEFAULT: "#b50938",
            dark: "#540016",
            darker: "#420012",
          },
          on_lords: colors.white,
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
