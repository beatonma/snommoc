import Image from "next/image";

export default function Home() {
  return (
    <div className="grid min-h-screen grid-rows-[20px_1fr_20px] items-center justify-items-center gap-16 p-8 pb-20 font-[family-name:var(--font-geist-sans)] sm:p-20">
      <main className="row-start-2 flex flex-col items-center gap-8 sm:items-start">
        <a
          className="flex h-10 items-center justify-center gap-2 rounded-full border border-solid border-transparent bg-foreground px-4 text-sm text-background transition-colors hover:bg-slate-300 sm:h-12 sm:px-5 sm:text-base dark:hover:bg-slate-600"
          href="members/"
        >
          <Image
            src="/default-member-profile.svg"
            alt="Members"
            loading="lazy"
            width={20}
            height={20}
          />
          Members
        </a>
      </main>
    </div>
  );
}
