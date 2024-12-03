import { default as NextImage, ImageProps } from "next/image";
import React from "react";
import { StaticImport } from "next/dist/shared/lib/get-img-props";

interface OptionalImage {
  src: string | StaticImport | undefined | null;
}
type OptionalImageProps = Omit<ImageProps, keyof OptionalImage> & OptionalImage;
export const OptionalImage = (props: OptionalImageProps) => {
  const { src, ...rest } = props;
  if (src) {
    return <NextImage src={src} {...rest} />;
  }
};

export const OptionalSvg = (props: OptionalImageProps) => {
  return <OptionalImage {...props} width={1} height={1} />;
};
