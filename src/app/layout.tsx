import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Navbar from "./Components/Navbar/navbar";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Navbar />
        <div className="pb-20 pt-36">{children}</div>
      </body>
    </html>
  );
}
