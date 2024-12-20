import { ComponentPropsWithoutRef, ReactNode } from "react";
import { TextLink } from "@/components/link";
import { Licence, licence, LicenceDefinition } from "@/licensing";

interface LicenseProps {
  licence: Licence;
}
export const License = (
  props: LicenseProps &
    Omit<ComponentPropsWithoutRef<"div">, "children" | "title">,
) => {
  const { licence: licenceKey, ...rest } = props;
  const licensing = licence(licenceKey);

  if (!licensing) throw new Error(`No licensing data for '${licenceKey}'`);

  return (
    <div {...rest}>
      <LinkifiedAttribution {...licensing} />
    </div>
  );
};

const LinkifiedAttribution = (props: LicenceDefinition) => {
  const { name, url, attribution } = props;

  if (!attribution.find((it) => it.includes(name))) {
    // If licence name not included in attribution text, linkify the whole text.
    return (
      <TextLink href={url} title={name}>
        {attribution.map((attr, index) => (
          <p key={index}>{attr}</p>
        ))}
      </TextLink>
    );
  }

  // Otherwise, linkify the licence name wherever it appears
  const linkified = (
    <TextLink href={url} title={name}>
      {name}
    </TextLink>
  );

  return (
    <>
      {attribution.map((attr, index) => {
        const parts = attr
          .split(name)
          .map((fragment, index) =>
            fragment ? <span key={index}>{fragment}</span> : "",
          );

        const lastIndex = parts.length - 1;
        const results: ReactNode[] = [];
        parts.forEach((part, index) => {
          results.push(part);
          if (index < lastIndex) {
            results.push(linkified);
          }
        });

        return <p key={index}>{results}</p>;
      })}
    </>
  );
};
