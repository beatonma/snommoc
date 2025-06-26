import { Todo } from "@/components/dev";
import { PageLayout } from "@/components/page-layout";

export default function Home() {
  return (
    <PageLayout layout="CenteredFeed">
      <Todo message="home page" />
    </PageLayout>
  );
}
