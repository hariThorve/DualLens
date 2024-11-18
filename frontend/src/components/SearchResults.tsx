import { SearchResponse } from '../types/search';
import { Bot, Sparkles, Globe, Copy, Check } from 'lucide-react';
import { useState } from 'react';

interface SearchResultsProps {
  response: SearchResponse;
}

export function SearchResults({ response }: SearchResultsProps) {
  const [copiedStates, setCopiedStates] = useState<{ [key: string]: boolean }>({});

  // Function to detect if text contains code
  const containsCode = (text: string) => {
    return text.includes('```') || text.includes('function') || text.includes('class') || 
           text.includes('const') || text.includes('let') || text.includes('var');
  };

  // Function to extract code blocks from text
  const extractCodeBlocks = (text: string) => {
    const codeBlockRegex = /```[\s\S]*?```/g;
    const matches = text.match(codeBlockRegex);
    if (!matches) return [];
    return matches.map(block => block.replace(/```/g, '').trim());
  };

  // Function to clean text of URLs and citations
  const cleanAnalysisText = (text: string) => {
    // Remove URLs
    const withoutUrls = text.replace(/(?:https?|ftp):\/\/[\n\S]+/g, '');
    // Remove citations like (Source: ...)
    const withoutCitations = withoutUrls.replace(/\(Source:.*?\)/g, '');
    // Remove references to Wikipedia, GeeksforGeeks etc.
    const withoutReferences = withoutCitations.replace(/\([^)]*(?:Wikipedia|GeeksforGeeks|wikitia|Tatler)[^)]*\)/g, '');
    // Remove trailing periods and spaces
    return withoutReferences.trim().replace(/\.+$/, '');
  };

  // Function to handle copy
  const handleCopy = async (text: string, id: string) => {
    await navigator.clipboard.writeText(text);
    setCopiedStates({ ...copiedStates, [id]: true });
    setTimeout(() => {
      setCopiedStates({ ...copiedStates, [id]: false });
    }, 2000);
  };

  return (
    <div className="w-full max-w-4xl mx-auto mt-8 space-y-8">
      {/* LLM Analysis Section */}
      {response.llm_responses && (
        <div className="bg-gradient-to-br from-gray-900 to-gray-800 p-8 rounded-2xl shadow-xl border border-gray-700">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
            <Bot className="w-6 h-6 text-blue-400" />
            AI Analysis
          </h2>
          <div className="space-y-6">
            {/* Gemini Response */}
            <div className="bg-gray-800/50 backdrop-blur p-6 rounded-xl border border-blue-500/20 hover:border-blue-500/40 transition-all">
              <div className="flex items-center gap-2 mb-4">
                <Sparkles className="w-5 h-5 text-blue-400" />
                <h3 className="font-semibold text-lg text-blue-400">Gemini Analysis</h3>
              </div>
              <div className="prose prose-invert max-w-none">
                {containsCode(response.llm_responses.gemini) ? (
                  <div className="space-y-4">
                    <p className="text-gray-300 leading-relaxed">
                      {cleanAnalysisText(response.llm_responses.gemini.split('```')[0])}
                    </p>
                    {extractCodeBlocks(response.llm_responses.gemini).map((code, index) => (
                      <div key={index} className="relative group">
                        <div className="absolute right-2 top-2 z-10">
                          <button
                            onClick={() => handleCopy(code, `gemini-${index}`)}
                            className="p-2 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors"
                            title="Copy to clipboard"
                          >
                            {copiedStates[`gemini-${index}`] ? (
                              <Check className="w-4 h-4 text-green-400" />
                            ) : (
                              <Copy className="w-4 h-4 text-gray-400" />
                            )}
                          </button>
                        </div>
                        <pre className="bg-gray-900/50 p-4 rounded-lg overflow-x-auto">
                          <code className="text-sm text-gray-300">{code}</code>
                        </pre>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-300 leading-relaxed">
                    {cleanAnalysisText(response.llm_responses.gemini)}
                  </p>
                )}
              </div>
            </div>

            {/* Groq Response */}
            <div className="bg-gray-800/50 backdrop-blur p-6 rounded-xl border border-purple-500/20 hover:border-purple-500/40 transition-all">
              <div className="flex items-center gap-2 mb-4">
                <Sparkles className="w-5 h-5 text-purple-400" />
                <h3 className="font-semibold text-lg text-purple-400">Groq Analysis</h3>
              </div>
              <div className="prose prose-invert max-w-none">
                {containsCode(response.llm_responses.groq) ? (
                  <div className="space-y-4">
                    <p className="text-gray-300 leading-relaxed">
                      {cleanAnalysisText(response.llm_responses.groq.split('```')[0])}
                    </p>
                    {extractCodeBlocks(response.llm_responses.groq).map((code, index) => (
                      <div key={index} className="relative group">
                        <div className="absolute right-2 top-2 z-10">
                          <button
                            onClick={() => handleCopy(code, `groq-${index}`)}
                            className="p-2 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors"
                            title="Copy to clipboard"
                          >
                            {copiedStates[`groq-${index}`] ? (
                              <Check className="w-4 h-4 text-green-400" />
                            ) : (
                              <Copy className="w-4 h-4 text-gray-400" />
                            )}
                          </button>
                        </div>
                        <pre className="bg-gray-900/50 p-4 rounded-lg overflow-x-auto">
                          <code className="text-sm text-gray-300">{code}</code>
                        </pre>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-300 leading-relaxed">
                    {cleanAnalysisText(response.llm_responses.groq)}
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Search Results Section */}
      <div className="space-y-4">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
          <Globe className="w-6 h-6 text-blue-400" />
          Search Results
          <span className="text-sm text-gray-400 font-normal">
            ({response.total_results} results in {response.search_time.toFixed(2)}s)
          </span>
        </h2>
        
        {response.results.map((result, index) => (
          <div 
            key={index} 
            className="bg-gray-800/50 backdrop-blur p-6 rounded-xl border border-gray-700 hover:border-gray-600 transition-all"
          >
            <h3 className="font-bold text-lg">
              <a 
                href={result.url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-blue-400 hover:text-blue-300 transition-colors"
              >
                {result.title}
              </a>
            </h3>
            {result.description && (
              <p className="text-gray-300 mt-3 leading-relaxed">
                {result.description}
              </p>
            )}
            <div className="flex items-center mt-4 text-sm text-gray-400">
              <Globe className="w-4 h-4 mr-2 text-gray-500" />
              <a 
                href={result.url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="hover:text-gray-300 transition-colors truncate"
              >
                {result.url}
              </a>
            </div>
          </div>
        ))}
      </div>

      {/* No Results Message */}
      {response.results.length === 0 && (
        <div className="text-center py-8">
          <p className="text-gray-400">No results found for your search.</p>
        </div>
      )}
    </div>
  );
}