import type { Metadata } from "next";
import { Bricolage_Grotesque } from "next/font/google";
import localFont from "next/font/local";
import "./globals.css";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  display: "swap",
});

const bricolage = Bricolage_Grotesque({
  subsets: ["latin"],
  variable: "--font-bricolage",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Brócoli — Come saludable con lo que tienes en casa",
  description:
    "Comidas saludables y variadas con ingredientes cotidianos, opciones hondureñas y compras dentro de tu presupuesto.",
  icons: {
    icon: "/favicon.ico",
    apple: "/brocoli-icon.png",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className={`${geistSans.variable} ${bricolage.variable}`}>
        {children}
      </body>
    </html>
  );
}
