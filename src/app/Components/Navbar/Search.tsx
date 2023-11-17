"use client";
import { useRouter } from "next/navigation";
import Logo from "./Logo";
const Search = () => {
  const router = useRouter();
  return (
    <>
      <Logo />
      <div
        className="
        opacity-90
        bg-[#FEFBD6]
        w-full
        md:w-auto
        py-2
        rounded-full
        shadow-xl
        transition
        cursor-pointer
        border-[2px]
        border-[#757376]"
      >
        <div
          className="
            flex flex-row items-center justify-between "
        >
          <div
            onClick={() => router.push(`/`)}
            className="
                text-md font-semibold px-6 text-[#F49082] transition-colors duration-200 ease-in-out hover:text-gray-600"
          >
            HOME
          </div>
          <div
            onClick={() => {
              router.push(`/about-us`);
            }}
            className="
                hidden
                sm:block
                text-sm
                text-[#F49082]
                font-semibold
                px-6
                border-x-[2px]
                border-[#757376]
                flex-1
                text-center
                transition-colors duration-200 ease-in-out hover:text-gray-600"
          >
            ABOUT US
          </div>
          <div
            onClick={() => router.replace(`/howto`)}
            className="
                text-sm font-semibold px-6 text-[#F49082] transition-colors duration-200 ease-in-out hover:text-gray-600"
          >
            HOW TO USE
          </div>
          <div
            onClick={() => router.replace(`/camera`)}
            className="
                text-sm font-semibold px-6 text-[#F49082] transition-colors duration-200 ease-in-out hover:text-gray-600"
          >
            Camera
          </div>
        </div>
      </div>
    </>
  );
};

export default Search;
