import React, { useEffect, useRef, useState } from "react";


const CameraCapture = ({ setImage, setImagestring }) => {
  
  const [isCapturing, setIsCapturing] = useState(true);
  const handleToggleCapture = () => {
    setIsCapturing((prevIsCapturing) => !prevIsCapturing);
  };
  const handleCameraCapture = async () => {
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

      // Upload the captured image to the server
      const formData = new FormData();
      formData.append("image", image);

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

  useEffect(() => {
    const captureInterval = setInterval(() => {
      handleCameraCapture();
    }, 20000);

    return () => {
      clearInterval(captureInterval);
    };
  }, []); // Run only once on component mount

  return (
    <div>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        videoConstraints={{ width: 1280, height: 720, facingMode: "user" }}
      />
      <canvas id="canvas" style={{ display: "none" }} />

      <button
        type="button"
        onClick={handleToggleCapture}
        className="font-bakso border-[2px] border-[#757376] bg-[#FEFBD6] p-2 rounded-full text-[#005B4A] transition-colors duration-200 ease-in-out hover:text-gray-600 hover:shadow-lg mt-2"
      >
        {isCapturing ? "Stop Camera" : "Start Camera"}
      </button>
    </div>
  );
};

export default CameraCapture;
