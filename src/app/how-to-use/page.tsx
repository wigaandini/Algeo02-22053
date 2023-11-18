import React from "react";
import Card from "./card";
import bgimg from "../../public/images/bg2.jpg";
import Container from "../Components/Navbar/Container";

const HowToUsePage = () => {
  const cardsData = [
    {
      title: "1. Navigasi",
      content:
        "Navigasikan website menggunakan tombol pada bagian kanan atas; 'Home,' 'How to Use,' , `About Us`, `About Project` dan `Camera'.",
    },
    {
      title: "2. Membandingkan Gambar",
      content:
        "Untuk membandingkan gambar, tekan tombol ‘Home’ dan pilih metode yang diinginkan; ‘Color’ atau ‘Tekstur.’",
    },
    {
      title: "3. Unggah Gambar dan Dataset",
      content:
        "Unggah gambar Anda pada kotak sebelah kiri ('Upload your image!') dan dataset (dalam bentuk folder) Anda pada kotak sebelah kanan ('Upload your dataset!').",
    },
    {
      title: "4. Proses Perbandingan",
      content:
        "Tekan tombol 'Search!' di bagian bawah untuk memulai proses perbandingan; tunggu hingga proses selesai untuk waktu lama proses muncul di layar.",
    },
    {
      title: "5. Hasil Perbandingan",
      content:
        "Gambar dataset yang memiliki kemiripan akan muncul secara urut. Untuk menavigasikan hasil perbandingan, gunakan tombol dengan angka.",
    },
    {
      title: "6. Mengganti Gambar atau Dataset",
      content:
        "Untuk mengganti gambar atau dataset yang telah diunggah, masing-masing tekan tombol 'Change your image?' atau 'Change your dataset?'.",
    },
    {
      title: "7. Akses Laman Web Lainnya",
      content:
        "Untuk mengakses laman web lainnya, tekan tombol ‘How to Use’ untuk instruksi penggunaan dan tombol ‘About Us’ untuk informasi tentang kami.",
    },
  ];

  const cardsDataEnglish = [
    {
      title: "1. Navigation",
      content:
        "Navigate the website using the buttons in the top right; 'Home,' 'How to Use,' , `About Us`, `About Project`, and `Camera'.",
    },
    {
      title: "2. Compare Images",
      content:
        "To compare images, click 'Home' and choose the desired method; 'Color' or 'Texture.'",
    },
    {
      title: "3. Upload Image and Dataset",
      content:
        "Upload your image on the left box ('Upload your image!') and your dataset (as a folder) on the right box ('Upload your dataset!'). You can also scrape images from a website by clicking 'scrape image.'",
    },
    {
      title: "4. Initiate Comparison",
      content:
        "Click 'Search!' at the bottom to initiate the comparison; wait for the process completion time to display.",
    },
    {
      title: "5. View Results",
      content:
        "Similar dataset images will appear, ordered by similarity. Navigate through pages using numbered buttons.",
    },
    {
      title: "6. Change Uploaded Content",
      content:
        "Change your uploaded image or dataset by clicking 'Change your image?' or 'Change your dataset?' respectively.",
    },
    {
      title: "7. Explore Additional Pages",
      content:
        "To access other pages, click the 'How to Use' button for usage instructions and the 'About Us' button for information about us.",
    },
  ];

  return (
    <>
      <div
        style={{
          backgroundImage: `url(${bgimg.src})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          width: "100%",
          height: "100vh",
          position: "fixed",
          top: 0,
          left: 0,
          zIndex: -1,
        }}
      />

      <div className="relative">
        <center>
          <Container>
            <div className="rounded-full">
              <h1 className="text-6xl font-bold text-black py-5">
                Cara Menggunakan
              </h1>
            </div>
          </Container>
        </center>

        <div className="grid grid-cols-3 gap-4">
          {cardsData.map((card, index) => (
            <div key={index} className="mb-4">
              <Card title={card.title} content={card.content} />
            </div>
          ))}
        </div>

        <center>
          <Container>
            <div className="rounded-full">
              <h1 className="text-6xl font-bold text-black py-5">How to Use</h1>
            </div>
          </Container>
        </center>

        <div className="grid grid-cols-3 gap-4">
          {cardsDataEnglish.map((card, index) => (
            <div key={index} className="mb-4">
              <Card title={card.title} content={card.content} />
            </div>
          ))}
        </div>
      </div>
    </>
  );
};

export default HowToUsePage;
