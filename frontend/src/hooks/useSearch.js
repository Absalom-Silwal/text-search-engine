import { useState } from 'react';
import client from '../api/client';

export const useSearch = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [query, setQuery] = useState('');

  const search = async (q) => {
    if (!q) return;
    setLoading(true);
    setQuery(q);
    try {
      const response = await client.get(`/search?q=${q}`);
      setResults(response.data);
      setError(null);
    } catch (err) {
      setError('Search failed');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const sendFeedback = async (docId) => {
    try {
      await client.post('/feedback', {
        query: query,
        doc_id: docId
      });
      // Optionally re-search to show updated ranking immediately
      await search(query);
    } catch (err) {
      console.error('Feedback failed', err);
    }
  };

  return { results, loading, error, search, sendFeedback };
};
