import React from "react";
import Card from "./card";
import bgimg from "../../public/images/bg2.jpg";
import Container from "../Components/Navbar/Container";

const HowToUsePage = () => {
    const cardsData = [
        {
          title: "Navigasi",
          content:
            "Navigasikan website menggunakan tombol pada bagian kanan atas; 'Home,' 'How to Use,' , `About Us`, `About Project` dan `Camera'.",
        },
        {
          title: "Membandingkan Gambar",
          content:
            "Untuk membandingkan gambar, tekan tombol ‘Home’ dan pilih metode yang diinginkan; ‘Color’ atau ‘Tekstur.’",
        },
        {
          title: "Unggah Gambar dan Dataset",
          content:
            "Unggah gambar Anda pada kotak sebelah kiri ('Upload your image!') dan dataset (dalam bentuk folder) Anda pada kotak sebelah kanan ('Upload your dataset!').",
        },
        {
          title: "Proses Perbandingan",
          content:
            "Tekan tombol 'Search!' di bagian bawah untuk memulai proses perbandingan; tunggu hingga proses selesai untuk waktu lama proses muncul di layar.",
        },
        {
          title: "Hasil Perbandingan",
          content:
            "Gambar dataset yang memiliki kemiripan akan muncul secara urut. Untuk menavigasikan hasil perbandingan, gunakan tombol dengan angka.",
        },
        {
          title: "Mengganti Gambar atau Dataset",
          content:
            "Untuk mengganti gambar atau dataset yang telah diunggah, masing-masing tekan tombol 'Change your image?' atau 'Change your dataset?'.",
        },
        {
          title: "Akses Laman Web Lainnya",
          content:
            "Untuk mengakses laman web lainnya, tekan tombol ‘How to Use’ untuk instruksi penggunaan dan tombol ‘About Us’ untuk informasi tentang kami.",
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
          height: "100vh", // Adjust the height as needed
          position: "fixed",
          top: 0,
          left: 0,
          zIndex: -1, // Set a lower z-index for the background
        }}
      />

      <div className="relative z-10">
        <center>
          <Container>
            <div className="rounded-full">
              <h1 className="text-6xl font-bold text-black py-5">Cara Menggunakan</h1>
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
      </div>
    </>
  );
};

export default HowToUsePage;
