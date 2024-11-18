import React from 'react';

export function Features() {
  return (
    <div className="mt-12 grid grid-cols-1 md:grid-cols-2 gap-4 text-center text-sm text-gray-400">
      <div className="p-4 bg-gray-800/30 rounded-xl hover:bg-gray-800/40 transition-colors">
        <h3 className="font-semibold text-white mb-2">Advanced AI</h3>
        <p>Powered by cutting-edge machine learning algorithms</p>
      </div>
      <div className="p-4 bg-gray-800/30 rounded-xl hover:bg-gray-800/40 transition-colors">
        <h3 className="font-semibold text-white mb-2">Real-time Results</h3>
        <p>Get instant answers to your questions</p>
      </div>
    </div>
  );
}