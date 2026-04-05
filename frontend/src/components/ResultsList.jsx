import React from 'react';
import ResultItem from './ResultItem';

const ResultsList = ({ results, onResultClick }) => {
  if (results.length === 0) return <p>No results found.</p>;

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
      {results.map((result) => (
        <ResultItem key={result.id} result={result} onClick={onResultClick} />
      ))}
    </div>
  );
};

export default ResultsList;
