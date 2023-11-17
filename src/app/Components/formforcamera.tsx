"use client";
import Image from "next/image";
import { useState, useRef, useEffect } from "react";
import placeholder from "../../public/images/placeholder.jpg";
import Card from "../card";
import Webcam from "react-webcam";
interface response {
  similarity_score: number;
  image_path: string;
}

const FormCamera = () => {
  const inputRefFolder = useRef<HTMLInputElement>(null);
  const [image, setImage] = useState<File | null>(null);
  const [imagedataset, setImagedataset] = useState<File[] | null>(null);
  const [result, setResult] = useState<any[] | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [startTime, setStartTime] = useState<number | null>(null);
  const [method, setMethod] = useState<string>("Color");
  const [elapsedTime, setElapsedTime] = useState<number>(0);
  const [backgroundColor, setBackgroundColor] = useState<string>(
    "radial-gradient(circle, #fecccb, #ffd5c8, #ffe0c9, #ffebcc, #fef6d4)"
  );
  const webcamRef = useRef<Webcam>(null);

  const handleToggle = () => {
    if (method === "Color") {
      setMethod("Texture");
    } else {
      setMethod("Color");
    }
  };

  const handleFolderClick = () => {
    if (inputRefFolder.current) {
      inputRefFolder.current.click();
    }
  };

  const handleFolderUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = e.target.files;

    if (selectedFiles) {
      const filesArray = Array.from(selectedFiles);
      setImagedataset(filesArray);
      const randomSeed = Math.floor(Math.random() * 1000000).toString();
      const chunkSize = 999; // Define your desired chunk size

      for (let i = 0; i < filesArray.length; i += chunkSize) {
        const formData = new FormData();
        const chunk = filesArray.slice(i, i + chunkSize);

        chunk.forEach((file) => {
          formData.append("imagedataset", file);
        });
        formData.append("seed", randomSeed);

        try {
          const res = await fetch("http://localhost:5000/api/upload-folder", {
            method: "POST",
            body: formData,
          });

          if (!res.ok) {
            console.log("Error uploading folder");
          }
        } catch (error) {
          console.error("Error uploading folder:", error);
        }
      }
    }
  };

  const itemsPerPage = 6;
  const [currentPage, setCurrentPage] = useState(1);
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentImages = result?.slice(indexOfFirstItem, indexOfLastItem);

  const totalPages = Math.ceil((result?.length || 0) / itemsPerPage);
  const calculatePageRange = () => {
    const totalPageCount = Math.min(5, totalPages);
    const startPage = Math.max(1, currentPage - Math.floor(totalPageCount / 2));
    const endPage = Math.min(startPage + totalPageCount - 1, totalPages);
    return Array.from(
      { length: Math.min(totalPageCount, endPage - startPage + 1) },
      (_, index) => startPage + index
    );
  };

  const handleNextPage = () => {
    setCurrentPage(totalPages);
  };

  const handlePrevPage = () => {
    setCurrentPage(1);
  };

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setStartTime(new Date().getTime()); // Set the start time
    setCurrentPage(1);

    try {
      const formData = new FormData();
      formData.append("file_name", image!.name);

      const res = await fetch(
        `http://localhost:5000/api/process_image_similarity/${method}`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await res.json();

      setLoading(false);
      setStartTime(null);

      if (res.ok) {
        setResult(data.similarity_results);
      } else {
        console.log("Error");
        setResult(null);
      }
    } catch (error) {
      console.error("Error:", error);
      setLoading(false);
      setResult(null);
      setStartTime(null);
    }
  };

  useEffect(() => {
    let intervalId: NodeJS.Timeout;

    // Update elapsed time every second
    if (startTime) {
      intervalId = setInterval(() => {
        const currentTime = new Date().getTime();
        const elapsedTime = (currentTime - startTime) / 1000; // Convert to seconds
        setElapsedTime(elapsedTime); // Update state with the elapsed time
      }, 1000);
    }

    // Cleanup the interval when the component is unmounted or when the search is complete
    return () => {
      clearInterval(intervalId);
    };
  }, [startTime, result]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      const webcam = webcamRef.current;
      const canvas = document.getElementById("canvas") as HTMLCanvasElement;
      const context = canvas.getContext("2d");

      if (webcam && canvas && context) {
        const video = webcam.video as HTMLVideoElement;

        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        canvas.toBlob(async (blob) => {
          if (blob) {
            setImage(new File([blob], "image.jpg"));
          }
        }, "image/jpeg");
      }
    }, 20000);

    return () => clearInterval(intervalId);
  }, [webcamRef]);

  return (
    <div
      className="py-10 mt-5  rounded-lg w-[85%] justify-center"
      style={{
        background: backgroundColor,
        paddingLeft: "20px",
        paddingRight: "20px",
      }}
    >
      <form onSubmit={onSubmit} className="formbg">
        <div className="grid grid-cols-2 gap-4 ">
          <div>
            <label className="block mb-4 sm:text-xl md:text-2xl lg:text-4xl">{` ${
              image ? "Captured Image : " : "Capture Your Image!"
            }`}</label>
            <div className="relative object-contain w-[160px] md:w-[240px] lg:w-[320px] xl:w-[480px] h-[90px] md:h-[135px] lg:h-[180px] xl:h-[270px] mb-4">
              <Webcam
                id="video"
                audio={false}
                ref={webcamRef}
                width="100%"
                height="100%"
                screenshotFormat="image/jpeg"
              />
              <canvas id="canvas" style={{ display: "none" }} />
              <Image
                alt="Captured Image"
                src={image ? URL.createObjectURL(image) : placeholder}
                fill
              />
            </div>
          </div>
          <div>
            <label className="block mb-4 sm:text-xl md:text-2xl lg:text-4xl">{`${
              imagedataset
                ? `Dataset : ${imagedataset.length} images `
                : "Upload Your Dataset!"
            }`}</label>
            <div className="relative object-contain w-[160px] md:w-[240px] lg:w-[320px] xl:w-[480px] h-[90px] md:h-[135px] lg:h-[180px] xl:h-[270px] mb-4">
              <Image
                alt="Uploaded Image"
                src={
                  imagedataset
                    ? URL.createObjectURL(imagedataset[0])
                    : placeholder
                }
                fill
              />
            </div>
            <input
              type="file"
              webkitdirectory="true"
              multiple
              className="hidden"
              ref={inputRefFolder}
              onChange={handleFolderUpload}
              required
              accept="image/*"
              name="folderupload"
            />
            <button
              type="button"
              onClick={handleFolderClick}
              className="border-[2px] border-[#757376] bg-[#FEFBD6] p-2 rounded-full text-[#005B4A] transition-colors duration-200 ease-in-out hover:text-gray-600 hover:shadow-lg"
            >
              {`${imagedataset ? "Change Your Dataset?" : "Upload Folder"}`}
            </button>
          </div>
        </div>

        {loading ? (
          <div className="mt-4 text-center">
            <div className="animate-pulse">Loading Image Similarity...</div>
            <p className="mt-2 text-gray-500">{`Time: ${elapsedTime.toFixed(
              2
            )} seconds`}</p>{" "}
            {/* Display elapsed time */}
          </div>
        ) : currentImages ? (
          currentImages.length > 0 ? (
            <div>
              <h1 className="text-xl sm:text-2xl md:text-3xl lg:text-4xl py-10">{`${result?.length} images in ${elapsedTime} seconds`}</h1>
              <div className="flex flex-wrap justify-center gap-10">
                {currentImages.map((response, index) => (
                  <div
                    key={index}
                    className={`relative flex items-center justify-center w-[160px] md:w-[240px] xl:w-[320px] h-[160px] md:h-[240px] xl:h-[320px] mb-4 mt-4`}
                  >
                    <Card
                      image={response.image_path}
                      similarity={response.similarity_score}
                    />
                  </div>
                ))}
              </div>
              {/* Pagination Codes */}
              <div className="flex justify-center mt-4">
                <button
                  type="button"
                  onClick={handlePrevPage}
                  disabled={currentPage === 1}
                  className={`disabled:opacity-70 disabled:cursor-not-allowed mx-2 px-4 py-2 rounded-full border-[2px] border-[#757376] bg-[#FEFBD6] text-[#005B4A] transition-all duration-200 ease-in-out hover:text-gray-600 hover:shadow-lg`}
                >
                  Start
                </button>
                <div className="flex">
                  {calculatePageRange().map((pageNumber) => (
                    <button
                      key={pageNumber}
                      type="button"
                      onClick={() => setCurrentPage(pageNumber)}
                      className={`mx-2 px-4 py-2 rounded-full border-[2px] border-[#757376] ${
                        pageNumber === currentPage
                          ? "bg-[#FEFBD6] text-[#005B4A]"
                          : "bg-white text-[#005B4A]"
                      } transition-all duration-200 ease-in-out hover:text-gray-600 hover:shadow-lg`}
                    >
                      {pageNumber}
                    </button>
                  ))}
                </div>
                <button
                  type="button"
                  onClick={handleNextPage}
                  disabled={currentPage === totalPages}
                  className={`disabled:opacity-70 disabled:cursor-not-allowed mx-2 px-4 py-2 rounded-full border-[2px] border-[#757376] bg-[#FEFBD6] text-[#005B4A] transition-all duration-200 ease-in-out hover:text-gray-600 hover:shadow-lg`}
                >
                  End
                </button>
              </div>
            </div>
          ) : (
            <h1>Tidak ada gambar yang mirip !</h1>
          )
        ) : null}

        <button
          type="submit"
          disabled={loading || !image || !imagedataset}
          className={`disabled:opacity-70 disabled:cursor-not-allowed mx-2 px-4 mt-10 py-2 rounded-full border-[2px] border-[#757376] bg-[#FEFBD6] text-[#005B4A] transition-all duration-200 ease-in-out hover:text-gray-600 hover:shadow-lg`}
        >
          Search!
        </button>
      </form>
    </div>
  );
};

export default FormCamera;
