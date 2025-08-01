import { Metadata } from "next";
import { InlineLink } from "@/components/button";
import { ContentLayout } from "@/components/page-layout";
import { Prose } from "@/components/prose";
import { navigationHref } from "@/navigation";

export const metadata: Metadata = {
  title: "Privacy",
  description: "Privacy policy for Commons",
};

export default async function AboutPrivacyPage() {
  return (
    <ContentLayout layout="CenteredReadable" className="px-edge">
      <Prose>
        <section>
          <h1>Privacy Policy</h1>

          <h2>Terms</h2>
          <p>
            Commons is a personal project by{" "}
            <InlineLink href="https://beatonma.org" className="h-card u-url">
              Michael Beaton
            </InlineLink>
            . Any instance of <q>we</q> in this document refers to me, Michael,
            or the Commons service as a whole. No other humans are involved at
            this time.
          </p>
        </section>

        <section>
          <h2>What data is collected?</h2>

          <p>
            Commons is currently in demo mode: user accounts are not enabled and
            no user data is collected.
          </p>

          <h3>Without an account</h3>
          <p>If you do not create an account, no data is collected.</p>

          <h3>With an account</h3>
          <p>
            If you choose to sign in with Google, we will create a Commons
            account which will be associated with your Google account ID and
            stored on the Commons service.
          </p>
          <p>
            The name, photo, and email address associated with your Google
            account may be stored on your device for the purposes of showing you
            which Google account you are using. These will never be sent
            anywhere or displayed publicly - they are only visible to you.
          </p>

          <p>
            Your Commons account has a username which will be randomly generated
            when you create your account. Your username is public and may be
            visible alongside any content that you submit to the Commons
            service. You may edit your username in your account settings
            (subject to{" "}
            <InlineLink href={navigationHref("about", "moderation")}>
              moderation
            </InlineLink>
            ).
          </p>

          <p>
            You may delete any content that you have submitted via the Commons
            app. You may also delete your account along with any associated
            content. Deleting content removes it from public view immediately,
            but it may remain stored on the Commons service for up to 14 days
            for{" "}
            <InlineLink href={navigationHref("about", "moderation")}>
              moderation
            </InlineLink>{" "}
            purposes.
          </p>
        </section>

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
            This privacy policy is also on Github and you may review its edit
            history{" "}
            <InlineLink href="https://github.com/beatonma/snommoc/commits/main/frontend/src/app/(default-layout)/about/privacy/page.tsx">
              here
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
