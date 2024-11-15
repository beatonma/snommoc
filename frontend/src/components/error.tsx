export default function ErrorMessage({ error }: { error?: string }) {
  return (
    <div className="bg-red-800 text-white">
      {["Error", error].filter(Boolean).join(": ")}
    </div>
  );
}
