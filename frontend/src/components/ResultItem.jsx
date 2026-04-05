import React from 'react';

const ResultItem = ({ result, onClick }) => {
  return (
    <div
      onClick={() => onClick(result.id)}
      style={{
        border: '1px solid #ddd',
        padding: '15px',
        marginBottom: '10px',
        cursor: 'pointer',
        borderRadius: '8px',
        transition: 'background-color 0.2s'
      }}
      onMouseOver={(e) => (e.currentTarget.style.backgroundColor = '#f9f9f9')}
      onMouseOut={(e) => (e.currentTarget.style.backgroundColor = '#fff')}
    >
      <h3 style={{ margin: '0 0 5px 0', color: '#007bff' }}>{result.title}</h3>
      <p style={{ margin: '0 0 10px 0', fontSize: '14px', color: '#555' }}>{result.snippet}</p>
      <div style={{ fontSize: '12px', color: '#888' }}>
        <strong>Score:</strong> {result.score.toFixed(2)} | <strong>Exp:</strong> {result.explanation}
      </div>
    </div>
  );
};

export default ResultItem;
