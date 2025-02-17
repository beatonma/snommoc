type ThreeChannel = [number, number, number];

export const getOnColor = (
  backgroundColorRgb: string | undefined,
): string | undefined => {
  if (!backgroundColorRgb) return undefined;
  const rgb = resolveToRgb(backgroundColorRgb);
  if (!rgb || rgb.length !== 3) return undefined;

  const [r, g, b] = normalized(rgb) as ThreeChannel;

  const luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b;

  const mixer = luminance > 0.5 ? "black" : "white";

  return `color-mix(in srgb, ${backgroundColorRgb} 15%, ${mixer})`;
};

export const resolveToRgb = (
  color: string | undefined,
): ThreeChannel | undefined => {
  if (!color) return undefined;

  if (color.includes("--")) {
    const cssName = color.match(/var\((--[^)\s]+)\)/)?.[1];
    if (!cssName) return undefined;

    return resolveToRgb(
      document.body.computedStyleMap().get(cssName)?.toString(),
    );
  }

  return rgbToRgb(color) ?? hexToRgb(color);
};

const normalized = (rgb: number[]) => rgb.map((it) => it / 255);

const rgbToRgb = (rgb: string): ThreeChannel | undefined => {
  try {
    return rgb
      .match(/^(?:rgba?\()?(\d+)[\s,]+(\d+)[\s,]+(\d+)(?:[/,\s\d.]+)?\)?$/)
      ?.slice(1)
      ?.map((it) => {
        const asNumber = parseInt(it);
        if (isNaN(asNumber))
          throw new Error(`Failed to parse color as RGB: ${rgb} ${it}`);
        return asNumber;
      }) as ThreeChannel;
  } catch (e) {
    console.debug(e);
    return undefined;
  }
};

const hexToRgb = (hex: string): ThreeChannel | undefined => {
  hex = hex.replace("#", "");

  const pattern = {
    3: /^([a-f\d])([a-f\d])([a-f\d])$/i,
    6: /^([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i,
    8: /^([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i,
  }[hex.length];
  if (!pattern) return undefined;

  try {
    return hex
      .match(pattern)
      ?.slice(1)
      ?.map((it) => {
        const asNumber = parseInt(it, 16);
        if (isNaN(asNumber))
          throw new Error(`Failed to convert hex to RGB: ${hex}`);
        return asNumber;
      }) as ThreeChannel;
  } catch (e) {
    console.debug(e);
    return undefined;
  }
};
