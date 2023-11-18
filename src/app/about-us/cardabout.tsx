"use client";
import React, { useEffect, useState } from "react";

interface CardAboutProps {
  name: string;
  photo: string;
  nim: string;
  kesanPesan: string;
  logo: string;
  deskripsi: string;
}

const CardAbout: React.FC<CardAboutProps> = ({
  name,
  photo,
  nim,
  kesanPesan,
  logo,
  deskripsi,
}) => {
  const [backgroundColor, setBackgroundColor] = useState<string>("");
  useEffect(() => {
    setBackgroundColor(
      "radial-gradient(circle, #fecccb, #ffd5c8, #ffe0c9, #ffebcc, #fef6d4)"
    );
  }, []);
  return (
    <div
      className="grid grid-cols-2 w-[85%] items-center  p-10 rounded-3xl border-2 border-black shadow-xl"
      style={{
        background: backgroundColor,
      }}
    >
      <div className="flex flex-col gap-10 justify-center items-center">
        <div className="flex flex-col gap-10 justify-center">
          <h1 className="font-lemon text-5xl font-bold">
            {name} - {nim}
          </h1>
          <h3 className="text-xl font-louis">{deskripsi}</h3>
        </div>
        <div>
          <p className="text-lg font-lemon">Kesan Pesan Tubes: </p>
          <p className="text-lg font-louis">"{kesanPesan}"</p>
        </div>
        <img src={logo} alt="Logo" className="w-20 h-20 mt-2" />
      </div>
      <div className="justify-center items-center">
        <img
          src={photo}
          alt="Profile Photo"
          className="w-[500px] h-[500px] rounded-full"
        />
      </div>
    </div>
  );
};

export default CardAbout;
