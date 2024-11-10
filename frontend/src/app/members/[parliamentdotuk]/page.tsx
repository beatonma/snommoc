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

type Member = api.components["schemas"]["MemberFullSchema"];
const MemberProfile = (props: Member) => {
  const { profile } = props;

  return (
    <div>
      <Image
        loading="lazy"
        className="aspect-square w-32 rounded-lg bg-gray-800"
        src={profile.portrait ?? "/default-member-profile.svg"}
        alt={`Portait of ${profile.name}`}
        width={32}
        height={32}
      />
      <h1>{profile.name}</h1>
    </div>
  );
};
