import React from 'react';
import { Loader2 } from 'lucide-react';

export function LoadingState() {
  return (
    <div className="mt-8 flex flex-col items-center">
      <Loader2 className="w-8 h-8 text-blue-400 animate-spin" />
      <p className="mt-4 text-gray-400">Searching for insights...</p>
    </div>
  );
}