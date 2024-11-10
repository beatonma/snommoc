import client from "@/lib/api";
import api from "@/lib/api/api";
import Image from "next/image";
import { Optional } from "@/components/optional";

export default async () => {
  const response = await client.GET("/api/members/");
  const data = response.data;
  const members = data?.items;
  const error = response.error;
  if (error) {
    return <pre>{JSON.stringify(error)}</pre>;
  }

  return (
    <div className="m-2 grid grid-cols-[repeat(auto-fit,minmax(120px,360px))] justify-center gap-0.5">
      {members?.map((member) => (
        <Member key={member.parliamentdotuk} {...member} />
      ))}
    </div>
  );
};

type MemberSchema = api.components["schemas"]["MemberMiniSchema"];
const Member = (props: MemberSchema) => {
  return (
    <a
      href={`${props.parliamentdotuk}/`}
      className="flex gap-2 bg-slate-700 p-3 text-white"
    >
      <Image
        loading="lazy"
        className="aspect-square w-16 rounded-lg bg-gray-800"
        src={props.portrait ?? "/default-member-profile.svg"}
        alt={`Portait of ${props.name}`}
        width={16}
        height={16}
      />
      <div>
        <h1 className="text-md font-semibold">{props.name}</h1>
        <Optional
          condition={props.current_post}
          children={(it) => <div className="text-xs">{it}</div>}
        />
        <Optional
          condition={props.constituency?.name}
          children={(it) => <div className="text-xs">{`MP for ${it}`}</div>}
        />
      </div>
    </a>
  );
};
