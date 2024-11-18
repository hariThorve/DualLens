export interface SearchResult {
    title: string;
    url: string;
    description?: string;
    content?: string;
    timestamp: string;
  }
  
  export interface LLMResponse {
    gemini: string;
    groq: string;
  }
  
  export interface SearchResponse {
    query: string;
    results: SearchResult[];
    total_results: number;
    search_time: number;
    llm_responses?: LLMResponse;
  }