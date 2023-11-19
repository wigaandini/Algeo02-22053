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

import { useMemo } from "react";

const Form = () => {
  const [image, setImage] = useState<File | null>(null);
  const [imagedataset, setImagedataset] = useState<File[] | null>(null);
  const [method, setMethod] = useState<string>("Color");
  const [startTime, setStartTime] = useState<number | null>(null);
  const [result, setResult] = useState<response[] | null>(null);
  const [imagestring, setImagestring] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [havescrapping, sethavescrapping] = useState(false);
  const [elapsedTime, setElapsedTime] = useState<number>(0); // Add state for elapsed time
  const [backgroundColor, setBackgroundColor] = useState<string>(
    "radial-gradient(circle, #fecccb, #ffd5c8, #ffe0c9, #ffebcc, #fef6d4)"
  );
  const [websiteUrl, setWebsiteUrl] = useState("");
  const [isScraping, setIsScraping] = useState(false);
  const [showBackdrop, setShowBackdrop] = useState(false);
  const [countdown, setCountdown] = useState(10);
  const [isCachedTexture, setIsCachedTexture] = useState(false);
  const [isCachedColor, setIsCachedColor] = useState(false);
  let initialTime = 40;
  if (imagedataset) {
    const length = imagedataset.length;
    if (
      (isCachedTexture && method === "Texture") ||
      (isCachedColor && method === "Color")
    ) {
      // Adjust Kalo ke cache
      if (length > 900) {
        initialTime = 20;
      } else if (length > 600) {
        initialTime = 15;
      } else if (length > 300) {
        initialTime = 10;
      } else {
        initialTime = 5;
      }
    } else {
      // Buat yang belum ke cache
      if (length > 1200) {
        initialTime = 70;
      } else if (length > 900) {
        initialTime = 60;
      } else if (length > 600) {
        initialTime = 50;
      } else if (length > 300) {
        initialTime = 40;
      }
    }
  }
  const inputRef = useRef<HTMLInputElement>(null);
  const inputRefFolder = useRef<HTMLInputElement>(null);
  const webcamRef = useRef(null);

  const imageSrc = useMemo(() => {
    return image ? URL.createObjectURL(image) : placeholder;
  }, [image, placeholder]);

  const imagedatasetSrc = useMemo(() => {
    // Check if imagedataset is an array and it has at least one element

    return imagedataset && imagedataset.length > 0
      ? havescrapping
        ? `/${imagedataset[0].replace(/\\/g, "/")}`
        : URL.createObjectURL(imagedataset[0])
      : placeholder;
  }, [imagedataset, placeholder]);

  const handlePhotoClick = () => {
    if (inputRef.current) {
      inputRef.current.click();
    }
  };

  const handleFolderClick = () => {
    if (inputRefFolder.current) {
      inputRefFolder.current.click();
    }
  };

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files && e.target.files[0];

    if (selectedFile) {
      setImage(selectedFile);

      const formData = new FormData();
      formData.append("image", selectedFile);

      try {
        const res = await fetch("http://localhost:5000/api/upload-image", {
          method: "POST",
          body: formData,
        });

        const data = await res.json();

        if (!res.ok) {
          console.log("Error uploading image");
        } else {
          setImagestring(data.image_path);
        }
      } catch (error) {
        console.error("Error uploading image:", error);
      }
    }
  };

  const handleFolderUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = e.target.files;
    sethavescrapping(false);
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
          if (method === "Texture") setIsCachedTexture(false);
          else if (method === "Color") setIsCachedColor(false);

          if (!res.ok) {
            console.log("Error uploading folder");
          }
        } catch (error) {
          console.error("Error uploading folder:", error);
        }
      }
    }
  };

  const handleToggleCheckbox = () => {
    setMethod((prevMethod) => (prevMethod === "Color" ? "Texture" : "Color"));
  };

  const handleWebsiteUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setWebsiteUrl(e.target.value);
  };

  const handleScrapeWebsite = () => {
    setIsScraping(true);
  };

  const handleCancelScraping = () => {
    setIsScraping(false);
    setWebsiteUrl(""); // Reset the entered URL
  };

  const handleCameraCapture = async () => {
    const webcam = webcamRef.current;
    const canvas = document.getElementById("canvas") as HTMLCanvasElement;
    const context = canvas.getContext("2d");

    if (webcam && canvas && context) {
      const video = webcam.video as HTMLVideoElement;

      context.drawImage(video, 0, 0, canvas.width, canvas.height);

      // Wrap canvas.toBlob() in a Promise
      const blob = await new Promise<Blob | null>((resolve) =>
        canvas.toBlob(resolve, "image/jpeg")
      );

      if (blob) {
        const imageconv = new File([blob], "image.jpg");
        setImage(imageconv);

        const formData = new FormData();
        formData.append("image", imageconv);

        try {
          const uploadRes = await fetch(
            "http://localhost:5000/api/upload-image",
            {
              method: "POST",
              body: formData,
            }
          );

          if (!uploadRes.ok) {
            console.log("Error uploading image");
            return; // Stop execution if there's an error
          }

          const uploadData = await uploadRes.json();

          if (uploadData && !uploadData.error) {
            setImagestring(uploadData.image_path);

            setElapsedTime(0);
            setLoading(true);
            setStartTime(new Date().getTime()); // Set the start time
            setCurrentPage(1);

            // Continue with the second API call
            const processFormData = new FormData();
            processFormData.append("file_name", imageconv.name);

            const processRes = await fetch(
              `http://localhost:5000/api/process_image_similarity/${method}`,
              {
                method: "POST",
                body: processFormData,
              }
            );

            const processData = await processRes.json();

            setLoading(false);
            setStartTime(null);

            if (processRes.ok) {
              setResult(processData.similarity_results);
              if (method === "Texture") setIsCachedTexture(true);
              else if (method === "Color") setIsCachedColor(true);
            } else {
              console.log("Error processing image");
              setResult(null);
            }
          } else {
            console.error("Error uploading image:", uploadData.error);
          }
        } catch (error) {
          console.error("Error handling image:", error);
        }
      }
    }
  };

  useEffect(() => {
    const captureAndSubmit = async () => {
      try {
        await handleCameraCapture();
      } catch (error) {
        console.error("Error in captureAndSubmit:", error);
      }
    };

    if (countdown === 0) {
      captureAndSubmit();
    }
  }, [countdown]);

  useEffect(() => {
    if (imagedataset && imagedataset.length > 0) {
      const countdownInterval = setInterval(() => {
        setCountdown((prevCountdown) => {
          if (prevCountdown === 0) {
            return initialTime;
          } else {
            return Math.max(prevCountdown - 1, 0);
          }
        });
      }, 1000);

      return () => {
        clearInterval(countdownInterval);
      };
    }
  }, [imagedataset, initialTime]);

  const handleSubmitScraping = async () => {
    setShowBackdrop(true);
    try {
      const res = await fetch("http://localhost:5000/api/scrape-website", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({ website_url: websiteUrl }),
      });
      setIsScraping(false);
      setWebsiteUrl("");
      setShowBackdrop(false);

      if (res.ok) {
        const data = await res.json();
        setImagedataset(data.image_paths);

        sethavescrapping(true); // Optional: Log the success message
        // Handle the scraped image paths as needed (data.image_paths)
      } else {
        console.error("Error scraping website:", res.statusText);
      }
    } catch (error) {
      console.error("Error scraping website:", error);
      setIsScraping(false);
      setWebsiteUrl("");
      setShowBackdrop(false);
    }
  };

  /* Pagination Codes */

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
  /* End of Pagination Codes */

  const sendAttachment = async () => {
    try {
      const res = await fetch("http://localhost:5000/api/send-attachment", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          similarity_results: result,
          image_path: imagestring,
        }),
      });

      if (res.ok) {
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "results.pdf";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      } else {
        console.error("Error sending attachment:", res.statusText);
      }
    } catch (error) {
      console.error("Error sending attachment:", error);
    }
  };

  useEffect(() => {
    setBackgroundColor(
      "radial-gradient(circle, #fecccb, #ffd5c8, #ffe0c9, #ffebcc, #fef6d4)"
    );
  }, []);

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

  const handleBackdropClick = () => {
    // Only allow clicking the backdrop if scraping is not in progress
    if (!isScraping) {
      // Add any action you want to perform on backdrop click here
      // For example, displaying an image or any other UI element
      console.log("Backdrop clicked");
    }
  };

  return (
    <div
      className="py-10 mt-5  rounded-lg w-[85%] justify-center border-2 border-[#757376]"
      style={{
        background: backgroundColor,
        paddingLeft: "20px",
        paddingRight: "20px",
      }}
    >
      {showBackdrop && (
        <div
          className={`fixed top-0 left-0 w-full h-full bg-black bg-opacity-50 z-50 ${
            isScraping ? "cursor-not-allowed" : "cursor-pointer"
          }`}
          onClick={handleBackdropClick}
        />
      )}
      <form className="formbg">
        <div className="p-5">
          {imagedataset && imagedataset.length > 0 ? (
            <>
              <p className="font-lemon text-2xl mb-5">
                Current Position (change in {countdown} seconds):
              </p>
              <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                videoConstraints={{
                  width: 480,
                  height: 270,
                  facingMode: "user",
                }}
              />
              <canvas id="canvas" style={{ display: "none" }} />{" "}
            </>
          ) : (
            <p className="font-lemon text-2xl mb-5">
              Please upload your dataset to activate camera!
            </p>
          )}
        </div>
        <div className="grid grid-cols-2 gap-4 mt-10 justify-center items-center">
          <div>
            {imagedataset && imagedataset.length > 0 ? (
              <>
                <label className="font-bakso block mb-4 sm:text-xl md:text-2xl lg:text-4xl">{` ${
                  image
                    ? "Current Photo : "
                    : `Will Capture in ${countdown} Seconds`
                }`}</label>
                <div className="relative object-contain w-[160px] md:w-[240px] lg:w-[320px] xl:w-[480px] h-[90px] md:h-[135px] lg:h-[180px] xl:h-[270px] mb-4">
                  <Image alt="Uploaded Image" src={imageSrc} fill />
                </div>
                <input
                  type="file"
                  className="hidden"
                  ref={inputRef}
                  onChange={handleImageUpload}
                  accept="image/*"
                  required
                  name="fileupload"
                />
                <button
                  type="button"
                  onClick={handlePhotoClick}
                  className="font-bakso border-[2px] border-[#757376] bg-[#FEFBD6] p-2 rounded-full text-[#005B4A] transition-colors duration-200 ease-in-out hover:text-gray-600 hover:shadow-lg"
                >
                  {image ? "Change Your Photo ?" : "Upload Photo"}
                </button>
              </>
            ) : (
              <p className="font-lemon text-2xl mb-5">
                Please upload your dataset to activate camera!
              </p>
            )}
          </div>
          <div className="justify-center">
            <label className="font-bakso block mb-4 sm:text-xl md:text-2xl lg:text-4xl">{`${
              imagedataset
                ? `Dataset : ${imagedataset.length} images `
                : "Upload Your Dataset!"
            }`}</label>
            <div className="relative object-contain w-[160px] md:w-[240px] lg:w-[320px] xl:w-[480px] h-[90px] md:h-[135px] lg:h-[180px] xl:h-[270px] mb-4">
              <Image alt="Uploaded Image" src={imagedatasetSrc} fill />
            </div>
            <div className="flex flex-row items-center justify-center">
              <div
                className={`rounded-lg w-${
                  isScraping ? "[100%]" : "[100%]"
                } justify-center`}
              >
                {isScraping ? (
                  <div className="flex flex-col gap-5 justify-center items-center">
                    <input
                      type="text"
                      placeholder="Input Website URL"
                      value={websiteUrl}
                      onChange={handleWebsiteUrlChange}
                      className="border-[2px] border-[#757376] w-[300px] bg-[#FEFBD6] p-2 rounded-full"
                    />
                    <div className="flex flex-row justify-center items-center gap-10">
                      <button
                        type="button"
                        onClick={handleCancelScraping}
                        className="font-bakso border-[2px] border-[#757376] bg-[#FEFBD6] p-2 rounded-full text-[#005B4A] transition-colors duration-200 ease-in-out hover:text-gray-600 hover:shadow-lg"
                      >
                        Cancel
                      </button>
                      <button
                        type="button"
                        onClick={handleSubmitScraping}
                        className="font-bakso border-[2px] border-[#757376] bg-[#FEFBD6] p-2 rounded-full text-[#005B4A] transition-colors duration-200 ease-in-out hover:text-gray-600 hover:shadow-lg"
                      >
                        Submit
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="flex flex-row gap-5 justify-center">
                    <input
                      type="file"
                      webkitdirectory="true"
                      multiple
                      className="hidden"
                      ref={inputRefFolder}
                      onChange={handleFolderUpload}
                      accept="image/*"
                      name="folderupload"
                    />
                    <button
                      type="button"
                      onClick={handleFolderClick}
                      className="font-bakso border-[2px] border-[#757376] bg-[#FEFBD6] p-2 rounded-full text-[#005B4A] transition-colors duration-200 ease-in-out hover:text-gray-600 hover:shadow-lg"
                    >
                      {`${
                        imagedataset ? "Change Your Dataset?" : "Upload Folder"
                      }`}
                    </button>{" "}
                    <button
                      type="button"
                      onClick={handleScrapeWebsite}
                      className="font-bakso border-[2px] border-[#757376] bg-[#FEFBD6] p-2 rounded-full text-[#005B4A] transition-colors duration-200 ease-in-out hover:text-gray-600 hover:shadow-lg"
                    >
                      Scrape Website
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        <div className="my-4 ">
          <center>
            <div className="items-center">
              <label className="inline-flex items-center ml-3 relative">
                <span
                  className={`text-[#005B4A] font-bakso mr-3 text-lg ${
                    method === "Color" ? "text-[#005B4A]" : "text-gray-400"
                  }`}
                >
                  Color
                </span>
                <input
                  type="checkbox"
                  onChange={handleToggleCheckbox}
                  checked={method === "Texture"}
                  className="hidden"
                />
                <div
                  className={`toggle-switch w-[48px] h-[24px] rounded-full ${
                    method === "Color" ? "bg-[#005B4A]" : "bg-gray-400"
                  }`}
                >
                  <div
                    className={`toggle-switch-handle  -ml-6 w-6 h-6 rounded-full transform transition-transform duration-300 ease-in-out ${
                      method === "Texture"
                        ? "bg-white translate-x-full"
                        : "bg-gray-200 translate-x-0"
                    }`}
                  ></div>
                </div>

                <span
                  className={`ml-3 text-[#005B4A] font-bakso text-lg ${
                    method === "Texture" ? "text-[#005B4A]" : "text-gray-400"
                  }`}
                >
                  Texture
                </span>
              </label>
            </div>
          </center>
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
              <hr className="my-6 border-t-2 border-[#757376]" />
              <h1 className="font-bakso text-xl sm:text-2xl md:text-3xl lg:text-4xl py-10">{`${result?.length} images in ${elapsedTime} seconds`}</h1>

              <div
                id="results-container"
                className="flex flex-wrap justify-center gap-10"
              >
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
              <button
                className={`disabled:opacity-70 disabled:cursor-not-allowed mx-2 px-4 mt-10 py-2 rounded-full border-[2px] border-[#757376] bg-[#FEFBD6] text-[#005B4A] transition-all duration-200 ease-in-out hover:text-gray-600 hover:shadow-lg`}
                disabled={!currentImages}
                onClick={sendAttachment}
                type="button"
              >
                Save Your Results?
              </button>
              <hr className="my-6 border-t-2 border-[#757376]" />
            </div>
          ) : (
            <h1>Tidak ada gambar yang mirip !</h1>
          )
        ) : null}
      </form>
    </div>
  );
};
export default Form;
