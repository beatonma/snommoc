export const ErrorMessage = ({ error }: { error?: string }) => (
  <div className="bg-red-800 text-white">
    {["Error", error].filter(Boolean).join(": ")}
  </div>
);
