import Image from "next/image";
import Container from "./Components/Navbar/Container";
import bgimg from "../public/images/a01d217e994a3b17bd7a4f7d4ab3c98f.jpg"

export default function Home() {
  return (
    <>
      <div
        className="z-0" // Set the z-index to 0 for the background image
      >
        <Image
          src={bgimg} // Replace with the actual path to your background image
          alt="Background Image"
          layout="fill"
          objectFit="cover"
        />
      </div>

      <Container>
        <div className="relative z-1 pt-8 text-center flex flex-row items-baseline justify-center gap-5">
          <div className="font-sans text-8xl">Reverse</div>
          <div className="font-sans text-5xl">Image</div>
        </div>

        <div className="relative z-1 text-center font-sans text-5xl pt-10">Search</div>
      </Container>
    </>
  );
}
