import Image from "next/image";
import React from "react";
import Icon from "@/components/icon";
import { Nullish } from "@/types/common";
import { Props } from "@/types/react";
import { classes } from "@/util/transforms";

export const ParliamentThumbnailSize = 260; // Parliament-sourced thumbnail size

interface PortraitAspectValue {
  ratio: number;
  className: `aspect-${"square" | `[${number}/${number}]`}`;
}
const PortraitAspectValues = {
  "aspect-square": { ratio: 1, className: "aspect-square" },
  "aspect-wide": { ratio: 3 / 2, className: "aspect-[3/2]" },
  "aspect-tall": {
    ratio: 3 / 4,
    className: "aspect-[3/4]",
  },
} satisfies Record<string, PortraitAspectValue>;
type PortraitAspect = keyof typeof PortraitAspectValues;

type PortraitProps = Pick<
  Props<
    typeof Image,
    {
      name: string;
      width: number | "parliament-thumbnail";
      aspect: PortraitAspect;
      src: string | Nullish;
    }
  >,
  "name" | "width" | "src" | "aspect" | "className" | "priority"
>;

export const MemberPortrait = (props: PortraitProps) => {
  const {
    className,
    width,
    aspect = "aspect-square",
    name,
    src,
    priority,
    ...rest
  } = props;

  if (!src) {
    return (
      <Icon
        icon="Commons"
        className={className}
        width={width}
        height={width}
        {...rest}
      />
    );
  }

  const resolvedAspect = PortraitAspectValues[aspect];
  const resolvedWidth =
    width === "parliament-thumbnail" ? ParliamentThumbnailSize : width;
  const height = Math.ceil(resolvedWidth / resolvedAspect.ratio);

  return (
    <Image
      loading={priority ? undefined : "lazy"}
      width={resolvedWidth}
      height={height}
      src={src}
      alt={`Portrait of ${name}`}
      className={classes(className, resolvedAspect.className)}
      {...rest}
    />
  );
};
