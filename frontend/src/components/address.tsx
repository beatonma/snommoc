import api from "@/lib/api/api";
import { OptionalDiv } from "@/components/optional";
import { ComponentPropsWithoutRef } from "react";
import { ButtonLink, LinkGroup } from "@/components/link";
import { addClass, transformString } from "@/util/transforms";

type PhysicalAddress = api.components["schemas"]["PhysicalAddressSchema"];
export const PhysicalAddress = (
  props: PhysicalAddress & ComponentPropsWithoutRef<"address">,
) => {
  const { description, address, postcode, phone, fax, email, ...rest } =
    addClass(props, "flex flex-col gap-y-1.5");

  return (
    <address {...rest}>
      <OptionalDiv className="text-xs" value={description} />

      <div>
        <OptionalDiv value={address} />
        <OptionalDiv value={postcode} />
      </div>

      <LinkGroup
        className="flex-col"
        links={[
          transformString(phone, (it) => `tel:${it}`),
          transformString(fax, (it) => `fax:${it}`),
          transformString(email, (it) => `mailto:${it}`),
        ]}
      />
    </address>
  );
};

type WebAddress = api.components["schemas"]["WebAddressSchema"];
export const WebAddress = (
  props: WebAddress & ComponentPropsWithoutRef<"address">,
) => {
  const { url, description, ...rest } = props;

  return (
    <address {...rest}>
      <ButtonLink href={url} defaultDisplayText={description ?? undefined} />
    </address>
  );
};
