import Container from "../Components/Navbar/Container";
import bgimg from "../../public/images/bgimg.jpg";
import Form from "../Components/formforcamera"; // Correct the import path

export default function Camera() {
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
          <div className="font-lemon relative z-1 text-6xl mt-10">
            Try Out Our Camera !
          </div>
          
          <Form />
        </Container>
      </center>
    </>
  );
}
