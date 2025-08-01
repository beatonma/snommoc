import { License } from "@/app/_components/licence";
import { InlineLink } from "@/components/button";
import { SeparatedRow } from "@/components/row";
import { navigationHref } from "@/navigation";

export const GlobalFooter = () => (
  <footer className="colorful-links p-8 pt-16 column gap-y-2 items-center text-center text-sm">
    <License licence="OpenParliament" />
    <SeparatedRow horizontal="justify-center">
      <span>
        <InlineLink href={navigationHref("about")}>
          About Commons
        </InlineLink>{" "}
      </span>

      <span>
        Made by{" "}
        <InlineLink href="https://beatonma.org">Michael Beaton</InlineLink>
      </span>

      <span>
        Source available on{" "}
        <InlineLink href="https://github.com/beatonma/snommoc">
          Github
        </InlineLink>
      </span>
    </SeparatedRow>
  </footer>
);
