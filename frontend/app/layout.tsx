import type { Metadata } from 'next';

import './globals.css';

export const metadata: Metadata = {
  title: 'PlantGuard AI',
  description: 'Modern plant disease detection dashboard powered by FastAPI and PyTorch.',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-background font-sans text-foreground antialiased">{children}</body>
    </html>
  );
}
