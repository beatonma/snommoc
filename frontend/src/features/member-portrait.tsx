import Image from "next/image";
import React from "react";
import Icon from "@/components/icon";
import { ImageWithFallback } from "@/components/image";
import { Nullish } from "@/types/common";
import { DivPropsNoChildren, Props } from "@/types/react";
import { addClass, classes } from "@/util/transforms";

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

  const resolvedAspect = PortraitAspectValues[aspect];
  const resolvedWidth =
    width === "parliament-thumbnail" ? ParliamentThumbnailSize : width;
  const height = Math.ceil(resolvedWidth / resolvedAspect.ratio);

  if (!src) {
    return (
      <FallbackImage className={classes(className, resolvedAspect.className)} />
    );
  }

  return (
    <ImageWithFallback
      src={src}
      fallback={
        <FallbackImage
          className={classes(className, resolvedAspect.className)}
        />
      }
      loading={priority ? undefined : "lazy"}
      width={resolvedWidth}
      height={height}
      alt={`Portrait of ${name}`}
      className={classes(className, resolvedAspect.className)}
      {...rest}
    />
  );
};

const FallbackImage = (props: DivPropsNoChildren) => {
  return (
    <div {...addClass(props, "flex items-center justify-center")}>
      <Icon
        icon="Commons"
        className="max-h-32 max-w-32 size-full aspect-square"
      />
    </div>
  );
};
