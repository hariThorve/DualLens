import React from 'react';

export function Footer() {
  return (
    <footer className="absolute bottom-0 w-full p-4 text-center text-gray-500 text-sm">
      <p>© {new Date().getFullYear()} AI Search Engine. All rights reserved.</p>
    </footer>
  );
}