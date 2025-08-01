import { Metadata } from "next";
import { InlineLink } from "@/components/button";
import { ContentLayout } from "@/components/page-layout";
import { Prose } from "@/components/prose";
import { SeparatedRow } from "@/components/row";
import { navigationHref } from "@/navigation";

export const metadata: Metadata = {
  title: "About",
  description: "About the Commons project",
};

export default async function AboutPage() {
  return (
    <ContentLayout layout="CenteredReadable" className="px-edge">
      <SeparatedRow className="colorful-links">
        <span>
          <InlineLink href={navigationHref("about", "privacy")}>
            Privacy policy
          </InlineLink>
        </span>
        <span>
          <InlineLink href={navigationHref("about", "moderation")}>
            Content moderation
          </InlineLink>
        </span>
      </SeparatedRow>

      <Prose className="my-em">
        <h1>About Commons</h1>

        <p>
          This project started as an attempt to make UK politics more engaging.
          It uses{" "}
          <InlineLink href="https://developer.parliament.uk/">
            UK parliament data
          </InlineLink>{" "}
          and displays it in readable, searchable, hopefully useful formats.
        </p>

        <p>
          Somewhere along the way I realised that I don&#39;t have solid vision
          of what it&#38;s actually supposed to be. Why should people use it,
          and why should they keep coming back to it? I still don&#39;t have a
          good answer for that. For a little more on its development history
          please see{" "}
          <InlineLink href="https://beatonma.org/apps/org-beatonma-commons/">
            here
          </InlineLink>
          .
        </p>

        <p>
          I still work on it for learning purposes but have no real intention of
          reaching a 1.0 release. It is now primarily a learning playground and,
          hopefully, a portfolio piece.
        </p>

        <p>
          All that is to say: the site you are viewing now is for{" "}
          <strong>demo purposes only</strong>. You are welcome to look around
          but beware that data is incomplete and not scheduled for regular
          updates because, for demo purposes, that would just be a waste of
          electricity.
        </p>

        <section>
          <h2>Source</h2>
          <div>
            The Commons service and associated apps are open source and
            available on Github:
            <ul className="mt-0">
              <li>
                <InlineLink href="https://github.com/beatonma/snommoc/">
                  Commons service and webapp
                </InlineLink>
              </li>
              <li>
                <InlineLink href="https://github.com/beatonma/commons/">
                  Commons for Android source
                </InlineLink>
              </li>
            </ul>
          </div>

          <p>
            Data comes from{" "}
            <InlineLink href="https://developer.parliament.uk/">
              UK parliament APIs
            </InlineLink>{" "}
            and is used under the terms of the{" "}
            <InlineLink href="https://www.parliament.uk/site-information/copyright-parliament/open-parliament-licence/">
              Open Parliament Licence v3.0
            </InlineLink>
            .
          </p>
        </section>

        <section>
          <h2>Contact</h2>
          <p>
            If you have any queries you are welcome to contact me using the form
            at{" "}
            <InlineLink href="https://beatonma.org/contact/">
              beatonma.org/contact/
            </InlineLink>
            , or by email at{" "}
            <InlineLink href="mailto:common@beatonma.org">
              commons@beatonma.org
            </InlineLink>
            .
          </p>
        </section>
      </Prose>
    </ContentLayout>
  );
}
