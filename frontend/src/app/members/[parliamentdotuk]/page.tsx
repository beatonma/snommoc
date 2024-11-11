import client from "@/lib/api";
import api from "@/lib/api/api";
import Image from "next/image";

export default async function Page({
  params,
}: {
  params: Promise<{ parliamentdotuk: number }>;
}) {
  const parliamentdotuk = (await params).parliamentdotuk;
  const response = await client.GET("/api/members/{parliamentdotuk}/", {
    params: {
      path: {
        parliamentdotuk: parliamentdotuk,
      },
    },
  });

  const error = response.error;
  if (error) {
    return <pre>{JSON.stringify(error)}</pre>;
  }

  return <MemberProfile {...response.data} />;
}

type Member = api.components["schemas"]["MemberProfile"];
const MemberProfile = (props: Member) => {
  return (
    <div>
      <Image
        loading="lazy"
        className="aspect-square w-32 rounded-lg bg-gray-800"
        src={props.portrait ?? "/default-member-portrait.svg"}
        alt={`Portrait of ${props.name}`}
        width={32}
        height={32}
      />
      <h1>{props.name}</h1>
    </div>
  );
};
