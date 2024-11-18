// import React from 'react';
// import { History } from 'lucide-react';

interface SearchSuggestionsProps {
  suggestions: string[];
  setQuery: (query: string) => void;
  show: boolean;
  query: string;
  onSuggestionClick: (suggestion: string) => void;
}

export function SearchSuggestions({ suggestions, show, query, onSuggestionClick }: SearchSuggestionsProps) {
  if (!show) return null;

  const filteredSuggestions = suggestions.filter(suggestion =>
    suggestion.toLowerCase().includes(query.toLowerCase())
  );

  if (filteredSuggestions.length === 0) return null;

  return (
    <div className="absolute w-full bg-gray-800 border border-gray-700 rounded-lg mt-2 shadow-xl z-10">
      {filteredSuggestions.map((suggestion, index) => (
        <button
          key={index}
          className="w-full px-4 py-2 text-left hover:bg-gray-700 transition-colors"
          onClick={() => onSuggestionClick(suggestion)}
        >
          {suggestion}
        </button>
      ))}
    </div>
  );
}