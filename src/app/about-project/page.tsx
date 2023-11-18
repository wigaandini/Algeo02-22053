import Image from "next/image";
import React from "react";
import Container from "../Components/Navbar/Container";
import bgimg from "../../public/images/bg2.jpg";
import nextjs from "../../public/images/nextjs.png";
import flask from "../../public/images/flask.png";
import tailwind from "../../public/images/tailwind.png";
import typescript from "../../public/images/ts.png";
import python from "../../public/images/python.png";
const AboutProject = () => {
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
        <Container>
          <div className="rounded-3xl container mx-auto my-10 p-8 bg-white shadow-md">
            <center>
              <h1 className="font-lemon text-3xl font-bold mb-6">
                Tentang Project Ini
              </h1>
            </center>
            <div className="font-louis text-lg">
              <p className="mb-4">
                Program Image Search Engine yang kami buat adalah aplikasi
                aljabar vektor dalam sistem temu balik gambar. Dengan adanya
                sistem temu balik gambar (image retrieval system), pengguna
                dapat dengan mudah mencari, mengakses, dan mengelola koleksi
                gambar mereka. Dalam konteks ini, aljabar vektor digunakan untuk
                menggambarkan dan menganalisis data melalui pendekatan
                klasifikasi berbasis konten (Content-Based Image Retrieval atau
                CBIR), di mana sistem temu balik gambar bekerja dengan
                mengidentifikasi gambar berdasarkan konten visual seperti warna
                dan tekstur.
              </p>

              <p className="mb-4">
                Content Based Image Retrieval System (CBIR) merupakan proses
                yang digunakan untuk mencari dan mengambil gambar berdasarkan
                kontennya. Kami menggunakan 2 tipe CBIR, yaitu CBIR dengan
                parameter warna dan CBIR dengan parameter tekstur.
              </p>

              <p className="mb-4">
                Cara kami menganalisis gambar dengan CBIR warna adalah
                berdasarkan nilai HSV ini. Kami menghitung frekuensi kemunculan
                kombinasi HSV pada tiap pixel pada gambar. Frekuensi tersebut
                akan direpresentasikan sebagai suatu vektor yang berukuran 72.
                Lalu untuk mencari kemiripan antara gambar satu dengan gambar
                lain, akan dihitung nilai cosine similarity antara vektor HSV
                gambar satu dengan vektor HSV gambar lainnya.
              </p>

              <p className="mb-4">
                Sedangkan cara kami menganalisis gambar dengan CBIR tekstur
                adalah membuat 6 fitur tekstur yang telah diekstraksi ke dalam
                bentuk vektor untuk masing-masing citra. Kemudian dihitung besar
                nilainya dalam persentase dengan menggunakan cosine similarity
                antara vektor fitur tekstur satu citra dengan yang lainnya.
              </p>

              <p className="mb-4">
                Kami menggunakan Next.js, Tailwind CSS, TypeScript, dan Flask
                untuk proyek ini.
              </p>
            </div>
            <div className="grid grid-cols-5 gap-4 mt-8 items-center justify-center">
              {/* Replace the paths and dimensions with your actual data */}
              <div className="w-full h-auto flex items-center justify-center">
                <Image
                  src={nextjs}
                  alt="Next.js Logo"
                  width={100}
                  height={50}
                />
              </div>
              <div className="w-full h-auto flex items-center justify-center">
                <Image
                  src={tailwind}
                  alt="Tailwind CSS Logo"
                  width={100}
                  height={50}
                />
              </div>
              <div className="w-full h-auto flex items-center justify-center">
                <Image
                  src={typescript}
                  alt="TypeScript Logo"
                  width={100}
                  height={50}
                />
              </div>
              <div className="w-full h-auto flex items-center justify-center">
                <Image src={flask} alt="Flask Logo" width={100} height={50} />
              </div>
              <div className="w-full h-auto flex items-center justify-center">
                <Image src={python} alt="Python Logo" width={100} height={50} />
              </div>
            </div>
          </div>
        </Container>

        {/* Konten halaman "About" sesuaikan dengan gaya "HowToUsePage" */}
        {/* ... (Tambahkan konten sesuai kebutuhan) */}
      </div>
    </>
  );
};

export default AboutProject;
