import './globals.css';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ backgroundImage: 'url(/background_image.png)', backgroundSize: 'cover', backgroundAttachment: 'fixed' }}>{children}</body>
    </html>
  );
}
