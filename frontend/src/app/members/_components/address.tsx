import { type PhysicalAddress as PhysicalAddressData } from "@/api/schema";
import { OptionalDiv } from "@/components/optional";
import { WebLinks } from "@/features/weblinks";
import { Props } from "@/types/react";
import { addClass, transformString } from "@/util/transforms";

export const PhysicalAddress = (
  props: Props<"address", PhysicalAddressData>,
) => {
  const { description, address, postcode, phone, fax, email, ...rest } =
    addClass(props, "column gap-y-1.5");

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

      <WebLinks
        layout="column"
        links={[
          transformString(phone, (it) => `tel:${it}`),
          transformString(fax, (it) => `fax:${it}`),
          transformString(email, (it) => `mailto:${it}`),
        ]}
      />
    </address>
  );
};
