import Image from "next/image";
import Container from "./Components/Navbar/Container";
import bgimg from "../public/images/a01d217e994a3b17bd7a4f7d4ab3c98f.jpg";
import Form from "./Components/form"; // Correct the import path

export default function Home() {
  return (
    <>
      <div className="relative z-0">
        {/* Use CSS to set the background image */}
        <div
          style={{
            backgroundImage: `url(${bgimg.src})`,
            backgroundSize: "cover",
            backgroundPosition: "center",
            width: "100%",
            height: "100vh", // Adjust the height as needed
            position: "fixed",
            top: 0,
            left: 0,
          }}
        />
      </div>
      <center>
        <Container>
          <div className="relative z-1 pt-8 text-center flex flex-row items-baseline justify-center gap-5">
            <div className="font-sans text-8xl">Reverse</div>
            <div className="font-sans text-5xl">Image</div>
          </div>

          <div className="relative z-1 text-center font-sans text-5xl pt-10">
            Search
          </div>
          <Form />
        </Container>
      </center>
    </>
  );
}
