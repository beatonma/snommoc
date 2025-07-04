import React, { ReactNode } from "react";
import { InlineLink } from "@/components/button";
import { Licence, LicenceDefinition, licence } from "@/licensing";
import { DivPropsNoChildren } from "@/types/react";

interface LicenseProps {
  licence: Licence;
}
export const License = (props: DivPropsNoChildren<LicenseProps, "title">) => {
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
      <InlineLink href={url} title={name}>
        {attribution.map((attr, index) => (
          <p key={index}>{attr}</p>
        ))}
      </InlineLink>
    );
  }

  // Otherwise, linkify the licence name wherever it appears
  const linkified = (
    <InlineLink href={url} title={name}>
      {name}
    </InlineLink>
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

        return (
          <p key={index}>
            {results.map((it, i) => (
              <React.Fragment key={i}>{it}</React.Fragment>
            ))}
          </p>
        );
      })}
    </>
  );
};
