"use client";

type MitreBadgeProps = {
  technique?: string;
};

export default function MitreBadge({ technique }: MitreBadgeProps) {
  if (!technique || technique === "N/A") {
    return (
      <span className="px-2 py-1 text-xs bg-gray-600 rounded text-white">
        N/A
      </span>
    );
  }

  return (
    <span className="px-2 py-1 text-xs bg-purple-600 rounded text-white font-semibold">
      {technique}
    </span>
  );
}
