import { useState } from 'react';
import { SearchBar } from './components/SearchBar';
import { SearchResults } from './components/SearchResults';
import { SearchResponse } from './types/search';
import { LoadingState } from './components/LoadingState';

function App() {
  const [searchResponse, setSearchResponse] = useState<SearchResponse | null>(null);
  const [isSearching, setIsSearching] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (searchQuery: string) => {
    if (!searchQuery.trim()) return;
    
    setIsSearching(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: searchQuery,
          max_results: 10,
        }),
      });

      if (!response.ok) {
        throw new Error('Search failed. Please try again.');
      }

      const data = await response.json();
      setSearchResponse(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
      setSearchResponse(null);
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-4">
      <div className="max-w-4xl mx-auto text-center mb-8">
        <h1 className="text-4xl font-bold mb-2">
          DualLens ✨
        </h1>
        <p className="text-gray-400">
          Discover insights with advanced AI technology
        </p>
      </div>

      <div className="max-w-4xl mx-auto">
        <SearchBar onSearch={handleSearch} />

        {error && (
          <div className="text-red-400 text-center mt-4">
            {error}
          </div>
        )}

        {isSearching && (
          <div className="flex justify-center mt-8">
            <LoadingState />
          </div>
        )}

        {searchResponse && !isSearching && (
          <SearchResults response={searchResponse} />
        )}
      </div>
    </div>
  );
}

export default App;