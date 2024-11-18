import { useState, FormEvent } from 'react';
import { Search } from 'lucide-react';

interface SearchBarProps {
  onSearch: (query: string) => void;
}

export function SearchBar({ onSearch }: SearchBarProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your search query..."
          className="w-full px-4 py-3 bg-gray-800 rounded-lg pr-12 
                     border border-gray-700 focus:border-blue-500 
                     focus:outline-none focus:ring-2 focus:ring-blue-500/20 
                     transition-all"
        />
        <button
          type="submit"
          className="absolute right-2 top-1/2 -translate-y-1/2 
                     p-2 bg-blue-500 rounded-lg hover:bg-blue-600 
                     transition-colors"
        >
          <Search className="w-4 h-4" />
        </button>
      </div>
    </form>
  );
}