import { Todo } from "@/components/dev";
import { ContentLayout } from "@/components/page-layout";

export default function Home() {
  return (
    <ContentLayout layout="CenteredFeed">
      <Todo message="home page" />
    </ContentLayout>
  );
}
