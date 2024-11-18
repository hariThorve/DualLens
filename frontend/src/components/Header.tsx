import React from 'react';
import { Command, Settings } from 'lucide-react';

export function Header() {
  return (
    <header className="p-4 flex justify-between items-center">
      <div className="flex items-center space-x-2">
        <Command className="w-8 h-8 text-blue-400" />
        <span className="text-xl font-bold">AI Search</span>
      </div>
      <Settings className="w-6 h-6 text-gray-400 hover:text-white cursor-pointer transition-colors" />
    </header>
  );
}