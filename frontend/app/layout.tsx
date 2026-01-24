import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
    title: "Literature Survey System",
    description: "Citation-grounded AI-assisted literature survey generation for engineering research",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    );
}
