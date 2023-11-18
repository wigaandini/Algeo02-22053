import Container from "./Components/Navbar/Container";
import bgimg from "../public/images/bgimg.jpg";
import Form from "./Components/form"; // Correct the import path
import opening from "../public/images/bgimgg.png";
import Image from "next/image";
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
          <div className="rounded-full">
            <Image
              src={opening}
              alt="opening"
              width={1320}
              height={1320}
              className="rounded-3xl border-2 border-[#757376]"
            />
          </div>

          <Form />
        </Container>
      </center>
    </>
  );
}
