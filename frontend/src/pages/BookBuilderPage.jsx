import React, { useState, useEffect } from 'react';

const BookBuilderPage = () => {
  const [bookData, setBookData] = useState({
    title: '',
    author: '',
    genre: 'non_fiction',
    topic: '',
    target_audience: '',
    word_count_goal: 50000,
    tone: 'professional',
    writing_style: 'narrative',
    key_themes: [],
    source_materials: []
  });

  const [currentBook, setCurrentBook] = useState(null);
  const [chapters, setChapters] = useState([]);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('');
  const [exportFormat, setExportFormat] = useState('txt');
  const [books, setBooks] = useState([]);

  const genres = [
    { value: 'fiction', label: 'Fiction' },
    { value: 'non_fiction', label: 'Non-Fiction' },
    { value: 'biography', label: 'Biography' },
    { value: 'self_help', label: 'Self Help' },
    { value: 'business', label: 'Business' },
    { value: 'technical', label: 'Technical' },
    { value: 'memoir', label: 'Memoir' },
    { value: 'poetry', label: 'Poetry' }
  ];

  const exportFormats = [
    { value: 'txt', label: 'Plain Text (.txt)' },
    { value: 'html', label: 'HTML (.html)' },
    { value: 'json', label: 'JSON (.json)' },
    { value: 'epub', label: 'EPUB (.epub)' },
    { value: 'm4b', label: 'M4B (.m4b)' }
  ];

  useEffect(() => {
    loadBooks();
  }, []);

  const loadBooks = async () => {
    try {
      const response = await fetch('/api/book-builder/list-books');
      if (response.ok) {
        const data = await response.json();
        setBooks(data.books);
      }
    } catch (error) {
      console.error('Failed to load books:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setBookData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleArrayInputChange = (field, value) => {
    const items = value.split(',').map(item => item.trim()).filter(item => item);
    setBookData(prev => ({
      ...prev,
      [field]: items
    }));
  };

  const createOutline = async () => {
    setLoading(true);
    setStatus('Creating book outline...');

    try {
      const response = await fetch('/api/book-builder/create-outline', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(bookData),
      });

      if (!response.ok) throw new Error('Failed to create outline');

      const result = await response.json();
      setCurrentBook(result);
      setStatus('Outline created successfully!');
    } catch (error) {
      console.error('Failed to create outline:', error);
      setStatus('Failed to create outline');
    } finally {
      setLoading(false);
    }
  };

  const generateChapter = async (chapterNumber) => {
    if (!currentBook) return;

    setLoading(true);
    setStatus(`Generating chapter ${chapterNumber}...`);

    try {
      const response = await fetch(`/api/book-builder/generate-chapter/${currentBook.book_id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ chapter_number: chapterNumber }),
      });

      if (!response.ok) throw new Error('Failed to generate chapter');

      const result = await response.json();
      setChapters(prev => [...prev.filter(c => c.number !== chapterNumber), result.chapter]);
      setStatus(`Chapter ${chapterNumber} generated successfully!`);
    } catch (error) {
      console.error('Failed to generate chapter:', error);
      setStatus(`Failed to generate chapter ${chapterNumber}`);
    } finally {
      setLoading(false);
    }
  };

  const generateAllChapters = async () => {
    if (!currentBook) return;

    setLoading(true);
    setStatus('Generating all chapters...');

    try {
      const response = await fetch(`/api/book-builder/generate-all-chapters/${currentBook.book_id}`, {
        method: 'POST',
      });

      if (!response.ok) throw new Error('Failed to start chapter generation');

      // Poll for status
      const pollStatus = async () => {
        try {
          const statusResponse = await fetch(`/api/book-builder/status/${currentBook.book_id}`);
          if (statusResponse.ok) {
            const statusData = await statusResponse.json();
            if (statusData.chapters_generated === statusData.total_chapters) {
              setStatus('All chapters generated successfully!');
              setLoading(false);
              // Reload chapters
              loadBookChapters(currentBook.book_id);
            } else {
              setStatus(`Generated ${statusData.chapters_generated}/${statusData.total_chapters} chapters...`);
              setTimeout(pollStatus, 2000);
            }
          }
        } catch (error) {
          console.error('Failed to check status:', error);
        }
      };

      setTimeout(pollStatus, 2000);
    } catch (error) {
      console.error('Failed to generate chapters:', error);
      setStatus('Failed to generate chapters');
      setLoading(false);
    }
  };

  const compileBook = async () => {
    if (!currentBook) return;

    setLoading(true);
    setStatus('Compiling book...');

    try {
      const response = await fetch(`/api/book-builder/compile-book/${currentBook.book_id}`, {
        method: 'POST',
      });

      if (!response.ok) throw new Error('Failed to compile book');

      const result = await response.json();
      setCurrentBook(prev => ({ ...prev, compiled: result.compiled_book }));
      setStatus('Book compiled successfully!');
    } catch (error) {
      console.error('Failed to compile book:', error);
      setStatus('Failed to compile book');
    } finally {
      setLoading(false);
    }
  };

  const exportBook = async () => {
    if (!currentBook) return;

    setLoading(true);
    setStatus('Exporting book...');

    try {
      const response = await fetch(`/api/book-builder/export-book/${currentBook.book_id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          format: exportFormat,
          output_filename: `${bookData.title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.${exportFormat}`
        }),
      });

      if (!response.ok) throw new Error('Failed to export book');

      const result = await response.json();

      // Trigger download
      const downloadResponse = await fetch(result.download_url);
      if (downloadResponse.ok) {
        const blob = await downloadResponse.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = result.export.file_path.split('/').pop();
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }

      setStatus('Book exported successfully!');
    } catch (error) {
      console.error('Failed to export book:', error);
      setStatus('Failed to export book');
    } finally {
      setLoading(false);
    }
  };

  const loadBookChapters = async (bookId) => {
    // This would need a new endpoint to get chapters
    // For now, we'll work with the chapters we have
  };

  const resetForm = () => {
    setBookData({
      title: '',
      author: '',
      genre: 'non_fiction',
      topic: '',
      target_audience: '',
      word_count_goal: 50000,
      tone: 'professional',
      writing_style: 'narrative',
      key_themes: [],
      source_materials: []
    });
    setCurrentBook(null);
    setChapters([]);
    setStatus('');
  };

  return (
    <div className="container mx-auto p-4 max-w-4xl">
      <h1 className="text-3xl font-bold mb-8 text-center">GOAT Book Builder</h1>
      <p className="text-center text-gray-600 mb-8">Create complete books from outline to export</p>

      {/* Status Message */}
      {status && (
        <div className={`mb-6 p-4 rounded-lg ${status.includes('Failed') ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'}`}>
          {status}
        </div>
      )}

      {/* Book Creation Form */}
      {!currentBook && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Create New Book</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium mb-1">Title</label>
              <input
                type="text"
                name="title"
                value={bookData.title}
                onChange={handleInputChange}
                className="w-full p-2 border rounded"
                placeholder="Enter book title"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Author</label>
              <input
                type="text"
                name="author"
                value={bookData.author}
                onChange={handleInputChange}
                className="w-full p-2 border rounded"
                placeholder="Enter author name"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Genre</label>
              <select
                name="genre"
                value={bookData.genre}
                onChange={handleInputChange}
                className="w-full p-2 border rounded"
              >
                {genres.map(genre => (
                  <option key={genre.value} value={genre.value}>{genre.label}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Topic</label>
              <input
                type="text"
                name="topic"
                value={bookData.topic}
                onChange={handleInputChange}
                className="w-full p-2 border rounded"
                placeholder="Main topic or subject"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Target Audience</label>
              <input
                type="text"
                name="target_audience"
                value={bookData.target_audience}
                onChange={handleInputChange}
                className="w-full p-2 border rounded"
                placeholder="Who is this book for?"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Word Count Goal</label>
              <input
                type="number"
                name="word_count_goal"
                value={bookData.word_count_goal}
                onChange={handleInputChange}
                className="w-full p-2 border rounded"
                min="10000"
                max="200000"
              />
            </div>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-1">Key Themes (comma-separated)</label>
            <input
              type="text"
              value={bookData.key_themes.join(', ')}
              onChange={(e) => handleArrayInputChange('key_themes', e.target.value)}
              className="w-full p-2 border rounded"
              placeholder="leadership, innovation, growth"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-1">Source Materials (comma-separated)</label>
            <input
              type="text"
              value={bookData.source_materials.join(', ')}
              onChange={(e) => handleArrayInputChange('source_materials', e.target.value)}
              className="w-full p-2 border rounded"
              placeholder="books, articles, research, experience"
            />
          </div>

          <button
            onClick={createOutline}
            disabled={loading || !bookData.title || !bookData.author || !bookData.topic}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 disabled:bg-gray-400"
          >
            {loading ? 'Creating Outline...' : 'Create Book Outline'}
          </button>
        </div>
      )}

      {/* Book Progress */}
      {currentBook && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">{currentBook.outline.title}</h2>
            <button
              onClick={resetForm}
              className="text-gray-600 hover:text-gray-800"
            >
              New Book
            </button>
          </div>

          <div className="mb-6">
            <div className="flex justify-between text-sm text-gray-600 mb-2">
              <span>Progress</span>
              <span>{chapters.length}/{currentBook.outline.chapters.length} chapters</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full"
                style={{ width: `${(chapters.length / currentBook.outline.chapters.length) * 100}%` }}
              ></div>
            </div>
          </div>

          {/* Outline Display */}
          <div className="mb-6">
            <h3 className="font-semibold mb-2">Book Outline</h3>
            <div className="bg-gray-50 p-4 rounded">
              <p className="mb-2"><strong>Premise:</strong> {currentBook.outline.premise}</p>
              <p className="mb-2"><strong>Estimated Chapters:</strong> {currentBook.outline.estimated_chapters}</p>
              <p className="mb-2"><strong>Estimated Words:</strong> {currentBook.outline.estimated_word_count.toLocaleString()}</p>
              <div className="mt-4">
                <h4 className="font-medium mb-2">Chapter Structure:</h4>
                <ul className="list-disc list-inside space-y-1">
                  {currentBook.outline.chapters.map((chapter, index) => (
                    <li key={index} className="text-sm">
                      {chapter.title} ({chapter.estimated_words} words)
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          {/* Chapter Generation */}
          <div className="mb-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-semibold">Chapters</h3>
              {chapters.length < currentBook.outline.chapters.length && (
                <button
                  onClick={generateAllChapters}
                  disabled={loading}
                  className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:bg-gray-400"
                >
                  Generate All Chapters
                </button>
              )}
            </div>

            <div className="space-y-2">
              {currentBook.outline.chapters.map((chapter, index) => {
                const generatedChapter = chapters.find(c => c.number === index + 1);
                return (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                    <div>
                      <span className="font-medium">Chapter {index + 1}: {chapter.title}</span>
                      {generatedChapter && (
                        <span className="ml-2 text-sm text-green-600">✓ Generated ({generatedChapter.word_count} words)</span>
                      )}
                    </div>
                    {!generatedChapter && (
                      <button
                        onClick={() => generateChapter(index + 1)}
                        disabled={loading}
                        className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 disabled:bg-gray-400"
                      >
                        Generate
                      </button>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Compile & Export */}
          {chapters.length === currentBook.outline.chapters.length && (
            <div className="border-t pt-6">
              {!currentBook.compiled ? (
                <div className="text-center">
                  <button
                    onClick={compileBook}
                    disabled={loading}
                    className="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 disabled:bg-gray-400"
                  >
                    Compile Book
                  </button>
                </div>
              ) : (
                <div className="text-center">
                  <div className="mb-4">
                    <p className="text-green-600 font-medium">✓ Book compiled successfully!</p>
                    <p className="text-sm text-gray-600">
                      Total words: {currentBook.compiled.total_word_count.toLocaleString()}
                    </p>
                  </div>

                  <div className="mb-4">
                    <label className="block text-sm font-medium mb-2">Export Format</label>
                    <select
                      value={exportFormat}
                      onChange={(e) => setExportFormat(e.target.value)}
                      className="p-2 border rounded mr-2"
                    >
                      {exportFormats.map(format => (
                        <option key={format.value} value={format.value}>{format.label}</option>
                      ))}
                    </select>
                  </div>

                  <button
                    onClick={exportBook}
                    disabled={loading}
                    className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 disabled:bg-gray-400"
                  >
                    Export Book
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Previous Books */}
      {books.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Previous Books</h2>
          <div className="space-y-2">
            {books.map(book => (
              <div key={book.book_id} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <div>
                  <span className="font-medium">{book.title}</span>
                  <span className="ml-2 text-sm text-gray-600">by {book.author}</span>
                  <span className="ml-2 text-sm text-gray-600">({book.genre})</span>
                </div>
                <div className="text-sm text-gray-600">
                  {book.chapters_generated}/{book.total_chapters} chapters
                  {book.compiled && <span className="ml-2 text-green-600">✓ Compiled</span>}
                  {book.exports_count > 0 && <span className="ml-2 text-blue-600">✓ Exported</span>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default BookBuilderPage;