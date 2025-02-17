import { describe, test } from "@jest/globals";
import { resolveToRgb } from "@/components/themed/color";
import expect from "expect";

describe("Color tests", () => {
  test("resolveToRgb rgb", () => {
    expect(resolveToRgb("rgb(255, 0, 0)")).toEqual([255, 0, 0]);
    expect(resolveToRgb("rgb(0  255 0)")).toEqual([0, 255, 0]);
    expect(resolveToRgb("rgb(0, 0, 255)")).toEqual([0, 0, 255]);
  });

  test("resolveToRgb rgb numbers only", () => {
    expect(resolveToRgb("255, 0, 0")).toEqual([255, 0, 0]);
    expect(resolveToRgb("0  255 0")).toEqual([0, 255, 0]);
    expect(resolveToRgb("0, 0, 255")).toEqual([0, 0, 255]);
  });

  test("resolveToRgb rgb with alpha", () => {
    expect(resolveToRgb("rgb(0 0 255 / 50)")).toEqual([0, 0, 255]);
    expect(resolveToRgb("rgba(0, 0, 255, .5)")).toEqual([0, 0, 255]);
  });

  test("resolveToRgb hex codes", () => {
    expect(resolveToRgb("#ff0000")).toEqual([255, 0, 0]);
    expect(resolveToRgb("00ff00")).toEqual([0, 255, 0]);
    expect(resolveToRgb("0000ff")).toEqual([0, 0, 255]);
  });
});
