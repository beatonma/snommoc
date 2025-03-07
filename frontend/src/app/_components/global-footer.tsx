import { License } from "@/app/_components/licence";

export default function GlobalFooter() {
  return (
    <footer className="column items-center gap-2 p-8 pt-16 text-center">
      <License licence="OpenParliament" />
    </footer>
  );
}
