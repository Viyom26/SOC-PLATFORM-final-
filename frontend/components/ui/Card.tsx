"use client";

import "./card.css";

type Props = {
  title: string;
  children: React.ReactNode;
};

export default function Card({ title, children }: Props) {
  return (
    <div className="card-container">
      <h3 className="card-title">{title}</h3>
      {children}
    </div>
  );
}
