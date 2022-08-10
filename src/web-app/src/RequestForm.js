import React, { useState } from 'react'

/**
 * Request form component that creates a form for the user to input information to GET, PUT, POST, DELETE,
 * and VISUALIZE the database.
 * @param props - functions from the App component that will help with making the api requests
 * @returns {JSX.Element} RequestForm component with forms
 * @constructor NA
 */
const RequestForm = (props) => {

  /**
   * State variables to keep track of different input details.
   * Event handlers to update state variables.
   */

  const [getBookId, setGetBookId] = useState('')
  const handleGetBookChange = event => {
	const { value } = event.target
    setGetBookId(value)
  }

  const [getAuthorId, setGetAuthorId] = useState('')
  const handleGetAuthorChange = event => {
    const { value } = event.target
    setGetAuthorId(value)
  }

  const [getSearchQuery, setGetSearchQuery] = useState('')
  const handleGetSearchChange = event => {
    const { value } = event.target
    setGetSearchQuery(value)
  }

  const initialPut = { id: '', json: '' }
  const [putBookDetails, setPutBookDetails] = useState(initialPut)
  const handlePutBookChange = event => {
	const { name, value } = event.target
	setPutBookDetails({ ...putBookDetails, [name]: value })
  }

  const [putAuthorDetails, setPutAuthorDetails] = useState(initialPut)
  const handlePutAuthorChange = event => {
	const { name, value } = event.target
	setPutAuthorDetails({ ...putAuthorDetails, [name]: value })
  }

  const [postBookJson, setPostBookJson] = useState('')
  const handlePostBookChange = event => {
    const { value } = event.target
    setPostBookJson(value)
  }

  const [postBooksJson, setPostBooksJson] = useState('')
  const handlePostBooksChange = event => {
    const { value } = event.target
    setPostBooksJson(value)
  }

  const [postAuthorJson, setPostAuthorJson] = useState('')
  const handlePostAuthorChange = event => {
    const { value } = event.target
    setPostAuthorJson(value)
  }

  const [postAuthorsJson, setPostAuthorsJson] = useState('')
  const handlePostAuthorsChange = event => {
    const { value } = event.target
    setPostAuthorsJson(value)
  }

  const [deleteBookId, setDeleteBookId] = useState('')
  const handleDeleteBookChange = event => {
	const { value } = event.target
    setDeleteBookId(value)
  }

  const [deleteAuthorId, setDeleteAuthorId] = useState('')
  const handleDeleteAuthorChange = event => {
	const { value } = event.target
    setDeleteAuthorId(value)
  }

  const [kBooks, setKBooks] = useState('')
  const handleVisBooksChange = event => {
	const { value } = event.target
    setKBooks(value)
  }

  const [kAuthors, setKAuthors] = useState('')
  const handleVisAuthorsChange = event => {
	const { value } = event.target
    setKAuthors(value)
  }

  return (
    <>
    <form
        onSubmit={event => {
            event.preventDefault()
            if (!getBookId) return
            props.getBook(getBookId)
        }}
    >
      <label>Book ID</label>
      <input type="text" name="id" value={getBookId} onChange={handleGetBookChange} />
      <button>GET Book</button>
    </form>
    <form
        onSubmit={event => {
            event.preventDefault()
            if (!getAuthorId) return
            props.getAuthor(getAuthorId)
        }}
    >
      <label>Author ID</label>
      <input type="text" name="id" value={getAuthorId} onChange={handleGetAuthorChange} />
      <button>GET Author</button>
    </form>
    <form
        onSubmit={event => {
            event.preventDefault()
            if (!getSearchQuery) return
            props.getSearch(getSearchQuery)
        }}
    >
      <label>Search Query</label>
      <input type="text" name="query" value={getSearchQuery} onChange={handleGetSearchChange} />
      <button>GET Search</button>
    </form>
    <form
        onSubmit={event => {
            event.preventDefault()
            if (!putBookDetails) return
            props.putBook(putBookDetails)
        }}
    >
      <label>Book ID</label>
      <input type="text" name="id" value={putBookDetails.id} onChange={handlePutBookChange} />
      <label>JSON Input</label>
      <input type="text" name="json" value={putBookDetails.json} onChange={handlePutBookChange} />
      <button>PUT Book</button>
    </form>
    <form
        onSubmit={event => {
            event.preventDefault()
            if (!putAuthorDetails) return
            props.putAuthor(putAuthorDetails)
        }}
    >
      <label>Author ID</label>
      <input type="text" name="id" value={putAuthorDetails.id} onChange={handlePutAuthorChange} />
      <label>JSON Input</label>
      <input type="text" name="json" value={putAuthorDetails.json} onChange={handlePutAuthorChange} />
      <button>PUT Author</button>
    </form>
    <form
        onSubmit={event => {
            event.preventDefault()
            if (!postBookJson) return
            props.postBook(postBookJson)
        }}
    >
      <label>JSON Input</label>
      <input type="text" name="name" value={postBookJson} onChange={handlePostBookChange} />
      <button>POST Book</button>
    </form>
    <form
        onSubmit={event => {
            event.preventDefault()
            if (!postBooksJson) return
            props.postBooks(postBooksJson)
        }}
    >
      <label>JSON Input</label>
      <input type="text" name="name" value={postBooksJson} onChange={handlePostBooksChange} />
      <button>POST Books</button>
    </form>
    <form
        onSubmit={event => {
            event.preventDefault()
            if (!postAuthorJson) return
            props.postAuthor(postAuthorJson)
        }}
    >
      <label>JSON Input</label>
      <input type="text" name="name" value={postAuthorJson} onChange={handlePostAuthorChange} />
      <button>POST Author</button>
    </form>
    <form
        onSubmit={event => {
            event.preventDefault()
            if (!postAuthorsJson) return
            props.postAuthors(postAuthorsJson)
        }}
    >
      <label>JSON Input</label>
      <input type="text" name="name" value={postAuthorsJson} onChange={handlePostAuthorsChange} />
      <button>POST Authors</button>
    </form>
    <form>
      <label>Book URL</label>
      <input type="text" name="name" value="" />
      <button>POST Scrape</button>
    </form>
    <form
        onSubmit={event => {
            event.preventDefault()
            if (!deleteBookId) return
            props.deleteBook(deleteBookId)
        }}
    >
      <label>Book ID</label>
      <input type="text" name="id" value={deleteBookId} onChange={handleDeleteBookChange} />
      <button>DELETE Book</button>
    </form>
    <form
        onSubmit={event => {
            event.preventDefault()
            if (!deleteAuthorId) return
            props.deleteAuthor(deleteAuthorId)
        }}
    >
      <label>Author ID</label>
      <input type="text" name="id" value={deleteAuthorId} onChange={handleDeleteAuthorChange} />
      <button>DELETE Author</button>
    </form>
    <form
        onSubmit={event => {
            event.preventDefault()
            if (!kBooks) return
            props.getVis({k: kBooks, type: 'book'})
        }}
    >
      <label>Top k Books</label>
      <input type="text" name="k" value={kBooks} onChange={handleVisBooksChange} />
      <button>Render Visualization</button>
    </form>
    <form
        onSubmit={event => {
            event.preventDefault()
            if (!kAuthors) return
            props.getVis({k: kAuthors, type: 'author'})
        }}
    >
      <label>Top k Authors</label>
      <input type="text" name="k" value={kAuthors} onChange={handleVisAuthorsChange} />
      <button>Render Visualization</button>
    </form>
    </>
  )
}

export default RequestForm