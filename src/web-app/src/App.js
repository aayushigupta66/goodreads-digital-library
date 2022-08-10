import './App.css';
import BookTable from './BookTable';
import AuthorTable from './AuthorTable';
import RequestForm from './RequestForm';
import RowChart from './Visualization'
import React, { useState, useEffect } from 'react';
import * as d3 from "d3";

/**
 * Main app component that holds all divs and components.
 * @returns {JSX.Element} App component with headers, input forms, and API responses.
 * @constructor NA
 */
function App() {

  /**
   * State variables to keep track of different inputs and outputs
   */

  const [failMessage, setFailMessage] = useState('')
  const [successMessage, setSuccessMessage] = useState('')

  const [getBookResponse, setGetBookResponse] = useState([]);
  const [getBookStatus, setGetBookStatus] = useState('')
  const [getBookId, setGetBookId] = useState('')

  const [getAuthorResponse, setGetAuthorResponse] = useState([]);
  const [getAuthorStatus, setGetAuthorStatus] = useState('')
  const [getAuthorId, setGetAuthorId] = useState('')

  const [getSearchResponse, setGetSearchResponse] = useState([]);
  const [getSearchStatus, setGetSearchStatus] = useState('')
  const [getSearchQuery, setGetSearchQuery] = useState('')

  const [putBookResponse, setPutBookResponse] = useState([])
  const [putBookStatus, setPutBookStatus] = useState('')
  const [putBookDetails, setPutBookDetails] = useState('')

  const [putAuthorResponse, setPutAuthorResponse] = useState([])
  const [putAuthorStatus, setPutAuthorStatus] = useState('')
  const [putAuthorDetails, setPutAuthorDetails] = useState('')

  const [postStatus, setPostStatus] = useState('')
  const [postBookJson, setPostBookJson] = useState('')
  const [postBooksJson, setPostBooksJson] = useState('')
  const [postAuthorJson, setPostAuthorJson] = useState('')
  const [postAuthorsJson, setPostAuthorsJson] = useState('')

  const [deleteStatus, setDeleteStatus] = useState('')
  const [deleteBookId, setDeleteBookId] = useState('')
  const [deleteAuthorId, setDeleteAuthorId] = useState('')

  const [visResponse, setVisResponse] = useState([]);
  const [visStatus, setVisStatus] = useState('')
  const [visDetails, setVisDetails] = useState({k: 0, type: ''})

  /**
   * Resets all status variables to ensure that the responses don't overlap/concatenate.
   */
  const resetStatus = () => {
    setGetBookStatus('')
    setGetAuthorStatus('')
    setGetSearchStatus('')
    setPutBookStatus('')
    setPutAuthorStatus('')
    setPostStatus('')
    setDeleteStatus('')
    setVisStatus('')
  }

  /**
   * Renders GET book component.
   * @returns {JSX.Element} Success, fail, or empty component based on getBookStatus.
   */
  const renderBook = () => {
    switch (getBookStatus) {
      case 'success':
        return <BookTable data={getBookResponse}/>;
      case 'fail':
        return <span>{failMessage}</span>
      default:
        return <></>
    }
  }

  /**
   * Function that sets the book id from request form.
   * @param id - book id
   */
  const getBook = id => {
    // reset everything else
    resetStatus()

    // set id
    setGetBookId(id)
  }

  /**
   * Renders GET author component.
   * @returns {JSX.Element} Success, fail, or empty component based on getAuthorStatus.
   */
  const renderAuthor = () => {
    switch (getAuthorStatus) {
      case 'success':
        return <AuthorTable data={getAuthorResponse}/>;
      case 'fail':
        return <span>{failMessage}</span>
      default:
        return <></>
    }
  }

  /**
   * Function that sets the author id from request form.
   * @param id - author id
   */
  const getAuthor = id => {
    // reset everything else
    resetStatus()

    // set id
    setGetAuthorId(id)
  }

  /**
   * Renders GET search component.
   * @returns {JSX.Element} Success, fail, or empty component based on getSearchStatus.
   */
  const renderSearch = () => {
    switch (getSearchStatus) {
      case 'success':
        return <BookTable data={getSearchResponse}/>;
      case 'fail':
        return <span>{failMessage}</span>
      default:
        return <></>
    }
  }

  /**
   * Function that sets the search query from request form.
   * @param query - search query
   */
  const getSearch = query => {
    // reset everything else
    resetStatus()

    // set query
    setGetSearchQuery(query)
  }

  /**
   * Renders PUT book component.
   * @returns {JSX.Element} Success, fail, or empty component based on putBookStatus.
   */
  const renderPutBook = () => {
    switch (putBookStatus) {
      case 'success':
        return <BookTable data={putBookResponse}/>;
      case 'fail':
        return <span>{failMessage}</span>
      default:
        return <></>
    }
  }

  /**
   * Function that sets the put book details needed from request form.
   * @param info - details for put book
   */
  const putBook = info => {
    // reset everything else
    resetStatus()

    // set details
    setPutBookDetails(info)
  }

  /**
   * Renders PUT author component.
   * @returns {JSX.Element} Success, fail, or empty component based on putAuthorStatus.
   */
  const renderPutAuthor = () => {
    switch (putAuthorStatus) {
      case 'success':
        return <AuthorTable data={putAuthorResponse}/>;
      case 'fail':
        return <span>{failMessage}</span>
      default:
        return <></>
    }
  }

  /**
   * Function that sets the put book details needed from request form.
   * @param info - details for put book
   */
  const putAuthor = info => {
    // reset everything else
    resetStatus()

    // set details
    setPutAuthorDetails(info)
  }

  /**
   * Renders POST book, books, author, and author component.
   * @returns {JSX.Element} Success, fail, or empty component based on postStatus.
   */
  const renderPost = () => {
    switch (postStatus) {
      case 'success':
        return <span>{successMessage}</span>
      case 'fail':
        return <span>{failMessage}</span>
      default:
        return <></>
    }
  }

  /**
   * Function that sets the post book details needed from request form.
   * @param json - json input
   */
  const postBook = json => {
    // reset everything else
    resetStatus()

    // set json
    setPostBookJson(json)
  }

  /**
   * Function that sets the post books details needed from request form.
   * @param json - json input
   */
  const postBooks = json => {
    // reset everything else
    resetStatus()

    // set json
    setPostBooksJson(json)
  }

  /**
   * Function that sets the post author details needed from request form.
   * @param json - json input
   */
  const postAuthor = json => {
    // reset everything else
    resetStatus()

    // set json
    setPostAuthorJson(json)
  }

  /**
   * Function that sets the post authors details needed from request form.
   * @param json - json input
   */
  const postAuthors = json => {
    // reset everything else
    resetStatus()

    // set json
    setPostAuthorsJson(json)
  }

  /**
   * Renders DELETE book and author component.
   * @returns {JSX.Element} Success, fail, or empty component based on deleteStatus.
   */
  const renderDelete = () => {
    switch (deleteStatus) {
      case 'success':
        return <span>{successMessage}</span>
      case 'fail':
        return <span>{failMessage}</span>
      default:
        return <></>
    }
  }

  /**
   * Function that sets the delete book details needed from request form.
   * @param id - book id
   */
  const deleteBook = id => {
    // reset everything else
    resetStatus()

    // set id
    setDeleteBookId(id)
  }

  /**
   * Function that sets the delete author details needed from request form.
   * @param id - author id
   */
  const deleteAuthor = id => {
    // reset everything else
    resetStatus()

    // set id
    setDeleteAuthorId(id)
  }

  /**
   * Renders top k book and author visualization components.
   * @returns {JSX.Element} Success, fail, or empty component based on visStatus.
   */
  const renderVis = () => {
    switch (visStatus) {
      case 'success':
        return <RowChart type={visDetails.type} data={visResponse}/>
      case 'fail':
        return <span>{failMessage}</span>
      default:
        return <></>
    }
  }

  /**
   * Function that sets the visualization details needed from request form.
   * @param info - visualization details
   */
  const getVis = info => {
    // reset everything else
    resetStatus()

    // set visualization details
    setVisDetails(info)
  }


  /**
   * CRUD OPERATIONS
   * The following useEffect functions make fetch requests based on the given parameters retrieved from
   * the request form and update status and responses accordingly.
   */

  useEffect(() => {
    if (getBookId === '') return

    var url = '/api/book?id=' + getBookId
    fetch(url).then(res => res.json()).then(data => {
      if ('error' in data) {
        setFailMessage(data['error']);
        setGetBookStatus('fail');
      } else {
        for (var i = 0; i < data.length; i++) {
          data[i] = JSON.parse(data[i]);
        }
        setGetBookResponse(data);
        setGetBookStatus('success');
      }
    });
  }, [getBookId]);

  useEffect(() => {
    if (getAuthorId === '') return

    var url = '/api/author?id=' + getAuthorId
    fetch(url).then(res => res.json()).then(data => {
      if ('error' in data) {
        setFailMessage(data['error']);
        setGetAuthorStatus('fail');
      } else {
        for (var i = 0; i < data.length; i++) {
          data[i] = JSON.parse(data[i]);
        }
        setGetAuthorResponse(data);
        setGetAuthorStatus('success');
      }
    });
  }, [getAuthorId]);

  useEffect(() => {
    if (getSearchQuery === '') return

    var url = '/api/search?q=' + getSearchQuery
    fetch(url).then(res => res.json()).then(data => {
      if ('error' in data) {
        setFailMessage(data['error']);
        setGetSearchStatus('fail');
      } else {
        for (var i = 0; i < data.length; i++) {
          data[i] = JSON.parse(data[i]);
        }
        setGetSearchResponse(data);
        setGetSearchStatus('success');
      }
    });
  }, [getSearchQuery]);

  useEffect(() => {
    if (putBookDetails === '') return

    var url = '/api/book?id=' + putBookDetails.id
    fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: putBookDetails.json,
    }).then(res => res.json()).then(data => {
      if ('error' in data) {
        setFailMessage(data['error']);
        setPutBookStatus('fail');
      } else {
        for (var i = 0; i < data.length; i++) {
          data[i] = JSON.parse(data[i]);
        }
        setPutBookResponse(data);
        setPutBookStatus('success');
      }
    });
  }, [putBookDetails]);

  useEffect(() => {
    if (putAuthorDetails === '') return

    var url = '/api/author?id=' + putAuthorDetails.id
    fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: putAuthorDetails.json,
    }).then(res => res.json()).then(data => {
      if ('error' in data) {
        setFailMessage(data['error']);
        setPutAuthorStatus('fail');
      } else {
        for (var i = 0; i < data.length; i++) {
          data[i] = JSON.parse(data[i]);
        }
        setPutAuthorResponse(data);
        setPutAuthorStatus('success');
      }
    });
  }, [putAuthorDetails]);

  useEffect(() => {
    if (postBookJson === '') return

    var url = '/api/book'
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: postBookJson,
    }).then(res => res.json()).then(data => {
      if ('error' in data) {
        setFailMessage(data['error']);
        setPostStatus('fail');
      } else {
        setSuccessMessage(data['success']);
        setPostStatus('success');
      }
    });
  }, [postBookJson]);

  useEffect(() => {
    if (postBooksJson === '') return

    var url = '/api/books'
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: postBooksJson,
    }).then(res => res.json()).then(data => {
      if ('error' in data) {
        setFailMessage(data['error']);
        setPostStatus('fail');
      } else {
        setSuccessMessage(data['success']);
        setPostStatus('success');
      }
    });
  }, [postBooksJson]);

  useEffect(() => {
    if (postAuthorJson === '') return

    var url = '/api/author'
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: postAuthorJson,
    }).then(res => res.json()).then(data => {
      if ('error' in data) {
        setFailMessage(data['error']);
        setPostStatus('fail');
      } else {
        setSuccessMessage(data['success']);
        setPostStatus('success');
      }
    });
  }, [postAuthorJson]);

  useEffect(() => {
    if (postAuthorsJson === '') return

    var url = '/api/authors'
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: postAuthorsJson,
    }).then(res => res.json()).then(data => {
      if ('error' in data) {
        setFailMessage(data['error']);
        setPostStatus('fail');
      } else {
        setSuccessMessage(data['success']);
        setPostStatus('success');
      }
    });
  }, [postAuthorsJson]);

  useEffect(() => {
    if (deleteBookId === '') return

    var url = '/api/book?id=' + deleteBookId
    fetch(url, {method: 'DELETE'}).then(res => res.json()).then(data => {
      if ('error' in data) {
        setFailMessage(data['error']);
        setDeleteStatus('fail');
      } else {
        setSuccessMessage(data['success']);
        setDeleteStatus('success');
      }
    });
  }, [deleteBookId]);

  useEffect(() => {
    if (deleteAuthorId === '') return

    var url = '/api/author?id=' + deleteAuthorId
    fetch(url, {method: 'DELETE'}).then(res => res.json()).then(data => {
      if ('error' in data) {
        setFailMessage(data['error']);
        setDeleteStatus('fail');
      } else {
        setSuccessMessage(data['success']);
        setDeleteStatus('success');
      }
    });
  }, [deleteAuthorId]);

  useEffect(() => {
    if (visDetails.k === 0) return

    var url = ''
    if (visDetails.type === 'author') {
      url = '/vis/top-authors?k=' + visDetails.k
    } else {
      url = '/vis/top-books?k=' + visDetails.k
    }

    fetch(url).then(res => res.json()).then(data => {
      if ('error' in data) {
        setFailMessage(data['error']);
        setVisStatus('fail');
      } else {
        for (var i = 0; i < data.length; i++) {
          data[i] = JSON.parse(data[i]);
        }
        setVisResponse(data);
        setVisStatus('success');
      }
    });
  }, [visDetails]);

  return (
      <div className="container">
        <h1>Goodreads CRUD App</h1>
        <div className="flex-row">
          <div className="flex-large">
            <h2>API Input</h2>
            <RequestForm getBook={getBook} getAuthor={getAuthor} getSearch={getSearch}
                         putBook={putBook} putAuthor={putAuthor}
                         postBook={postBook} postBooks={postBooks} postAuthor={postAuthor} postAuthors={postAuthors}
                         deleteBook={deleteBook} deleteAuthor={deleteAuthor}
                         getVis={getVis}/>
          </div>
          <div className="flex-large">
            <h2>API Response</h2>
            {renderBook()}
            {renderAuthor()}
            {renderSearch()}
            {renderPutBook()}
            {renderPutAuthor()}
            {renderPost()}
            {renderDelete()}
            {renderVis()}
          </div>
        </div>
      </div>
  );
}

export default App;
