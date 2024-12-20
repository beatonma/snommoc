import { type PhysicalAddress as PhysicalAddressData } from "@/api";
import { OptionalDiv } from "@/components/optional";
import { ComponentPropsWithoutRef } from "react";
import { LinkGroup } from "@/components/link";
import { addClass, transformString } from "@/util/transforms";

export const PhysicalAddress = (
  props: PhysicalAddressData & ComponentPropsWithoutRef<"address">,
) => {
  const { description, address, postcode, phone, fax, email, ...rest } =
    addClass(props, "flex flex-col gap-y-1.5");

  return (
    <address {...rest}>
      <OptionalDiv className="text-xs" value={description} />

      <div>
        <OptionalDiv
          value={address}
          block={(it) =>
            it.split(",").map((line, index) => <p key={index}>{line.trim()}</p>)
          }
        />
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
