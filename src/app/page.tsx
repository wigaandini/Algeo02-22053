import Container from "./Components/Navbar/Container";
import bgimg from "../public/images/bgimg.jpg";
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
          <div className="font-bakso relative z-1 text-8xl mt-10">Content Based</div>
          <div className="relative z-1 pt-8 text-center flex flex-row items-baseline justify-center gap-5">
            <div className="font-bakso text-5xl">Image</div>
            <div className="relative z-1 text-center font-bakso text-5xl pt-10">
              Retrieval
            </div>
          </div>
          <Form />
        </Container>
      </center>
    </>
  );
}
