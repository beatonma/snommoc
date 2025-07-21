import { License } from "@/app/_components/licence";
import { InlineLink } from "@/components/button";
import { SeparatedRow } from "@/components/row";

export const GlobalFooter = () => (
  <footer className="colorful-links p-8 pt-16 column gap-y-2 items-center text-sm">
    <License licence="OpenParliament" />
    <SeparatedRow>
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
