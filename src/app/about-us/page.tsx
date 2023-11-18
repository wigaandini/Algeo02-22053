import Image from "next/image";
import Container from "../Components/Navbar/Container";
import bgimg from "../../public/images/bgimg.jpg";
import CardAbout from "./cardabout";
import placeholder from "../../public/images/placeholder.jpg";
import wiga from "../../public/images/wiga.gif";
import nuel from "../../public/images/nuel.gif";
import salsa from "../../public/images/salsa.gif";
import logowiga from "../../public/images/logowiga.png";
import logonuel from "../../public/images/logonuel.png";
import logosalsa from "../../public/images/logosalsa.png";


const AboutUs = () => {
  const aboutData = [
    {
      name: "Erdianti Wiga Putri Andini",
      photo: wiga.src,
      nim: "13522053",
      kesanPesan: "Fak kata gw teh",
      deskripsi:
        "Mba mba dari malang yang suka ama orang dari nangor kita sebut saja inisialnya W (for white) dan suka marah-marah.",
      logo: logowiga.src,
    },
    {
      name: "Imanuel Sebastian Girsang",
      photo: nuel.src,
      nim: "13522058",
      kesanPesan: "Kalo kata wiga tubes ini EZ banget",
      logo: logonuel.src,
      deskripsi:
        "Ga ada deskripsi, hehehhee",
    },
    {
      name: "Salsabiila",
      photo: salsa.src,
      nim: "13522062",
      kesanPesan: "Ditunggu Tahun Depan Lebih Susah lagi Tubesnya, terlalu ez kalo buat level pembuat soal pengkom",
      logo: logosalsa.src,
      deskripsi:
        "Pengcarry Handal Pengkom",
    },
  ];

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
          <div className="font-bakso relative z-1 text-8xl mt-10">Know</div>
          <div className="relative z-1 pt-8 text-center flex flex-row items-baseline justify-center gap-5">
            <div className="font-bakso text-5xl">The People</div>
            <div className="relative z-1 text-center font-bakso text-5xl pt-10">
              Behind this team
            </div>
          </div>
          <div className="flex flex-col justify-center items-center gap-10 pt-10">
            {aboutData.map((data, index) => (
              <CardAbout
                key={index} // Make sure to provide a unique key for each element in the array
                name={data.name}
                photo={data.photo}
                nim={data.nim}
                kesanPesan={data.kesanPesan}
                logo={data.logo}
                deskripsi={data.deskripsi}
              />
            ))}
          </div>
        </Container>
      </center>
    </>
  );
};

export default AboutUs;
