import React from 'react';
import SearchBar from './components/SearchBar';
import ResultsList from './components/ResultsList';
import { useSearch } from './hooks/useSearch';

function App() {
  const { results, loading, error, search, sendFeedback } = useSearch();

  return (
    <div style={{ padding: '40px', fontFamily: 'sans-serif' }}>
      <h1>🔍 Feedback Search Engine</h1>
      <p style={{ color: '#666', marginBottom: '30px' }}>
        Ranking improves as you click on results! (BM25 + Click Boost)
      </p>
      
      <SearchBar onSearch={search} />
      
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      
      {!loading && !error && (
        <ResultsList results={results} onResultClick={sendFeedback} />
      )}
    </div>
  );
}

export default App;
