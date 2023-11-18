import React from "react";

interface CardProps {
  title: string;
  content: string;
}

const Card: React.FC<CardProps> = ({ title, content }) => {
  return (
    <div className="max-w-md mx-auto mb-4 p-6 bg-white rounded-xl shadow-md h-[175px]">
      <h2 className="font-louis text-2xl font-bold mb-4">{title}</h2>
      <p className="font-louis text-gray-600">{content}</p>
    </div>
  );
};

export default Card;
