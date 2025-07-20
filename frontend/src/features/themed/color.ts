import { Nullish } from "@/types/common";

type RGB = [number, number, number];
type HSL = [number, number, number];
const rgbToString = ([r, g, b]: RGB) => `rgb(${r}, ${g}, ${b})`;

const WcagContrast = 4.5; // https://www.w3.org/TR/WCAG21/#contrast-minimum
const PreferredContrast = 8;

export const getOnColor = (
  backgroundColor: string | Nullish,
  foregroundColor?: string | Nullish,
  element?: HTMLElement | Nullish,
): string | undefined => {
  if (!backgroundColor) return undefined;

  const resolvedBg = resolveToRgb(backgroundColor, element);
  const resolvedFg = resolveToRgb(foregroundColor ?? backgroundColor, element);
  if (!resolvedBg || !resolvedFg) {
    return undefined;
  }

  const adjusted = adjustContrast(resolvedBg, resolvedFg);
  return rgbToString(adjusted);
};

export const getContainerColor = (
  sourceColor: string | Nullish,
  foregroundColor: string | Nullish,
  maxSaturation: number = 0.25,
): string | undefined => {
  const resolvedSource = resolveToRgb(sourceColor);
  const resolvedForeground = resolveToRgb(foregroundColor);

  if (!resolvedSource || !resolvedForeground) return undefined;

  const adjusted = adjustContrast(
    resolvedForeground,
    reduceSaturation(resolvedSource, maxSaturation),
  );
  return rgbToString(adjusted);
};

const reduceSaturation = (color: RGB, maxSaturation: number): RGB => {
  const hsl = rgbToHsl(color);

  maxSaturation = Math.max(0, Math.min(1, maxSaturation));
  const saturation = hsl[1];
  hsl[1] = Math.min(saturation, maxSaturation);

  return hslToRgb(hsl);
};

const resolveToRgb = (
  color: string | Nullish,
  element?: HTMLElement | Nullish,
): RGB | undefined => {
  if (!color) return undefined;

  if (color.includes("--")) {
    const cssName = color.match(/var\((--[^)\s]+)\)/)?.[1];
    if (!cssName) return undefined;
    try {
      return resolveToRgb(
        (element ?? document.body).computedStyleMap().get(cssName)?.toString(),
      );
    } catch (e) {
      if (e instanceof ReferenceError) {
        // document not available on server
        return undefined;
      }
      throw e;
    }
  }

  return rgbToRgb(color) ?? hexToRgb(color);
};

/**
 * Return a variant of `foreground` which has a sufficient contrast ratio with `background`.
 */
const adjustContrast = (
  relativeTo: RGB,
  adjustable: RGB,
  minContrast: number = PreferredContrast,
): RGB => {
  if (minContrast < WcagContrast) {
    console.warn(
      `adjustContrast minContrast should be at least ${WcagContrast} (got ${minContrast})`,
    );
  }
  const againstLuminance = getLuminance(relativeTo);

  const step = 5;

  // Try and find a suitable contrast by adjusting towards black
  let adjusted: RGB = [...adjustable];

  for (let i = 0; i < 100; i++) {
    if (
      getContrastRatio(againstLuminance, getLuminance(adjusted)) > minContrast
    ) {
      return adjusted;
    }

    if (adjusted.every((it) => it === 0)) {
      // Already reached black. Try going the other direction instead.
      break;
    }

    const [r, g, b] = adjusted;

    adjusted = [
      Math.max(0, r - step),
      Math.max(0, g - step),
      Math.max(0, b - step),
    ];
  }

  adjusted = [...adjustable];
  for (let i = 0; i < 100; i++) {
    if (
      getContrastRatio(againstLuminance, getLuminance(adjusted)) > minContrast
    ) {
      return adjusted;
    }

    if (adjusted.every((it) => it === 255)) {
      // Already reached white
      break;
    }

    const [r, g, b] = adjusted;

    adjusted = [
      Math.min(255, r + step),
      Math.min(255, g + step),
      Math.min(255, b + step),
    ];
  }
  return adjusted;
};

const getLuminance = (rgb: RGB): number => {
  const [r, g, b] = rgb.map((val) => {
    const sRGB = val / 255;
    return sRGB <= 0.03928
      ? sRGB / 12.92
      : Math.pow((sRGB + 0.055) / 1.055, 2.4);
  }) as RGB;
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};

const getContrastRatio = (luminance1: number, luminance2: number): number => {
  const lighter = Math.max(luminance1, luminance2);
  const darker = Math.min(luminance1, luminance2);
  return (lighter + 0.05) / (darker + 0.05);
};

/*
 * Color format conversions
 */
const rgbToRgb = (rgb: string): RGB | undefined => {
  try {
    return rgb
      .match(/^(?:rgba?\()?(\d+)[\s,]+(\d+)[\s,]+(\d+)(?:[/,\s\d.]+)?\)?$/)
      ?.slice(1)
      ?.map((it) => {
        const asNumber = parseInt(it);
        if (isNaN(asNumber))
          throw new Error(`Failed to parse color as RGB: ${rgb} ${it}`);
        return asNumber;
      }) as RGB;
  } catch (e) {
    console.debug(e);
    return undefined;
  }
};

const hexToRgb = (hex: string): RGB | undefined => {
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
      }) as RGB;
  } catch (e) {
    console.debug(e);
    return undefined;
  }
};

const rgbToHsl = ([r, g, b]: RGB): HSL => {
  const red = r / 255;
  const green = g / 255;
  const blue = b / 255;

  const max = Math.max(red, green, blue);
  const min = Math.min(red, green, blue);
  let h = 0;
  let s = 0;
  const l = (max + min) / 2;

  if (max === min) {
    h = s = 0;
  } else {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);

    switch (max) {
      case red:
        h = (green - blue) / d + (green < blue ? 6 : 0);
        break;
      case green:
        h = (blue - red) / d + 2;
        break;
      case blue:
        h = (red - green) / d + 4;
        break;
    }
    h /= 6;
  }

  return [h, s, l];
};

const hslToRgb = ([hue, saturation, lightness]: HSL): RGB => {
  let r = 0;
  let g = 0;
  let b = 0;

  if (saturation === 0) {
    r = g = b = lightness; // achromatic
  } else {
    const hue2rgb = (p: number, q: number, t: number) => {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1 / 6) return p + (q - p) * 6 * t;
      if (t < 1 / 2) return q;
      if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
      return p;
    };

    const q =
      lightness < 0.5
        ? lightness * (1 + saturation)
        : lightness + saturation - lightness * saturation;
    const p = 2 * lightness - q;

    r = hue2rgb(p, q, hue + 1 / 3);
    g = hue2rgb(p, q, hue);
    b = hue2rgb(p, q, hue - 1 / 3);
  }

  return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
};

export const _private = { resolveToRgb };
